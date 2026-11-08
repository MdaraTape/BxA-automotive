import os
import re
import secrets
import sqlite3
from pathlib import Path

from flask import Flask, abort, flash, g, jsonify, redirect, render_template, request, session, url_for

ROOT = Path(__file__).resolve().parent
INTERESTS = ("Hand-control consultation", "Wheelchair transfer", "Other access need")


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE=str(Path(app.instance_path) / "bxa.sqlite"),
        SECRET_KEY=os.environ.get("BXA_SECRET"),
        SESSION_COOKIE_SAMESITE="Lax",
    )
    if config:
        app.config.update(config)
    Path(app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)
    if not app.secret_key:
        key_path = Path(app.instance_path) / "session.key"
        key_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with key_path.open("x") as key_file:
                key_file.write(secrets.token_hex(32))
        except FileExistsError:
            pass
        app.secret_key = key_path.read_text()

    def db():
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DATABASE"])
            g.db.row_factory = sqlite3.Row
            g.db.execute("PRAGMA foreign_keys = ON")
        return g.db

    @app.teardown_appcontext
    def close_db(_error):
        connection = g.pop("db", None)
        if connection:
            connection.close()

    @app.cli.command("init-db")
    def init_db():
        db().executescript((ROOT / "schema.sql").read_text())
        db().executescript((ROOT / "seed.sql").read_text())
        print("BxA database and sample catalogue ready.")

    def cart():
        return session.get("cart", [])

    @app.context_processor
    def shared():
        if "csrf" not in session:
            session["csrf"] = secrets.token_hex(24)
        return {"csrf": session["csrf"], "cart_count": sum(line["quantity"] for line in cart())}

    @app.before_request
    def protect_forms():
        if request.method == "POST":
            expected = session.get("csrf", "")
            if not expected or not secrets.compare_digest(expected, request.form.get("csrf", "")):
                abort(400, "Invalid form token. Reload the page and try again.")

    @app.template_filter("money")
    def money(value):
        return f"${value // 100:,}.{value % 100:02d}"

    def product(product_id):
        record = db().execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
        if record is None:
            abort(404)
        return record

    def selection(item, colour_id, trim_id):
        if item["kind"] == "accessory":
            if colour_id or trim_id:
                abort(400, "Accessories do not accept vehicle options.")
            return None, None, item["price"]
        options = []
        for kind, option_id in (("colour", colour_id), ("trim", trim_id)):
            option = db().execute(
                "SELECT * FROM vehicle_options WHERE id = ? AND product_id = ? AND kind = ?",
                (option_id, item["id"], kind),
            ).fetchone()
            if not option:
                abort(400, f"Choose a valid {kind} for this vehicle.")
            options.append(option)
        colour, trim = options
        return colour["label"], trim["label"], item["price"] + colour["adjustment"] + trim["adjustment"]

    def cart_details():
        details = []
        for index, line in enumerate(cart()):
            item = product(line["product_id"])
            colour, trim, unit_price = selection(item, line["colour"], line["trim"])
            details.append(dict(index=index, product=item, quantity=line["quantity"],
                                colour=colour, trim=trim, price=unit_price,
                                subtotal=unit_price * line["quantity"]))
        return details

    @app.get("/")
    def catalog():
        needs = db().execute("SELECT * FROM access_needs ORDER BY id").fetchall()
        active = request.args.getlist("need", type=int)
        active = sorted(set(active) & {need["id"] for need in needs})
        kind = request.args.get("kind", "")
        query = "SELECT * FROM products p WHERE 1=1"
        params = []
        if kind in ("vehicle", "accessory"):
            query += " AND kind = ?"
            params.append(kind)
        if active:
            placeholders = ",".join("?" for _ in active)
            query += f""" AND id IN (
                SELECT product_id FROM product_access_needs WHERE need_id IN ({placeholders})
                GROUP BY product_id HAVING COUNT(*) = ?)"""
            params.extend([*active, len(active)])
        items = db().execute(query + " ORDER BY id", params).fetchall()
        return render_template("shop.html", items=items, needs=needs, active=active, kind=kind)

    @app.get("/products/<int:product_id>")
    def detail(product_id):
        item = product(product_id)
        options = db().execute(
            "SELECT * FROM vehicle_options WHERE product_id = ? ORDER BY id", (product_id,)
        ).fetchall()
        return render_template("detail.html", item=item, options=options, interests=INTERESTS)

    @app.post("/cart/add/<int:product_id>")
    def add(product_id):
        item = product(product_id)
        colour = request.form.get("colour", type=int)
        trim = request.form.get("trim", type=int)
        selection(item, colour, trim)
        lines = cart()
        match = next((line for line in lines if (line["product_id"], line["colour"], line["trim"])
                      == (product_id, colour, trim)), None)
        if match:
            if match["quantity"] == 20:
                abort(400, "Maximum quantity is 20 per line.")
            match["quantity"] += 1
        else:
            if len(lines) >= 20:
                abort(400, "Maximum of 20 distinct cart lines.")
            lines.append(dict(product_id=product_id, colour=colour, trim=trim, quantity=1))
        session["cart"] = lines
        session.pop("checkout_token", None)
        if request.accept_mimetypes.best == "application/json":
            return jsonify(count=sum(line["quantity"] for line in lines), message="Added to cart.")
        flash("Added to cart.")
        return redirect(url_for("view_cart"))

    @app.get("/cart")
    def view_cart():
        lines = cart_details()
        return render_template("cart.html", lines=lines, total=sum(line["subtotal"] for line in lines))

    @app.post("/cart/<int:index>")
    def update_cart(index):
        lines = cart()
        if index >= len(lines):
            abort(404)
        if request.form.get("action") == "remove":
            lines.pop(index)
        else:
            quantity = request.form.get("quantity", type=int)
            if quantity is None or not 1 <= quantity <= 20:
                abort(400, "Choose a quantity between 1 and 20.")
            lines[index]["quantity"] = quantity
        session["cart"] = lines
        session.pop("checkout_token", None)
        return redirect(url_for("view_cart"))

    def contact():
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        if not 1 <= len(name) <= 100 or len(email) > 254 or not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
            abort(400, "Enter a name and a valid email address.")
        return name, email

    @app.route("/checkout", methods=["GET", "POST"])
    def checkout():
        if request.method == "GET":
            if not cart():
                return redirect(url_for("view_cart"))
            if "checkout_token" not in session:
                session["checkout_token"] = secrets.token_hex(24)
            return render_template("checkout.html", token=session["checkout_token"], lines=cart_details())
        token = request.form.get("token", "")
        if token != session.get("checkout_token") or not token:
            abort(400, "Open checkout again before placing the order.")
        connection = db()
        with connection:
            connection.execute("BEGIN IMMEDIATE")
            prior = connection.execute("SELECT reference FROM orders WHERE checkout_token = ?", (token,)).fetchone()
            if prior:
                reference = prior["reference"]
            else:
                name, email = contact()
                address = request.form.get("address", "").strip()
                if not 1 <= len(address) <= 300 or not cart():
                    abort(400, "Enter a delivery address and add at least one item.")
                lines = cart_details()
                reference = secrets.token_hex(10).upper()
                order_id = connection.execute(
                    "INSERT INTO orders(reference,checkout_token,name,email,address,total) VALUES (?,?,?,?,?,?)",
                    (reference, token, name, email, address, sum(line["subtotal"] for line in lines)),
                ).lastrowid
                connection.executemany(
                    """INSERT INTO order_items(order_id,product_id,name,unit_price,quantity,colour,trim)
                       VALUES (?,?,?,?,?,?,?)""",
                    [(order_id, line["product"]["id"], line["product"]["name"], line["price"],
                      line["quantity"], line["colour"], line["trim"]) for line in lines],
                )
        session["cart"] = []
        return redirect(url_for("confirmation", reference=reference))

    @app.get("/orders/<reference>")
    def confirmation(reference):
        order = db().execute("SELECT id,reference,total FROM orders WHERE reference = ?", (reference,)).fetchone()
        if not order:
            abort(404)
        lines = db().execute("SELECT * FROM order_items WHERE order_id = ? ORDER BY id", (order["id"],)).fetchall()
        return render_template("confirmation.html", order=order, lines=lines)

    @app.post("/enquiries/<int:product_id>")
    def enquiry(product_id):
        item = product(product_id)
        interest = request.form.get("interest", "")
        if item["kind"] != "vehicle" or interest not in INTERESTS:
            abort(400, "Select a vehicle and a consultation interest.")
        name, email = contact()
        reference = secrets.token_hex(6).upper()
        connection = db()
        with connection:
            connection.execute(
                "INSERT INTO enquiries(reference,product_id,name,email,interest) VALUES (?,?,?,?,?)",
                (reference, product_id, name, email, interest),
            )
        flash(f"Consultation enquiry saved. Reference {reference}.")
        return redirect(url_for("detail", product_id=product_id))

    @app.errorhandler(400)
    @app.errorhandler(404)
    def error_page(error):
        if request.accept_mimetypes.best == "application/json":
            return jsonify(message=error.description), error.code
        return render_template("error.html", error=error), error.code

    return app

import sqlite3
import tempfile
import unittest
from pathlib import Path

from app import create_app


class StoreTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "test.sqlite"
        self.app = create_app({"TESTING": True, "DATABASE": str(self.path), "SECRET_KEY": "test"})
        result = self.app.test_cli_runner().invoke(args=["init-db"])
        self.assertEqual(result.exit_code, 0, result.output)
        self.client = self.app.test_client()
        self.client.get("/")
        with self.client.session_transaction() as session:
            self.csrf = session["csrf"]

    def post(self, path, **values):
        return self.client.post(path, data={"csrf": self.csrf, **values})

    def cart_revision(self):
        self.client.get("/cart")
        with self.client.session_transaction() as session:
            return session["cart_revision"]

    def rows(self, query):
        with sqlite3.connect(self.path) as connection:
            return connection.execute(query).fetchall()

    def test_multi_filter_matches_both_needs(self):
        response = self.client.get("/?need=2&need=3")
        self.assertIn(b"Wide grip key sleeve", response.data)
        self.assertIn(b"Large zip pull set", response.data)
        self.assertNotIn(b"Seat belt reach handle", response.data)

    def test_order_snapshot_and_retry(self):
        self.assertEqual(self.post("/cart/add/1", colour=2, trim=4, price=1).status_code, 302)
        self.assertEqual(self.post("/cart/add/6").status_code, 302)
        self.assertEqual(self.post("/cart/1", quantity=3, revision=self.cart_revision()).status_code, 302)
        self.client.get("/checkout")
        with self.client.session_transaction() as session:
            token = session["checkout_token"]
        form = dict(token=token, name="Demo Customer", email="demo@example.com", address="1 Demo Lane")
        response = self.post("/checkout", **form)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.post("/checkout", **form).location, response.location)
        self.assertEqual(self.rows("SELECT total FROM orders"), [(15545000,)])
        self.assertEqual(
            self.rows("SELECT unit_price, quantity, colour, trim FROM order_items ORDER BY id"),
            [(15530000, 1, "Polar White", "Premium"), (5000, 3, None, None)],
        )
        with sqlite3.connect(self.path) as connection:
            connection.execute("UPDATE products SET price = 1")
        self.assertIn(b"$155,450.00", self.client.get(response.location).data)

    def test_invalid_option_quantity_and_form_token(self):
        self.assertEqual(self.post("/cart/add/1", colour=5, trim=4).status_code, 400)
        self.assertEqual(self.client.post("/cart/add/6").status_code, 400)
        self.post("/cart/add/6")
        self.assertEqual(self.post("/cart/0", quantity=0, revision=self.cart_revision()).status_code, 400)
        self.assertEqual(self.post("/cart/0", action="remove", revision=self.cart_revision()).status_code, 302)
        self.assertIn(b"Your cart is empty", self.client.get("/cart").data)

    def test_enquiry_is_separate_from_orders(self):
        form = dict(name="Demo Customer", email="demo@example.com", interest="Hand-control consultation")
        self.assertEqual(self.post("/enquiries/6", **form).status_code, 400)
        self.assertEqual(self.post("/enquiries/1", **form).status_code, 302)
        self.assertEqual(self.rows("SELECT product_id, interest FROM enquiries"), [(1, form["interest"])])
        self.assertEqual(self.rows("SELECT id FROM orders"), [])

    def test_empty_checkout_and_duplicate_cart_add(self):
        response = self.client.get("/checkout", follow_redirects=True)
        self.assertIn(b"Your cart is empty", response.data)
        self.post("/cart/add/6")
        self.post("/cart/add/6")
        with self.client.session_transaction() as session:
            self.assertEqual(len(session["cart"]), 1)
            self.assertEqual(session["cart"][0]["quantity"], 2)

    def test_stale_cart_form_cannot_update_a_different_line(self):
        self.post("/cart/add/6")
        self.post("/cart/add/7")
        old_revision = self.cart_revision()
        self.post("/cart/0", action="remove", revision=old_revision)
        response = self.post("/cart/0", quantity=9, revision=old_revision)
        self.assertEqual(response.status_code, 302)
        with self.client.session_transaction() as session:
            self.assertEqual(session["cart"][0]["product_id"], 7)
            self.assertEqual(session["cart"][0]["quantity"], 1)
        self.assertIn(b"Your cart changed", self.client.get("/cart").data)

    def test_non_ascii_form_token_returns_bad_request(self):
        response = self.client.post("/cart/add/6", data={"csrf": "incorrect-☃"})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Invalid form token", response.data)

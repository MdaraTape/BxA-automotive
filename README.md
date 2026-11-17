# BxA Automotive
Bavaira x Affalterbach is a student e-commerce prototype for premium sample vehicles and accessories. Customers can filter accessories by multiple access needs and send a separate adaptation consultation enquiry.

## Brand and manufacturer disclaimer
BxA is an independent student project. It is not affiliated with, endorsed by or
authorised by BMW, Mercedes-Benz or Mercedes-AMG. Manufacturer names identify
sample vehicles only. All purchases and payments are simulated. Access-needs
filters and consultation enquiries do not confirm medical suitability or
adaptation compatibility. Prices and vehicle options are fictional demo data.

## Run locally
Use Python 3.10 or later. Download the repository from the default `main`
branch and extract it, or clone it. Open a terminal in the folder containing
`app.py` and `requirements.txt`.

Windows PowerShell (activation is unnecessary when calling the interpreter directly):

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m flask --app app:create_app init-db
.\.venv\Scripts\python.exe -m flask --app app:create_app run
```

macOS / Linux:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m flask --app app:create_app init-db
.venv/bin/python -m flask --app app:create_app run
```

Open http://127.0.0.1:5000. Use sample contact details. The SQLite file and local session key are stored under the ignored `instance/` directory. Initialisation creates tables and inserts missing sample data.

## Try the prototype
1. Choose **Accessories** in the product-type filter and apply it.
2. Open **Foldable transfer board**. Its detail page shows the name, description,
   database price of $125.00, **Add to cart**, and **View cart**.
3. Click **Add to cart**. JavaScript updates the cart count and shows a status
   message. Open **View cart**, check quantity 1 and total $125.00, then use
   **Simulated checkout**.
4. Enter sample details such as Demo Customer, demo@example.com and 1 Demo Lane.
   Place the simulated order. **Order saved** shows the reference and $125.00 total.
5. Return to the catalogue. Select **Hand and arm mobility** and **Grip and
   dexterity** to return two accessories matching both needs.
6. Open the GLE sample vehicle. Polar White and Premium produce a fictional
   $155,300.00 price. Add it and complete another simulated order.
7. On the vehicle detail page, save a separate adaptation consultation enquiry.

## Product-detail view
The complete purchase sequence is catalogue -> product detail -> cart -> checkout
-> confirmation. The detail view sits between browsing and the cart. Accessories
show a Purchase panel with Add to cart and View cart. Vehicle details add colour
and trim selectors and a separate consultation form. This distinction is shown
in the final documentation and screenshots under `docs/`.

See [the finalization evidence](docs/finalization.md) for the product-detail
wireframe, student screenshots and verification scope.

## Design
- Flask and Jinja render the pages. HTML forms work with JavaScript disabled.
- The signed session holds product and option IDs and quantities. Flask calculates totals from integer cents stored in SQLite.
- An SQLite transaction saves the order and its line items together. The order records the unit price, colour and trim at checkout.
- The access-needs join table lets an accessory match several categories. Vehicle options belong to a specific vehicle.
- Adaptation enquiries are recorded separately from purchases. Payment is simulated.

## Final release checks
Finalization retains the Phase 2 implementation and adds form validation fixes,
manufacturer disclaimers and documentation responding to tutor feedback. The
`phase-2` branch preserves the assessed development milestone.

Cart forms carry a revision identifier. A form left open in another tab refreshes
the cart if an intervening update moved or removed its target row. Form tokens
are compared as bytes so malformed Unicode values return HTTP 400.

The database schema is in `schema.sql`. The data in `seed.sql` provide two sample
vehicles, eight accessories and four access-needs categories. From the catalogue,
try a filtered search, add a vehicle and an accessory, change a quantity, then
place a simulated order. The confirmation shows the saved options and prices.
For a fresh demo, stop the server and point `DATABASE` at a temporary file when
creating the app, or move the local `instance/` directory aside and rerun init-db.

## Verification
Windows: `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`.
macOS / Linux: `.venv/bin/python -m unittest discover -s tests -v`. Tests use a temporary SQLite database and synthetic inputs.

## Scope and assistance
The final coursework release covers guest purchasing and adaptation enquiries. The prototype uses two sample vehicles, eight accessories and fictional demo prices. It does not collect payment information. ChatGPT assisted with implementation, verification and portfolio drafting. Review the source and adapt the reflection to your own experience before submission.

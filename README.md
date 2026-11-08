# BxA Automotive
Bavaira x Affalterbach is a student e-commerce prototype for premium sample vehicles and accessories. Customers can filter accessories by multiple access needs and send a separate adaptation consultation enquiry.

## Run locally
Use Python 3.10 or later. From the repository directory:

```sh
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS / Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m flask --app app:create_app init-db
python -m flask --app app:create_app run
```

Open http://127.0.0.1:5000. Use sample contact details. The SQLite file and local session key are stored under the ignored `instance/` directory. Initialisation creates tables and inserts missing sample data.

## Try the prototype
1. Select **Hand and arm mobility** and **Grip and dexterity**. Results match both needs.
2. Open a vehicle and choose a colour and trim. **Add to cart** updates the cart count through fetch and JSON.
3. Change a quantity in the cart and continue to simulated checkout. Submit sample details to receive an order reference.
4. Return to a vehicle and save a separate adaptation enquiry.

## Design
- Flask and Jinja render the pages. HTML forms work with JavaScript disabled.
- The signed session holds product and option IDs and quantities. Flask calculates totals from integer cents stored in SQLite.
- An SQLite transaction saves the order and its line items together. The order records the unit price, colour and trim at checkout.
- The access-needs join table lets an accessory match several categories. Vehicle options belong to a specific vehicle.
- Adaptation enquiries are recorded separately from purchases. Payment is simulated.

## Final release checks
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
Run `python -m unittest discover -s tests -v`. Tests use a temporary SQLite database and synthetic inputs.

## Scope and assistance
The final coursework release covers guest purchasing and adaptation enquiries. The prototype uses two sample vehicles, eight accessories and fictional demo prices. It does not collect payment information. ChatGPT assisted with implementation, verification and portfolio drafting. Review the source and adapt the reflection to your own experience before submission.

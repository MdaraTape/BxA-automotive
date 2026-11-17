# BxA finalization and evidence

## Response to Phase 2 feedback released 16 November 2026

The final release incorporates the Phase 2 code and final validation fixes into
the default `main` branch. The root README includes installation, database and
test commands, the accessory-first demo sequence, and the manufacturer disclaimer.
The same disclaimer appears in the shared footer on every application page.

## Product detail between catalogue and cart

![Accessory product-detail wireframe](product-detail.svg)

Open a product name in the catalogue to reach `/products/<id>`. For example,
`/products/5` shows Foldable transfer board, its description and $125.00 price.
The Purchase panel contains **Add to cart** and **View cart**. Adding posts the
product ID and form token to Flask. With JavaScript enabled, JSON updates the
cart count and the page announces Added to cart. Without JavaScript, the form
redirects to the cart. The cart shows quantity, unit price, subtotal, Update,
Remove and Simulated checkout. The final confirmation reads saved order records.

Vehicles add colour and trim choices. Their adaptation enquiry is stored in a
separate table. Access-needs tags filter accessories and do not establish
medical suitability or certify an adaptation.

## Scope and data

There are two sample vehicles, eight accessories and four access-needs categories.
Multiple selected access needs use AND matching. Prices are fictional USD amounts
stored as integer cents. The signed Flask session stores the cart. SQLite stores
products, options, tags, orders, order items and enquiries. Guest cart persistence
depends on the browser session cookie. Saved orders survive later catalogue-price
changes. No accounts, real payments, stock reservation or certified adaptation
matching are implemented.

## Verification on 17 November 2026

Eight automated tests passed in Python 3.12 with Flask 3.1.2. The suite covers
combined filtering, cross-vehicle option rejection, missing and malformed form
tokens, invalid quantity, removal, duplicate additions, an empty checkout,
stale cart forms, order snapshots, checkout retry, separate enquiries, and the
accessory detail-to-confirmation journey including the AJAX response and SQLite
order line.

A transfer-board test saved one item at 12,500 cents with a 12,500-cent order
total. The configured-vehicle test saved Polar White/Premium and the order price
snapshot. The test includes three organisers for a combined $155,450.00 total.

Earlier Chromium verification and the student's 9 November browser screenshots
support the Phase 2 flow. A fresh browser walkthrough of this final release is
pending because the current browser environment blocked local-page access.
Broader cross-browser and assistive-technology testing remains future work.

## Final evidence capture

Run this release following the root README. Capture the Foldable transfer board
detail page with its name, description, $125.00 price, Add to cart and View cart
visible. Capture the Added to cart message and updated cart count as well. Include
the visible manufacturer disclaimer in the final evidence. Use sample contact
details for any repeated checkout. Keep the screenshots from the exact release
included in the final code ZIP.

## Assistance

ChatGPT assisted with implementation, testing, diagrams and documentation. The
student reviews the work, tests the application and explains the implementation
and reflection in their own words.

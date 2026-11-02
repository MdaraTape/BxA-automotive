# BxA - Bavaira x Affalterbach

Disability-inclusive automotive e-commerce store offering accessories and simulated premium vehicle purchases.
Student project: DLBITPEWP01_E, Option 2 (E-commerce).

## Status
Phase 1 planning only. No runnable application or completed tests are claimed.
Repository URL: https://github.com/MdaraTape/BxA-automotive

## Purpose
Serve disabled and non-disabled customers through a shared shopping experience.
Disability-focused products and optional adaptation consultation enquiries are explicit features.
This is an independent educational concept, not an authorised manufacturer service.

## Planned stack
Python, Flask, Jinja, HTML, custom CSS, JavaScript fetch/JSON and SQLite via sqlite3.
Signed Flask session for product IDs and quantities; server-authoritative prices.

## Core features
- Approximately eight seeded accessories and two or three sample premium vehicles; catalogue filtering and detail pages.
- Multi-select access needs: leg/foot mobility, hand/arm mobility, grip/dexterity,
  wheelchair use/transfers. Browsing without a filter remains possible.
- Other / discuss my needs is an enquiry option; no diagnoses required.
- Cart with quantity updates and removal; asynchronous add-to-cart badge.
- Validated guest checkout, simulated payment, persisted orders and confirmation.
- Vehicle studio: select a sample car, colour and trim, add the configured car to the cart,
  complete simulated checkout and receive a saved order confirmation.
- Separate disability-related adaptation consultation enquiries, including hand-control requests.
  An enquiry is not an installed adaptation or confirmed vehicle compatibility.
- Keyboard operation, visible focus, labels, alternative text and clear errors.

## Planned database
categories -> products -> order_items <- orders
products -> vehicle_options (allowed colours/trims and price adjustments for vehicle products)
products -> enquiries (vehicle products only)
products <-> access_needs through product_access_needs
Each order contains one or more items. Monetary values use integer minor units.
Products distinguish accessories from vehicles using a product type.
Order items retain product name, configured unit price and selected colour/trim snapshots.
The backend validates vehicle options and recalculates all prices from trusted database data.

## Development sequence
1. Read and apply Phase 1 tutor feedback.
2. Schema, seed data and a database-backed catalogue page.
3. Product details and vehicle configuration; cart, validation and asynchronous interaction.
4. Checkout, atomic order writes and confirmation.
5. Disability-related consultation form and persisted enquiries.
6. Tests, accessibility checks, screenshots and documentation.

## Setup
To be documented when implementation exists: Python version, dependency installation,
environment variables, database initialisation/seeding and application launch commands.
Do not submit the final project with this setup section incomplete.

## Planned verification
Cart quantity boundaries; invalid product IDs; tampered prices; empty cart;
checkout errors; invalid vehicle options; configured vehicle price calculation;
order/item and configuration persistence; enquiry validation; keyboard use;
responsive layout and two-browser checks. Record actual results during development.

## Scope exclusions
No user accounts, real payments, legally binding vehicle sales, delivery logistics
or actual adaptation installation. Vehicle purchases are educational simulations.
Consultation requests do not confirm vehicle compatibility or medical suitability.

## Evidence and attribution
Use incremental commits. Record challenges and scope changes honestly.
Track image sources, libraries, tutorials and AI assistance according to school rules.
Use synthetic customer data in tests and screenshots. Do not commit secrets.

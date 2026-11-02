# BxA - Bavaria x Affalterbach

Disability-inclusive automotive accessories store and premium vehicle enquiry studio.
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
- Approximately eight seeded products; catalogue filtering and detail pages.
- Multi-select access needs: leg/foot mobility, hand/arm mobility, grip/dexterity,
  wheelchair use/transfers. Browsing without a filter remains possible.
- Other / discuss my needs is an enquiry option; no diagnoses required.
- Cart with quantity updates and removal; asynchronous add-to-cart badge.
- Validated guest checkout, simulated payment, persisted orders and confirmation.
- Sample vehicle/colour/trim selection and separate disability-related consultation enquiries.
- Keyboard operation, visible focus, labels, alternative text and clear errors.

## Planned database
categories -> products -> order_items <- orders
vehicles -> enquiries
products <-> access_needs through product_access_needs
Each order contains one or more items. Monetary values use integer minor units.
Order items retain a product name and price snapshot.

## Development sequence
1. Read and apply Phase 1 tutor feedback.
2. Schema, seed data and a database-backed catalogue page.
3. Details and cart; validation and asynchronous interaction.
4. Checkout, atomic order writes and confirmation.
5. Vehicle studio and persisted enquiries.
6. Tests, accessibility checks, screenshots and documentation.

## Setup
To be documented when implementation exists: Python version, dependency installation,
environment variables, database initialisation/seeding and application launch commands.
Do not submit the final project with this setup section incomplete.

## Planned verification
Cart quantity boundaries; invalid product IDs; tampered prices; empty cart;
checkout errors; order/item persistence; enquiry validation; keyboard use;
responsive layout and two-browser checks. Record actual results during development.

## Scope exclusions
No user accounts, real payments, vehicle sales or actual adaptation installation.
Consultation requests do not confirm vehicle compatibility or medical suitability.

## Evidence and attribution
Use incremental commits. Record challenges and scope changes honestly.
Track image sources, libraries, tutorials and AI assistance according to school rules.
Use synthetic customer data in tests and screenshots. Do not commit secrets.

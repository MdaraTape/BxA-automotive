CREATE TABLE IF NOT EXISTS categories (
  id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS products (
  id INTEGER PRIMARY KEY, category_id INTEGER NOT NULL REFERENCES categories(id),
  name TEXT NOT NULL, kind TEXT NOT NULL CHECK(kind IN ('vehicle','accessory')),
  price INTEGER NOT NULL CHECK(price >= 0), description TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS access_needs (
  id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS product_access_needs (
  product_id INTEGER REFERENCES products(id), need_id INTEGER REFERENCES access_needs(id),
  PRIMARY KEY(product_id, need_id)
);
CREATE TABLE IF NOT EXISTS vehicle_options (
  id INTEGER PRIMARY KEY, product_id INTEGER NOT NULL REFERENCES products(id),
  kind TEXT NOT NULL CHECK(kind IN ('colour','trim')), label TEXT NOT NULL,
  adjustment INTEGER NOT NULL CHECK(adjustment >= 0)
);
CREATE TABLE IF NOT EXISTS orders (
  id INTEGER PRIMARY KEY, reference TEXT UNIQUE NOT NULL, checkout_token TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL, email TEXT NOT NULL, address TEXT NOT NULL, total INTEGER NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS order_items (
  id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL REFERENCES orders(id),
  product_id INTEGER NOT NULL REFERENCES products(id), name TEXT NOT NULL,
  unit_price INTEGER NOT NULL, quantity INTEGER NOT NULL CHECK(quantity BETWEEN 1 AND 20),
  colour TEXT, trim TEXT
);
CREATE TABLE IF NOT EXISTS enquiries (
  id INTEGER PRIMARY KEY, reference TEXT UNIQUE NOT NULL, product_id INTEGER NOT NULL REFERENCES products(id),
  name TEXT NOT NULL, email TEXT NOT NULL, interest TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

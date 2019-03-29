DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS default_transactions;
DROP TABLE IF EXISTS transaction_categories;
DROP TABLE IF EXISTS transaction_subcategories;
DROP TABLE IF EXISTS partners;
DROP TABLE IF EXISTS shorthands_to_partners;
DROP TABLE IF EXISTS shorthands_to_subcategories;


-- Subcategories rule, supercategories are only used for grouping / statistics
-- Auto-incrementing row ids are implicitly created by SQLite as 'rowid'
-- Dates are stored as INTEGER (seconds since epoch)
-- Due to lack of a DECIMAL type, money is stored as integers of hundredth fractions ($220.20 is stored as `22020`)

CREATE TABLE transactions (
  partner_id INTEGER NOT NULL,
  amount_hundredths INTEGER NOT NULL,            -- Store $220.20 as `22020` to avoid loss of precision (no `decimal` type in SQLite)
  currency TEXT NOT NULL,
  subcategory_id INTEGER NOT NULL,               -- Category is redundant as it can be assumed from subcategory
  datestamp INTEGER NOT NULL,                    -- When the transaction took place
  created_at INTEGER DEFAULT CURRENT_TIMESTAMP,  -- When it was added to the database
  gps_latitude REAL,                             -- Tiny loss of precision OK here
  gps_longitude REAL,                            -- Tiny loss of precision OK here
  comment TEXT,
  PRIMARY KEY rowid,
  FOREIGN KEY (partner_id) REFERENCES partners(rowid),
  FOREIGN KEY (subcategory_id) REFERENCES transaction_categories(rowid)
);

CREATE TABLE default_transactions (              -- Same as transactions, excluding datestamp, gps_latitude, gps_longitude
  partner_id INTEGER NOT NULL,
  amount_hundredths INTEGER NOT NULL,            -- Store $220.20 as `22020` to avoid loss of precision (no `decimal` type in SQLite)
  currency TEXT NOT NULL,
  subcategory_id INTEGER NOT NULL,               -- Category is assumed from subcategory
  created_at INTEGER DEFAULT CURRENT_TIMESTAMP,  -- When it was added to the database
  comment TEXT,
  PRIMARY KEY partner_id,
  FOREIGN KEY (partner_id) REFERENCES partners(rowid),
  FOREIGN KEY (subcategory_id) REFERENCES transaction_categories(rowid)
);

CREATE TABLE transaction_categories (
  name TEXT NOT NULL,
  created_at INTEGER DEFAULT CURRENT_TIMESTAMP,
  comment TEXT,
  default_subcategory_id INTEGER,
  FOREIGN KEY (default_subcategory_id) REFERENCES transaction_subcategories(rowid)
);

CREATE TABLE transaction_subcategories (
  created_at INTEGER DEFAULT CURRENT_TIMESTAMP,
  name TEXT NOT NULL,
  comment TEXT,
  category_id INTEGER NOT NULL,
  FOREIGN KEY (category_id) REFERENCES transaction_categories(rowid)
);

CREATE TABLE partners (
  created_at INTEGER DEFAULT CURRENT_TIMESTAMP,
  full_name TEXT NOT NULL,
  default_subcategory_id INTEGER,
  FOREIGN KEY (default_subcategory_id) REFERENCES transaction_subcategories(rowid)
);

CREATE TABLE shorthands_to_partners (
  shorthand TEXT NOT NULL UNIQUE,
  partner_id INTEGER NOT NULL,
  FOREIGN KEY (partner_id) REFERENCES partners(rowid)
);

CREATE TABLE shorthands_to_categories (
  shorthand TEXT NOT NULL UNIQUE,
  subcategory_id INTEGER NOT NULL,
  FOREIGN KEY (subcategory_id) REFERENCES partners(rowid)

);

-- ==========================================
-- SQLite schema for the real-estate project
-- ==========================================

-- Table 1: Buildings
-- ------------------
-- a_*   : fields extracted directly from ad pages
-- llm_* : fields extracted/enriched using an LLM
-- c_*   : fields from CSV-based enrichment / post-processing

CREATE TABLE IF NOT EXISTS buildings (
  a_id INTEGER PRIMARY KEY AUTOINCREMENT,
  a_url TEXT UNIQUE NOT NULL,
  a_title TEXT,
  a_city TEXT,
  a_postalCode TEXT,
  a_price INTEGER,             -- e.g. 180000
  a_surfaceArea REAL,
  a_description TEXT,
  a_images TEXT,               -- JSON or comma-separated URLs
  a_publicationDate TEXT,      -- MM-DD-YYYY stored as text
  a_dpe TEXT,
  a_ges TEXT,

  llm_residential_office TEXT, -- "residential" or "office"
  llm_nbFlats INTEGER,         -- 0 if not a residential building
  llm_flatSizes TEXT,          -- e.g. "80,120,90,140" or "0"
  llm_other TEXT,              -- perks / amenities as a long string

  c_treated INTEGER DEFAULT 0, -- 0 = not post-processed, 1 = fully treated
  c_INSEE TEXT,
  c_pricePerSqMeter REAL,
  c_taxHab REAL,               -- taxe d'habitation rate (e.g. 0.15)
  c_taxFonc REAL,              -- taxe foncière rate
  c_vacancy REAL,
  c_vacancyCat INTEGER,
  c_revenue REAL,
  c_revenueCat INTEGER,        -- 1–10, 10 = highest revenue
  c_dept TEXT,
  c_region TEXT
);

-- Table 3: Sources (master list of source websites)
-- -------------------------------------------------
-- Only one column: source name.
-- Pre-populated with "Bienici" and "SeLoger".

CREATE TABLE IF NOT EXISTS sources (
  source TEXT PRIMARY KEY
);

INSERT OR IGNORE INTO sources (source) VALUES
  ('Bienici'),
  ('SeLoger');

-- Table 2: Building search links
-- ------------------------------
-- Search URLs used by the scraping engine.
-- One row per search URL, with the associated source.

CREATE TABLE IF NOT EXISTS search_links (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  link TEXT NOT NULL,
  source TEXT NOT NULL,
  FOREIGN KEY (source) REFERENCES sources(source)
);

-- Table 4: Ads cart
-- -----------------
-- List of ad/building IDs that the user has added to the cart.

CREATE TABLE IF NOT EXISTS cart (
  id INTEGER PRIMARY KEY,     -- references buildings.a_id
  FOREIGN KEY (id) REFERENCES buildings(a_id) ON DELETE CASCADE
);

-- Helpful indexes
-- ---------------

CREATE INDEX IF NOT EXISTS idx_buildings_url ON buildings(a_url);
CREATE INDEX IF NOT EXISTS idx_buildings_city ON buildings(a_city);
CREATE INDEX IF NOT EXISTS idx_cart_id ON cart(id);

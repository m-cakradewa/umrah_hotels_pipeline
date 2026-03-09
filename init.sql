-- 1️⃣ Table: hotel_prices
CREATE TABLE IF NOT EXISTS hotel_prices (
    id SERIAL PRIMARY KEY,
    scrape_date TEXT,
    checkin_date TEXT,
    hotel_name TEXT,
    price TEXT,
    stars TEXT,
    rating TEXT,
    link TEXT
);

-- 2️⃣ Table: scrape_runs
CREATE TABLE IF NOT EXISTS scrape_runs (
    id SERIAL PRIMARY KEY,
    run_time TEXT,
    status TEXT,         -- success / failed
    rows_inserted TEXT,
    error_message TEXT
);
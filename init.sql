create schema _bronze;
create schema _silver;
create schema _gold;




-- 1️⃣ Table: hotel_prices
CREATE TABLE IF NOT EXISTS _bronze.hotel_prices (
    id SERIAL PRIMARY KEY,
    scrape_date TEXT,
    checkin_date TEXT,
    hotel_name TEXT,
    price TEXT,
    stars TEXT,
    dist_to_haram TEXT,
    link TEXT
);

CREATE TABLE IF NOT EXISTS _silver.hotel_prices (
    id TEXT,
    scrape_date DATE,
    checkin_date DATE,
    hotel_name TEXT,
    price NUMERIC,
    stars INT,
    dist_to_haram NUMERIC,
    link TEXT
);



-- 2️⃣ Table: scrape_runs
CREATE TABLE IF NOT EXISTS _bronze.scrape_logs (
    id SERIAL PRIMARY KEY,
    run_time TEXT,
    status TEXT,         -- success / failed
    rows_inserted TEXT,
    error_message TEXT
);
{{ config(
    materialized='table'
) }}
SELECT
to_char(checkin_date,'YYYY-MM') as month_text,
ROUND(AVG(price), 2) AS avg_price,
count(id)/count(distinct scrape_date)
as avg_hotels_per_day,
stars
from {{ ref('base_table') }}
GROUP BY month_text, stars
order by month_text desc, stars desc
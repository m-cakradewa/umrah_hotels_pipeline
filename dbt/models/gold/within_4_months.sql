{{ config(
    materialized='view'
) }}
select stars, months_ahead, days_ahead,
round(avg(price),2) as avg_price,
count(id)/count(distinct scrape_date)
as avg_hotels_per_day
from {{ ref('base_table') }}
where days_ahead between 30 and 120
group by stars, months_ahead, days_ahead
order by stars, months_ahead, days_ahead
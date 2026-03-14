{{ config(
    materialized='table',
    schema='silver',
	alias='hotel_prices'
) }}

with ranked as (

select
    trim(hotel_name) || ' - ' ||
    replace(scrape_date,'-','') || ' - ' ||
    replace(checkin_date,'-','') as id,

    cast(scrape_date as date) as scrape_date,
    cast(checkin_date as date) as checkin_date,

    trim(hotel_name) as hotel_name,

    cast(replace(price,',','') as numeric) as price,
    cast(stars as numeric) as stars,
    cast(split_part(dist_to_haram,' ',1) as numeric) as dist_to_haram,

    link,

    row_number() over (
        partition by
            trim(hotel_name),
            scrape_date,
            checkin_date
        order by scrape_date desc
    ) as rn

from {{ source('bronze','hotel_prices') }}
where trim(hotel_name) <> ''

)

select
    id,
    scrape_date,
    checkin_date,
    hotel_name,
    price,
    stars,
    dist_to_haram,
    link
from ranked
where rn = 1



-- -- alter table silver.hotel_prices
-- -- add constraint unique_hotel unique (id);

-- {{config(
-- 	materialized='table',
-- 	schema='silver',
-- 	post_hook=[
-- 		"alter table {{ this }} alter column id type text",
-- 		"alter table {{this }} add constraint unique_hotel unique(id)"
-- 	]
-- )}}

-- -- remove empty rows
-- -- insert into silver.hotel_prices
-- select distinct
-- -- remove duplicates
-- trim(hotel_name) || ' - ' || 
-- replace(scrape_date,'-','') || ' - ' || 
-- replace(checkin_date,'-','') as id,
-- -- change format to date
-- cast(scrape_date as date) as scrape_date,
-- cast(checkin_date as date) as checkin_date,
-- trim(hotel_name) as hotel_name,
-- -- numerical price
-- cast(replace(price,',','') as numeric) as price,
-- -- numerical stars
-- cast(stars as numeric) as stars,
-- -- numerical distance
-- cast(split_part(dist_to_haram, ' ',1) as numeric) as dist_to_haram,
-- link
-- from {{ source('bronze','hotel_prices') }}
-- where trim(hotel_name) <> ''
-- --on conflict (id) do nothing
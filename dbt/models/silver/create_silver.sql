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
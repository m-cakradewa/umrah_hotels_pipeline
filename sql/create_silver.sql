alter table silver.hotel_prices
add constraint unique_hotel unique (id);

alter table silver.hotel_prices
alter column id type text;

-- remove empty rows
insert into silver.hotel_prices
select distinct
-- remove duplicates
trim(hotel_name) || ' - ' || 
replace(scrape_date,'-','') || ' - ' || 
replace(checkin_date,'-','') as id,
-- change format to date
cast(scrape_date as date) as scrape_date,
cast(checkin_date as date) as checkin_date,
trim(hotel_name) as hotel_name,
-- numerical price
cast(replace(price,',','') as numeric) as price,
-- numerical stars
cast(stars as numeric) as stars,
-- numerical distance
cast(split_part(dist_to_haram, ' ',1) as numeric) as dist_to_haram,
link
from bronze.hotel_prices
where trim(hotel_name) <> ''
on conflict (id) do nothing;

select * from silver.hotel_prices;

select round(avg(price),2) as avg_price_2a
from silver.hotel_prices where stars = 5 and ;
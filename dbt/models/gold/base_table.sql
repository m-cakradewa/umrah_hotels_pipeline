{{ config(
    materialized='view'
) }}
select *, 
checkin_date - current_date as days_ahead,
(date_part('year', checkin_date) - date_part('year', current_date)) * 12 +
(date_part('month', checkin_date) - date_part('month', current_date))
as months_ahead
from {{ ref('create_silver') }}

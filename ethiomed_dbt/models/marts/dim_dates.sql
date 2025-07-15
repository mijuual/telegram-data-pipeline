with date_series as (
    select 
        generate_series(
            (select min(date)::date from {{ ref('stg_telegram_messages') }}),
            (select max(date)::date from {{ ref('stg_telegram_messages') }}),
            interval '1 day'
        )::date as calendar_date
)

select
    calendar_date as date,
    extract(year from calendar_date) as year,
    extract(month from calendar_date) as month,
    extract(day from calendar_date) as day,
    extract(week from calendar_date) as week,
    to_char(calendar_date, 'Day') as weekday,
    case 
        when extract(isodow from calendar_date) in (6, 7) then true
        else false
    end as is_weekend
from date_series

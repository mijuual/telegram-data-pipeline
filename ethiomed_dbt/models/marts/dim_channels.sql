with source as (
    select * from {{ ref('stg_telegram_messages') }}
),

dim_channels as (
    select distinct
        channel_name,
        min(date) as first_seen_at,
        max(date) as last_seen_at,
        count(*) as total_messages
    from source
    group by channel_name
)

select 
    row_number() over (order by channel_name) as channel_id,
    channel_name,
    first_seen_at,
    last_seen_at,
    total_messages
from dim_channels

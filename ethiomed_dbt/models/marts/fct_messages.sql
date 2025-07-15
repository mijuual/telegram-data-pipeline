with messages as (
    select * from {{ ref('stg_telegram_messages') }}
),

channels as (
    select * from {{ ref('dim_channels') }}
),

dates as (
    select * from {{ ref('dim_dates') }}
),

fct as (
    select
        message_id as message_id,
        ch.channel_id,
        dt.date as date_id,
        msg.sender_id,
        msg.message,
        length(msg.message) as message_length,
        msg.has_media,
        case when msg.image_path is not null then true else false end as has_image
    from messages msg
    left join channels ch
        on msg.channel_name = ch.channel_name
    left join dates dt
        on date_trunc('day', msg.date) = dt.date
)

select * from fct

{{ config(materialized='view') }}

with source as (
    select *
    from raw.telegram_messages
),

renamed as (
    select
        id as message_id,
        date,
        sender_id,
        channel_name,
        message,
        has_media,
        image_path
    from source
)

select * from renamed

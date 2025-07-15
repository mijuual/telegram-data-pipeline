-- models/staging/stg_image_detections.sql

with raw as (
    select 
        message_id,
        object_class,
        confidence_score
    from {{ source('raw', 'stg_image_detections') }}
)

select * from raw

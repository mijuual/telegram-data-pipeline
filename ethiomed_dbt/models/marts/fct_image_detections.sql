-- models/marts/fct_image_detections.sql

with detections as (
    select 
        message_id,
        object_class,
        confidence_score
    from {{ ref('stg_image_detections') }}
),

messages as (
    select * from {{ ref('fct_messages') }}
)

select 
    d.message_id,
    d.object_class,
    d.confidence_score
from detections d
inner join messages m
    on d.message_id = m.message_id

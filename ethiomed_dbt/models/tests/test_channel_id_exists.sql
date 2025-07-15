-- models/tests/test_channel_id_exists.sql
SELECT
    f.channel_id
FROM {{ ref('fct_messages') }} f
LEFT JOIN {{ ref('dim_channels') }} d
    ON f.channel_id = d.channel_id
WHERE d.channel_id IS NULL

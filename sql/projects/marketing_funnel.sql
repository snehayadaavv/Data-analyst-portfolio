-- Funnel conversion by channel and experiment variant
WITH stage_flags AS (
    SELECT
        user_id,
        channel,
        variant,
        MAX(CASE WHEN event_name = 'visit' THEN 1 ELSE 0 END) AS did_visit,
        MAX(CASE WHEN event_name = 'signup' THEN 1 ELSE 0 END) AS did_signup,
        MAX(CASE WHEN event_name = 'activation' THEN 1 ELSE 0 END) AS did_activate
    FROM events
    GROUP BY user_id, channel, variant
)
SELECT
    channel,
    variant,
    SUM(did_visit) AS visits,
    SUM(did_signup) AS signups,
    SUM(did_activate) AS activations,
    CAST(SUM(did_signup) * 100.0 / NULLIF(SUM(did_visit), 0) AS DECIMAL(10,2)) AS visit_to_signup_pct,
    CAST(SUM(did_activate) * 100.0 / NULLIF(SUM(did_signup), 0) AS DECIMAL(10,2)) AS signup_to_activation_pct
FROM stage_flags
GROUP BY channel, variant
ORDER BY channel, variant;


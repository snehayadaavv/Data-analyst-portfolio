-- Monthly churn rate by month
WITH churn_base AS (
    SELECT
        DATEFROMPARTS(YEAR(cancel_date), MONTH(cancel_date), 1) AS churn_month,
        COUNT(*) AS churned_customers
    FROM subscriptions
    WHERE status = 'churned'
      AND cancel_date IS NOT NULL
    GROUP BY DATEFROMPARTS(YEAR(cancel_date), MONTH(cancel_date), 1)
),
active_base AS (
    SELECT
        DATEFROMPARTS(YEAR(month), MONTH(month), 1) AS churn_month,
        COUNT(DISTINCT customer_id) AS active_customers
    FROM usage
    GROUP BY DATEFROMPARTS(YEAR(month), MONTH(month), 1)
)
SELECT
    a.churn_month,
    a.active_customers,
    COALESCE(c.churned_customers, 0) AS churned_customers,
    CAST(COALESCE(c.churned_customers, 0) * 100.0 / NULLIF(a.active_customers, 0) AS DECIMAL(10,2)) AS churn_rate_pct
FROM active_base a
LEFT JOIN churn_base c
    ON a.churn_month = c.churn_month
ORDER BY a.churn_month;


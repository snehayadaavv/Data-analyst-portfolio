-- Revenue, gross margin, and target variance by month and region
WITH sales_summary AS (
    SELECT
        DATEFROMPARTS(YEAR(order_date), MONTH(order_date), 1) AS sales_month,
        region,
        SUM(revenue) AS total_revenue,
        SUM(revenue - cost) AS gross_margin
    FROM orders
    GROUP BY DATEFROMPARTS(YEAR(order_date), MONTH(order_date), 1), region
)
SELECT
    s.sales_month,
    s.region,
    s.total_revenue,
    s.gross_margin,
    t.revenue_target,
    s.total_revenue - t.revenue_target AS variance_to_target
FROM sales_summary s
LEFT JOIN targets t
    ON s.sales_month = t.month
   AND s.region = t.region
ORDER BY s.sales_month, s.region;


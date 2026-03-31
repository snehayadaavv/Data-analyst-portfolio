# Sales & Revenue Performance

## Business Question
Which regions, products, and channels are driving growth, and where are we underperforming against target?

## Project Goal
- Track month-over-month and year-over-year revenue.
- Compare actual sales to targets by region and category.
- Surface margin pressure and opportunity segments.

## Dataset (example schema)
- `orders(order_id, order_date, region, channel, product_category, revenue, cost)`
- `targets(month, region, revenue_target)`

## Workflow
1. Build monthly sales summary in SQL.
2. Compute variance to target and gross margin.
3. Visualize trends and decomposition in dashboard.

## Key Insights (sample)
- East region exceeded target by +12% in Q3, led by online channel.
- Accessories category has high volume but low margin.
- Enterprise channel has stable margin and highest repeat purchase rate.

## Recommendations
- Reallocate budget toward top-performing East campaigns.
- Bundle low-margin accessories with high-margin core products.
- Expand enterprise account retention playbook.

## Files
- `sales_query.sql` - monthly performance and margin query
- `python/projects/sales_performance.py` - variance diagnostics and segment ranking
- `generate_sample_data.py` - creates sample CSV datasets under `data/raw/`

## Make it work (sample data + Python)
1. Create sample CSVs:
   - `python generate_sample_data.py`
2. Run the sales analysis:
   - `python ..\..\python\projects\sales_performance.py`

## Sample data location
- `data/raw/orders.csv`
- `data/raw/targets.csv`


# Executive Overview Dashboard

## Audience
Leadership team (CEO, COO, Head of Growth)

## Purpose
Provide a one-page snapshot of business health across revenue, customer growth, churn, and satisfaction.

## Core KPIs
- Total Revenue
- Monthly Recurring Revenue (MRR)
- Active Customers
- Churn Rate (%)
- Net Promoter Score (NPS)

## Recommended Visuals
- KPI cards for each top metric
- Monthly revenue trend line
- New vs churned customers clustered column chart
- Region performance map or bar chart
- Churn by plan type stacked bar chart

## Filters/Slicers
- Date (month/quarter/year)
- Region
- Plan Type

## Data Tables Needed
- `fact_revenue`
- `fact_customers`
- `fact_churn`
- `dim_date`
- `dim_region`
- `dim_plan`

## Build Checklist
- [ ] Import data tables and define relationships
- [ ] Create DAX measures for all KPIs
- [ ] Add trend and segment visuals
- [ ] Format with consistent theme/colors
- [ ] Add page tooltip for KPI definitions
- [ ] Export screenshot to `screenshots/`


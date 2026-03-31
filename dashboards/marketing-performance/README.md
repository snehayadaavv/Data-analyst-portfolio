# Marketing Performance Dashboard

## Audience
Marketing manager, growth analyst, performance team

## Purpose
Measure campaign efficiency and conversion outcomes across channels.

## Core KPIs
- Spend
- Impressions
- Click-Through Rate (CTR)
- Cost per Acquisition (CAC)
- Conversion Rate
- Return on Ad Spend (ROAS)

## Recommended Visuals
- Channel performance table (spend, conversions, CAC, ROAS)
- Spend vs conversion scatter plot
- Funnel chart (impression -> click -> signup -> purchase)
- Campaign trend line by week
- Top and bottom campaign bar chart

## Filters/Slicers
- Date
- Channel
- Campaign
- Region

## Data Tables Needed
- `fact_campaign_daily`
- `fact_funnel_events`
- `dim_campaign`
- `dim_channel`
- `dim_date`

## Build Checklist
- [ ] Define CAC and ROAS measures
- [ ] Create channel comparison page
- [ ] Add funnel conversion page
- [ ] Include campaign-level drill-through
- [ ] Add screenshot export to `screenshots/`


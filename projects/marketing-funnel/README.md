# Marketing Funnel & A/B Testing

## Business Question
Where are users dropping off in the acquisition funnel, and did the new landing page improve conversion?

## Project Goal
- Build channel-level funnel conversion metrics.
- Evaluate A/B test impact on signup conversion.
- Recommend rollout decision based on data.

## Dataset (example schema)
- `events(user_id, event_time, channel, event_name, variant)`
- `campaign_spend(date, channel, spend)`

## Workflow
1. Build funnel stages in SQL (`visit -> signup -> activation`).
2. Calculate conversion rates by channel and variant.
3. Validate test significance and practical impact.

## Key Insights (sample)
- Biggest drop-off occurs from visit to signup on paid social traffic.
- Variant B improved signup rate by +3.1 percentage points.
- Search channel remains the most efficient CAC-to-LTV segment.

## Recommendations
- Roll out Variant B to 100% after QA sign-off.
- Redesign paid social landing page and message match.
- Shift spend toward channels with stronger activation conversion.

## Files
- `funnel_query.sql` - funnel stage metrics by channel and variant
- `python/projects/marketing_funnel_ab_test.py` - funnel stage metrics + conversion lift
- `generate_sample_data.py` - creates sample CSV datasets under `data/raw/`

## Make it work (sample data + Python)
1. Create sample CSVs:
   - `python generate_sample_data.py`
2. Run funnel metrics:
   - `python ..\..\python\projects\marketing_funnel_ab_test.py`

## Sample data location
- `data/raw/events.csv`


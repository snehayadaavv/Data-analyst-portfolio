# Customer Churn Diagnosis

## Business Question
Why are customers churning, and which customer segments should we prioritize to reduce monthly churn rate?

## Project Goal
- Measure churn trend over time.
- Identify top churn drivers.
- Recommend actions for retention and win-back campaigns.

## Dataset (example schema)
- `customers(customer_id, signup_date, plan_type, region, monthly_fee)`
- `subscriptions(customer_id, status, cancel_date, tenure_months)`
- `usage(customer_id, month, sessions, avg_session_minutes, support_tickets)`

## Workflow
1. Build monthly churn base table in SQL.
2. Engineer behavior features in Python.
3. Rank feature importance and profile high-risk users.
4. Create a one-page dashboard for stakeholders.

## Key Insights (sample)
- Customers with `tenure < 3 months` and `low session activity` are 2.4x more likely to churn.
- Churn is highest in Basic plan users with more than 2 support tickets/month.
- Region West showed a sudden churn spike after a pricing update.

## Recommendations
- Launch a 90-day onboarding journey for new customers.
- Trigger proactive support outreach for low-engagement accounts.
- Run a pricing communication test for affected regions.

## Files
- `churn_query.sql` - churn and retention computation
- `python/projects/customer_churn.py` - feature engineering and risk scoring
- `generate_sample_data.py` - creates sample CSV datasets under `data/raw/`

## Make it work (sample data + Python)
1. Create sample CSVs:
   - `python generate_sample_data.py`
2. Run the churn analysis:
   - `python ..\..\python\projects\customer_churn.py`

## Sample data location
- `data/raw/customers.csv`
- `data/raw/subscriptions.csv`
- `data/raw/usage.csv`


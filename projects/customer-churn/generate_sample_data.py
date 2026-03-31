from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class Config:
    seed: int = 42
    n_customers: int = 30


def month_start(d: datetime) -> datetime:
    return datetime(d.year, d.month, 1)


def months_between(a: datetime, b: datetime) -> int:
    # Whole-month difference using year/month parts only.
    return (b.year - a.year) * 12 + (b.month - a.month)


def main() -> None:
    cfg = Config()
    random.seed(cfg.seed)

    repo_root = Path(__file__).resolve().parents[2]
    raw_dir = repo_root / "projects" / "customer-churn" / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    regions = ["North", "South", "East", "West"]
    plan_types = ["Basic", "Plus", "Premium"]

    # Generate customers.
    start_signup = datetime(2025, 1, 1)
    signup_spread_months = 12

    customers = []
    for cid in range(1001, 1001 + cfg.n_customers):
        signup_offset = random.randint(0, signup_spread_months)
        signup_date = datetime(start_signup.year, start_signup.month, 1) + pd.DateOffset(months=signup_offset)
        signup_date = signup_date.to_pydatetime()

        region = random.choice(regions)
        plan_type = random.choices(plan_types, weights=[0.45, 0.35, 0.2])[0]

        monthly_fee = {
            "Basic": random.randint(30, 45),
            "Plus": random.randint(55, 75),
            "Premium": random.randint(90, 120),
        }[plan_type]

        customers.append(
            {
                "customer_id": cid,
                "signup_date": signup_date.date().isoformat(),
                "plan_type": plan_type,
                "region": region,
                "monthly_fee": monthly_fee,
            }
        )

    customers_df = pd.DataFrame(customers)

    # Decide churn status and cancellation dates.
    # Higher churn likelihood for Basic plan and for one region to create signal.
    base_churn_rate = 0.28
    region_churn_boost = {"North": 0.08, "South": 0.0, "East": 0.03, "West": 0.05}
    plan_churn_boost = {"Basic": 0.14, "Plus": 0.06, "Premium": 0.0}

    # Reference end of dataset window.
    dataset_end = datetime(2026, 4, 1)
    churn_records = []
    for _, row in customers_df.iterrows():
        cid = int(row["customer_id"])
        plan_type = row["plan_type"]
        region = row["region"]

        churn_prob = min(0.7, base_churn_rate + plan_churn_boost[plan_type] + region_churn_boost[region])
        is_churned = random.random() < churn_prob

        if is_churned:
            # Cancel between 2025-06 and 2026-03 (so there are some months of usage).
            cancel_month_offset = random.randint(6, 15)
            cancel_date = datetime(2025, 1, 1) + pd.DateOffset(months=cancel_month_offset)
            cancel_date = cancel_date.to_pydatetime()
            status = "churned"
        else:
            cancel_date = None
            status = "active"

        churn_records.append(
            {
                "customer_id": cid,
                "status": status,
                "cancel_date": (cancel_date.date().isoformat() if cancel_date else None),
            }
        )

    subs_df = pd.DataFrame(churn_records)

    # Generate monthly usage rows for each customer up to cancel month (or dataset end month).
    usage_rows = []
    months = pd.date_range("2026-01-01", "2026-04-01", freq="MS").to_pydatetime().tolist()

    for _, crow in customers_df.iterrows():
        cid = int(crow["customer_id"])
        plan_type = crow["plan_type"]
        region = crow["region"]
        signup_date = datetime.fromisoformat(crow["signup_date"])

        sub_row = subs_df[subs_df["customer_id"] == cid].iloc[0]
        cancel_date_str = sub_row["cancel_date"]
        cancel_dt = datetime.fromisoformat(cancel_date_str) if pd.notna(cancel_date_str) else None

        for m in months:
            if cancel_dt is not None and m > month_start(cancel_dt):
                # No usage after cancellation in this sample window.
                continue

            tenure_m = max(0, months_between(signup_date, m))

            # Base sessions influenced by plan and tenure.
            plan_sessions_factor = {"Basic": 0.85, "Plus": 1.0, "Premium": 1.25}[plan_type]
            region_sessions_boost = {"North": 0.95, "South": 1.0, "East": 1.05, "West": 0.98}[region]

            # Newer customers get slightly more engagement; churned customers tend to drop.
            churned = sub_row["status"] == "churned"
            engagement = 1.0
            if tenure_m < 3:
                engagement += 0.18
            if churned and tenure_m > 6:
                engagement -= 0.15

            mean_sessions = 10 * plan_sessions_factor * region_sessions_boost * engagement
            sessions = max(0, int(random.gauss(mean_sessions, 3)))

            avg_session_minutes = max(2, int(random.gauss(18, 6) + (tenure_m - 6) * -0.3))
            # Support tickets increase for Basic plan and for churned customers nearing cancellation.
            base_tickets = {"Basic": 2.4, "Plus": 1.6, "Premium": 1.0}[plan_type]
            if churned and cancel_dt is not None:
                months_to_cancel = max(0, months_between(m, month_start(cancel_dt)))
                # More tickets closer to churn.
                base_tickets += max(0, 2.0 - 0.6 * months_to_cancel)
            support_tickets = max(0, int(random.gauss(base_tickets, 1.2)))

            usage_rows.append(
                {
                    "customer_id": cid,
                    "month": m.date().isoformat(),
                    "sessions": sessions,
                    "avg_session_minutes": avg_session_minutes,
                    "support_tickets": support_tickets,
                }
            )

    usage_df = pd.DataFrame(usage_rows)

    customers_df.to_csv(raw_dir / "customers.csv", index=False)
    subs_df.to_csv(raw_dir / "subscriptions.csv", index=False)
    usage_df.to_csv(raw_dir / "usage.csv", index=False)

    print("Sample churn data created:")
    print(f"- {raw_dir / 'customers.csv'} ({len(customers_df)} rows)")
    print(f"- {raw_dir / 'subscriptions.csv'} ({len(subs_df)} rows)")
    print(f"- {raw_dir / 'usage.csv'} ({len(usage_df)} rows)")


if __name__ == "__main__":
    main()


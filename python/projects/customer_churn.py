from __future__ import annotations

from pathlib import Path

import pandas as pd


def build_risk_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Simple heuristic risk score for portfolio demo purposes.
    Expected columns: tenure_months, sessions, support_tickets, churned
    """
    out = df.copy()
    out["risk_score"] = (
        (out["tenure_months"] < 3).astype(int) * 40
        + (out["sessions"] < 5).astype(int) * 35
        + (out["support_tickets"] > 2).astype(int) * 25
    )
    return out.sort_values("risk_score", ascending=False)


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[2]
    raw_dir = repo_root / "projects" / "customer-churn" / "data" / "raw"

    customers_path = raw_dir / "customers.csv"
    subscriptions_path = raw_dir / "subscriptions.csv"
    usage_path = raw_dir / "usage.csv"

    missing = [p for p in [customers_path, subscriptions_path, usage_path] if not p.exists()]
    if missing:
        raise SystemExit(
            "Missing sample data CSV(s). Run:\n"
            "  python projects/customer-churn/generate_sample_data.py\n"
            f"Missing: {', '.join(str(p) for p in missing)}"
        )

    customers = pd.read_csv(customers_path)
    subscriptions = pd.read_csv(subscriptions_path)
    usage = pd.read_csv(usage_path)

    # Parse dates.
    customers["signup_date"] = pd.to_datetime(customers["signup_date"])
    subscriptions["cancel_date"] = pd.to_datetime(subscriptions["cancel_date"], errors="coerce")
    usage["month"] = pd.to_datetime(usage["month"])

    # Build per-customer features from the last 3 months of observed usage.
    last_month = usage.groupby("customer_id")["month"].max().rename("last_month").reset_index()
    merged = usage.merge(last_month, on="customer_id", how="left")
    # Select the last 3 observed months per customer.
    merged = merged[merged["month"] >= merged["last_month"] - pd.DateOffset(months=2)]

    agg = (
        merged.groupby("customer_id", as_index=False)
        .agg(
            sessions=("sessions", "sum"),
            support_tickets=("support_tickets", "sum"),
        )
    )

    # Tenure in whole months between signup and last observed usage month.
    last_month_dates = pd.to_datetime(last_month.set_index("customer_id")["last_month"])
    # Only compute tenure for customers that appear in usage features.
    signup_dates = pd.to_datetime(customers.set_index("customer_id")["signup_date"]).reindex(last_month_dates.index)
    tenure_months = (
        (last_month_dates.dt.year - signup_dates.dt.year) * 12
        + (last_month_dates.dt.month - signup_dates.dt.month)
    ).astype(int).rename("tenure_months").reset_index()

    churned = (
        subscriptions.assign(churned=lambda d: (d["status"] == "churned").astype(int))[
            ["customer_id", "churned"]
        ]
    )

    features = agg.merge(tenure_months, on="customer_id").merge(churned, on="customer_id")

    risk_table = build_risk_table(
        features.rename(columns={"sessions": "sessions", "support_tickets": "support_tickets"})
    )
    # Save a simple ranked output for recruiters.
    out_dir = repo_root / "projects" / "customer-churn" / "data" / "processed"
    out_dir.mkdir(parents=True, exist_ok=True)
    risk_table.to_csv(out_dir / "risk_table.csv", index=False)

    print(risk_table[["customer_id", "tenure_months", "sessions", "support_tickets", "churned", "risk_score"]].head(10))


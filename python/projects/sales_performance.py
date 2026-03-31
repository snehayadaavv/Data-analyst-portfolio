from __future__ import annotations

from pathlib import Path

import pandas as pd


def variance_report(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["variance"] = out["total_revenue"] - out["revenue_target"]
    out["variance_pct"] = out["variance"] / out["revenue_target"].replace(0, pd.NA)
    return out.sort_values(["sales_month", "variance"], ascending=[True, False])


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[2]
    raw_dir = repo_root / "projects" / "sales-performance" / "data" / "raw"

    orders_path = raw_dir / "orders.csv"
    targets_path = raw_dir / "targets.csv"

    missing = [p for p in [orders_path, targets_path] if not p.exists()]
    if missing:
        raise SystemExit(
            "Missing sample data CSV(s). Run:\n"
            "  python projects/sales-performance/generate_sample_data.py\n"
            f"Missing: {', '.join(str(p) for p in missing)}"
        )

    orders = pd.read_csv(orders_path)
    targets = pd.read_csv(targets_path)

    orders["order_date"] = pd.to_datetime(orders["order_date"])
    orders["sales_month"] = orders["order_date"].values.astype("datetime64[M]")

    orders_agg = (
        orders.assign(gross_margin=orders["revenue"] - orders["cost"])
        .groupby(["sales_month", "region"], as_index=False)
        .agg(total_revenue=("revenue", "sum"), gross_margin=("gross_margin", "sum"))
    )

    targets["month"] = pd.to_datetime(targets["month"])
    targets = targets.rename(columns={"month": "sales_month"})

    merged = orders_agg.merge(targets, on=["sales_month", "region"], how="left")
    merged["revenue_target"] = merged["revenue_target"].fillna(0)

    report = variance_report(merged)

    out_dir = repo_root / "projects" / "sales-performance" / "data" / "processed"
    out_dir.mkdir(parents=True, exist_ok=True)
    report.to_csv(out_dir / "variance_report.csv", index=False)

    print(report.head(10))


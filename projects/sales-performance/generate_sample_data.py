from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class Config:
    seed: int = 7


def main() -> None:
    cfg = Config()
    random.seed(cfg.seed)

    repo_root = Path(__file__).resolve().parents[2]
    raw_dir = repo_root / "projects" / "sales-performance" / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    regions = ["East", "West", "North"]
    channels = ["Online", "Retail", "Partner"]
    product_categories = ["Core", "Accessories", "Services"]

    months = pd.date_range("2026-01-01", "2026-06-01", freq="MS").to_pydatetime().tolist()

    # Targets by month and region (simple increasing trend + noise).
    targets = []
    for r in regions:
        base = random.randint(250000, 420000)
        for m in months:
            month_idx = (m.year - months[0].year) * 12 + (m.month - months[0].month)
            trend = 1.0 + 0.03 * month_idx
            target = int(base * trend + random.randint(-25000, 25000))
            targets.append({"month": m.date().isoformat(), "region": r, "revenue_target": target})
    targets_df = pd.DataFrame(targets)

    # Orders: generate revenue and cost with category + channel effects.
    orders = []
    order_id = 50001

    for m in months:
        for r in regions:
            for _ in range(10):  # small but sufficient sample
                channel = random.choices(channels, weights=[0.45, 0.35, 0.20])[0]
                category = random.choices(product_categories, weights=[0.55, 0.25, 0.20])[0]

                # Pricing + margin differences.
                revenue_base = {
                    "Core": random.randint(18000, 32000),
                    "Accessories": random.randint(6000, 14000),
                    "Services": random.randint(12000, 21000),
                }[category]

                channel_multiplier = {"Online": 1.06, "Retail": 0.96, "Partner": 1.02}[channel]
                region_multiplier = {"East": 1.05, "West": 0.97, "North": 1.00}[r]

                # Add seasonal-ish noise.
                month_idx = (m.year - months[0].year) * 12 + (m.month - months[0].month)
                seasonal = 1.0 + 0.02 * (month_idx % 3)

                revenue = int(revenue_base * channel_multiplier * region_multiplier * seasonal)
                cost_ratio = {"Core": 0.62, "Accessories": 0.76, "Services": 0.55}[category]
                cost = int(revenue * cost_ratio + random.randint(-800, 1200))

                orders.append(
                    {
                        "order_id": order_id,
                        "order_date": datetime(m.year, m.month, random.randint(1, 28)).date().isoformat(),
                        "region": r,
                        "channel": channel,
                        "product_category": category,
                        "revenue": revenue,
                        "cost": cost,
                    }
                )
                order_id += 1

    orders_df = pd.DataFrame(orders)

    orders_df.to_csv(raw_dir / "orders.csv", index=False)
    targets_df.to_csv(raw_dir / "targets.csv", index=False)

    print("Sample sales data created:")
    print(f"- {raw_dir / 'orders.csv'} ({len(orders_df)} rows)")
    print(f"- {raw_dir / 'targets.csv'} ({len(targets_df)} rows)")


if __name__ == "__main__":
    main()


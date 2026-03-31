from __future__ import annotations

from pathlib import Path

import pandas as pd


def funnel_metrics(events: pd.DataFrame) -> pd.DataFrame:
    # Convert event stream into stage flags per user/channel/variant.
    stage = (
        events.groupby(["user_id", "channel", "variant"], as_index=False)
        .agg(
            did_visit=("event_name", lambda s: int((s == "visit").any())),
            did_signup=("event_name", lambda s: int((s == "signup").any())),
            did_activate=("event_name", lambda s: int((s == "activation").any())),
        )
    )

    grouped = (
        stage.groupby(["channel", "variant"], as_index=False)
        .agg(visits=("did_visit", "sum"), signups=("did_signup", "sum"), activations=("did_activate", "sum"))
    )
    grouped["visit_to_signup_pct"] = (grouped["signups"] * 100.0 / grouped["visits"].replace(0, pd.NA)).round(2)
    grouped["signup_to_activation_pct"] = (
        grouped["activations"] * 100.0 / grouped["signups"].replace(0, pd.NA)
    ).round(2)
    grouped["visit_to_activation_pct"] = (
        grouped["activations"] * 100.0 / grouped["visits"].replace(0, pd.NA)
    ).round(2)
    return grouped.sort_values(["channel", "variant"])


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[2]
    raw_dir = repo_root / "projects" / "marketing-funnel" / "data" / "raw"

    events_path = raw_dir / "events.csv"
    if not events_path.exists():
        raise SystemExit(
            "Missing sample data CSV. Run:\n"
            "  python projects/marketing-funnel/generate_sample_data.py\n"
            f"Missing: {events_path}"
        )

    events = pd.read_csv(events_path)

    # Basic cleanup for consistent types.
    if "event_time" in events.columns:
        events["event_time"] = pd.to_datetime(events["event_time"], errors="coerce")

    metrics = funnel_metrics(events)

    out_dir = repo_root / "projects" / "marketing-funnel" / "data" / "processed"
    out_dir.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(out_dir / "funnel_metrics.csv", index=False)

    print(metrics.head(20))


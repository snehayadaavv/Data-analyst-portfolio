from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class Config:
    seed: int = 99
    n_users: int = 120


def random_datetime_between(start: datetime, end: datetime) -> datetime:
    delta = end - start
    seconds = int(delta.total_seconds())
    return start + timedelta(seconds=random.randint(0, max(1, seconds)))


def main() -> None:
    cfg = Config()
    random.seed(cfg.seed)

    repo_root = Path(__file__).resolve().parents[2]
    raw_dir = repo_root / "projects" / "marketing-funnel" / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    channels = ["Paid Social", "Search", "Email"]
    variants = ["A", "B"]

    start = datetime(2026, 1, 1)
    end = datetime(2026, 4, 30, 23, 59, 59)

    # Variant effect: B slightly better conversion.
    # Also channel effects for visit->signup and signup->activation.
    visit_to_signup = {
        "Paid Social": {"A": 0.18, "B": 0.23},
        "Search": {"A": 0.26, "B": 0.29},
        "Email": {"A": 0.32, "B": 0.34},
    }
    signup_to_activation = {
        "Paid Social": {"A": 0.28, "B": 0.33},
        "Search": {"A": 0.35, "B": 0.37},
        "Email": {"A": 0.42, "B": 0.44},
    }

    events = []
    user_start = 20001
    for i in range(cfg.n_users):
        user_id = user_start + i
        variant = random.choice(variants)
        channel = random.choices(channels, weights=[0.5, 0.35, 0.15])[0]

        # Always create a visit.
        visit_time = random_datetime_between(start, end)
        events.append(
            {
                "user_id": user_id,
                "event_time": visit_time.isoformat(),
                "channel": channel,
                "event_name": "visit",
                "variant": variant,
            }
        )

        # Signup conditional on visit.
        if random.random() < visit_to_signup[channel][variant]:
            signup_time = visit_time + timedelta(minutes=random.randint(5, 180))
            events.append(
                {
                    "user_id": user_id,
                    "event_time": signup_time.isoformat(),
                    "channel": channel,
                    "event_name": "signup",
                    "variant": variant,
                }
            )

            # Activation conditional on signup.
            if random.random() < signup_to_activation[channel][variant]:
                activation_time = signup_time + timedelta(hours=random.randint(1, 72))
                events.append(
                    {
                        "user_id": user_id,
                        "event_time": activation_time.isoformat(),
                        "channel": channel,
                        "event_name": "activation",
                        "variant": variant,
                    }
                )

    events_df = pd.DataFrame(events).sort_values(["user_id", "event_time"])
    events_df.to_csv(raw_dir / "events.csv", index=False)

    print("Sample marketing funnel data created:")
    print(f"- {raw_dir / 'events.csv'} ({len(events_df)} rows, {events_df.user_id.nunique()} users)")


if __name__ == "__main__":
    main()


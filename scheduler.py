"""
Scheduler — runs price checks at a configurable interval.
Usage: python scheduler.py
"""

import schedule
import time
import json
from tracker import check_prices


def load_interval() -> int:
    with open("config.json", "r") as f:
        return json.load(f).get("check_interval_minutes", 60)


if __name__ == "__main__":
    interval = load_interval()
    print(f"⏱  Scheduler started — checking every {interval} minute(s).")
    print("   Press Ctrl+C to stop.\n")

    # Run once immediately on start
    check_prices()

    schedule.every(interval).minutes.do(check_prices)

    while True:
        schedule.run_pending()
        time.sleep(30)

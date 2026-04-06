"""
ml-price-tracker — MercadoLibre price tracker with email alerts
"""

import json
import os
import requests
from datetime import datetime
from emailer import send_alert


HISTORY_FILE = "price_history.json"
CONFIG_FILE = "config.json"


def load_config() -> dict:
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def load_history() -> dict:
    if not os.path.exists(HISTORY_FILE):
        return {}
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)


def save_history(history: dict):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def fetch_item(item_id: str) -> dict | None:
    """Fetch item data from MercadoLibre public API."""
    url = f"https://api.mercadolibre.com/items/{item_id}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        return {
            "id": data["id"],
            "title": data["title"],
            "price": data["price"],
            "currency": data["currency_id"],
            "url": data["permalink"],
            "condition": data.get("condition", "unknown"),
        }
    except requests.RequestException as e:
        print(f"  [ERROR] Could not fetch {item_id}: {e}")
        return None


def check_prices():
    config = load_config()
    history = load_history()
    now = datetime.now().isoformat(timespec="seconds")

    print(f"\n{'='*50}")
    print(f"  Run: {now}")
    print(f"{'='*50}")

    for entry in config["items"]:
        item_id = entry["id"]
        threshold = entry.get("alert_below")

        print(f"\n→ Checking {item_id}...")
        item = fetch_item(item_id)
        if not item:
            continue

        price = item["price"]
        title = item["title"]
        currency = item["currency"]
        url = item["url"]

        # Update history
        if item_id not in history:
            history[item_id] = {"title": title, "records": []}

        records = history[item_id]["records"]
        records.append({"price": price, "timestamp": now})
        history[item_id]["title"] = title

        # Compute previous price
        prev_price = records[-2]["price"] if len(records) >= 2 else None

        print(f"  Title    : {title[:60]}")
        print(f"  Price    : {currency} {price:,.2f}")
        if prev_price:
            diff = price - prev_price
            sign = "+" if diff >= 0 else ""
            print(f"  Change   : {sign}{diff:,.2f} vs last check")
        if threshold:
            print(f"  Alert if : below {currency} {threshold:,.2f}")

        # Alert conditions
        should_alert = False
        alert_reason = ""

        if threshold and price < threshold:
            should_alert = True
            alert_reason = f"Price dropped below your threshold of {currency} {threshold:,.2f}"

        if prev_price and price < prev_price:
            should_alert = True
            drop_pct = (prev_price - price) / prev_price * 100
            alert_reason += f"\nPrice fell {drop_pct:.1f}% since last check ({currency} {prev_price:,.2f} → {currency} {price:,.2f})"

        if should_alert:
            print(f"  🔔 ALERT triggered!")
            send_alert(
                to=config["email"]["to"],
                title=title,
                price=price,
                currency=currency,
                url=url,
                reason=alert_reason.strip(),
            )

    save_history(history)
    print(f"\n✓ Done. History saved to {HISTORY_FILE}\n")


if __name__ == "__main__":
    check_prices()

"""
CLI helper to manage tracked items without editing config.json manually.

Usage:
  python cli.py add MLA123456789 --below 50000
  python cli.py remove MLA123456789
  python cli.py list
  python cli.py history MLA123456789
"""

import argparse
import json
import os
import sys


CONFIG_FILE = "config.json"
HISTORY_FILE = "price_history.json"


def load_config():
    with open(CONFIG_FILE) as f:
        return json.load(f)

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)


def cmd_add(args):
    cfg = load_config()
    ids = [i["id"] for i in cfg["items"]]
    if args.item_id in ids:
        print(f"⚠  {args.item_id} is already tracked.")
        return
    entry = {"id": args.item_id, "alert_below": args.below}
    cfg["items"].append(entry)
    save_config(cfg)
    threshold = f"ARS {args.below:,.2f}" if args.below else "none"
    print(f"✓ Added {args.item_id} (alert threshold: {threshold})")


def cmd_remove(args):
    cfg = load_config()
    before = len(cfg["items"])
    cfg["items"] = [i for i in cfg["items"] if i["id"] != args.item_id]
    if len(cfg["items"]) == before:
        print(f"⚠  {args.item_id} not found in config.")
    else:
        save_config(cfg)
        print(f"✓ Removed {args.item_id}")


def cmd_list(args):
    cfg = load_config()
    history = json.load(open(HISTORY_FILE)) if os.path.exists(HISTORY_FILE) else {}

    if not cfg["items"]:
        print("No items tracked yet. Use: python cli.py add <ITEM_ID>")
        return

    print(f"\n{'ID':<20} {'Alert Below':>14}  {'Last Price':>14}  Title")
    print("-" * 80)
    for item in cfg["items"]:
        iid = item["id"]
        threshold = f"{item['alert_below']:,.0f}" if item["alert_below"] else "—"
        h = history.get(iid, {})
        records = h.get("records", [])
        last_price = f"{records[-1]['price']:,.0f}" if records else "—"
        title = h.get("title", "—")[:35]
        print(f"{iid:<20} {threshold:>14}  {last_price:>14}  {title}")
    print()


def cmd_history(args):
    if not os.path.exists(HISTORY_FILE):
        print("No history yet. Run tracker.py first.")
        return
    with open(HISTORY_FILE) as f:
        history = json.load(f)
    item = history.get(args.item_id)
    if not item:
        print(f"No history for {args.item_id}")
        return
    print(f"\n{item['title']}")
    print(f"{'Timestamp':<25} {'Price':>12}")
    print("-" * 40)
    for r in item["records"][-20:]:  # last 20
        print(f"{r['timestamp']:<25} {r['price']:>12,.2f}")
    print()


def main():
    parser = argparse.ArgumentParser(description="ml-price-tracker CLI")
    sub = parser.add_subparsers(dest="command")

    p_add = sub.add_parser("add", help="Track a new item")
    p_add.add_argument("item_id", help="MercadoLibre item ID (e.g. MLA123456789)")
    p_add.add_argument("--below", type=float, default=None, help="Alert if price drops below this value")

    p_rem = sub.add_parser("remove", help="Stop tracking an item")
    p_rem.add_argument("item_id")

    sub.add_parser("list", help="List all tracked items")

    p_hist = sub.add_parser("history", help="Show price history for an item")
    p_hist.add_argument("item_id")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    {"add": cmd_add, "remove": cmd_remove, "list": cmd_list, "history": cmd_history}[args.command](args)


if __name__ == "__main__":
    main()

# 🛒 ml-price-tracker

Track MercadoLibre product prices and get **email alerts** when they drop.

Built with Python + MercadoLibre public API. No API key required.

---

## Features

- ✅ Tracks any MercadoLibre item by ID
- ✅ Stores full price history locally (JSON)
- ✅ Email alerts when price drops or falls below a threshold
- ✅ Runs on a schedule (configurable interval)
- ✅ CLI to add/remove/list items without editing files

---

## Setup

```bash
git clone https://github.com/Lazaro549/ml-price-tracker
cd ml-price-tracker
pip install -r requirements.txt
```

### Configure

Edit `config.json`:

```json
{
  "check_interval_minutes": 60,
  "email": {
    "from": "tu_email@gmail.com",
    "app_password": "xxxx xxxx xxxx xxxx",
    "to": "destino@gmail.com"
  },
  "items": [
    { "id": "MLA123456789", "alert_below": 50000 }
  ]
}
```

> **Gmail App Password**: Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords) and generate one. Do NOT use your main password.

### Find a MercadoLibre Item ID

Open any product page — the ID is in the URL:
```
https://www.mercadolibre.com.ar/...MLA-123456789-...
→ item ID: MLA123456789
```

---

## Usage

### CLI (recommended)

```bash
# Add an item to track
python cli.py add MLA123456789 --below 50000

# List all tracked items with last prices
python cli.py list

# View price history for an item
python cli.py history MLA123456789

# Stop tracking an item
python cli.py remove MLA123456789
```

### Run once

```bash
python tracker.py
```

### Run on schedule

```bash
python scheduler.py
```

Checks every N minutes (set in `config.json`). Keep it running in a terminal or use `nohup`/`screen`.

---

## Alert Logic

An email is sent when:
- The current price is **below your configured threshold** (`alert_below`)
- The price **dropped since the last check** (any amount)

---

## Project Structure

```
ml-price-tracker/
├── tracker.py        # Core logic: fetch → compare → alert
├── emailer.py        # Gmail SMTP email sender
├── scheduler.py      # Periodic runner
├── cli.py            # Command-line interface
├── config.json       # Your settings & tracked items
├── price_history.json  # Auto-generated, stores all records
└── requirements.txt
```

---

## Requirements

- Python 3.10+
- `requests`, `schedule`

```bash
pip install requests schedule
```

---

## Roadmap

- [ ] Telegram alerts
- [ ] Multi-currency support (MLA, MLB, MLC…)
- [ ] Web dashboard (Flask/FastAPI)
- [ ] AWS Lambda deployment
- [ ] Price history chart (matplotlib)

---

## 💸 Donations

If you'd like to support this project:

- 🇦🇷 ARS (Argentina) — Alias: `lazaro.503.alaba.mp`
- 🌎 USD (Argentina only, local transfers) — Alias: `ahogada.duras.foca`

---

Made by [Lazaro Gomez Vitolo](https://github.com/Lazaro549) — Mar del Plata, Argentina 🇦🇷

import os
import requests
from datetime import date, timedelta

# --- Telegram config from environment variables ---
TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = int(os.environ["TELEGRAM_CHAT_ID"])

def send_telegram(message: str):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    r = requests.post(url, data=payload)
    r.raise_for_status()

# --- Surf logic ---
WATERGATE = (50.4445, -5.0398)
CROYDE = (51.1278, -4.2286)

THRESHOLD = 14.0  # seconds
DAYS_AHEAD = 5

def swell_period_on_date(lat, lon, target_date):
    url = (
        "https://marine-api.open-meteo.com/v1/marine"
        f"?latitude={lat}&longitude={lon}"
        "&daily=swell_wave_period_max"
        "&forecast_days=7"
        "&timezone=Europe%2FLondon"
    )
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()

    times = data["daily"]["time"]
    periods = data["daily"]["swell_wave_period_max"]

    target_str = target_date.isoformat()
    i = times.index(target_str)
    return periods[i]

def main():
    today = date.today()
    target = today + timedelta(days=DAYS_AHEAD)

    w_period = swell_period_on_date(*WATERGATE, target)
    c_period = swell_period_on_date(*CROYDE, target)

    print(f"Watergate on {target}: {w_period:.1f} seconds")
    print(f"Croyde on {target}: {c_period:.1f} seconds")

    # Only alert if threshold is hit
    if w_period >= THRESHOLD or c_period >= THRESHOLD:
        msg = (
            f"Surf radar – {target}\n"
            f"Watergate: {w_period:.1f}s\n"
            f"Croyde: {c_period:.1f}s\n"
            "🔥 Long-period swell 5 days out! (threshold hit)"
        )
        print("Sending Telegram alert:")
        print(msg)
        send_telegram(msg)
    else:
        print("No special long-period swell 5 days out. No alert sent.")

if __name__ == "__main__":
    main()

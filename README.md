🌊 Surf Radar – Long-Period Swell Alerts

A tiny automation that tells me when the surf is likely to be good at my favourite UK spots.
Swell period is the most reliable early indicator of quality waves, so this bot checks the marine forecast and alerts me only when the conditions look promising.

⸻

✔️ What It Does
	•	Fetches the marine forecast from Open-Meteo
	•	Checks the swell period 5 days ahead for:
	•	Watergate Bay
	•	Croyde Bay
	•	If either spot has a daily max period ≥ 14 seconds, it sends me a Telegram message
	•	If not, it stays silent
	•	Runs automatically once per day via GitHub Actions

⸻

⚙️ How It Works
	•	surf_check.py pulls the data, checks the threshold, and sends a Telegram alert
	•	.github/workflows/surf.yml runs the script daily on GitHub’s servers
	•	Secrets (TELEGRAM_TOKEN, TELEGRAM_CHAT_ID) are stored securely in GitHub Secrets

No hosting, no costs, no manual checking.

⸻

🕒 Schedule

Runs daily at 07:00 UTC
(07:00 UK in winter, 08:00 UK in summer)

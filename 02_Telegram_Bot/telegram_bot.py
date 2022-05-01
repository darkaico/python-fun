import os

import requests

# token que obtuvimos con BotFather
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

chat_id = "<aqui usamos el chat id donde se haya incluido al bot>"
message = "La verdad, ni me sorprende"

params = {"chat_id": chat_id, "parse_mode": "Markdown", "text": message}

requests.get(TELEGRAM_API_URL, params=params)

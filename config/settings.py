# config/settings.py
import os

# --- Telegram Bot (OBLIGATOIRE) ---
TELEGRAM_TOKEN = "1234567890:ABCdefGHIJKLMNOPQRSTUVWXYZabcdefghijklmn"  # Ton token bot Telegram (obtenu via @BotFather)
ADMIN_ID = 987654321  # Ton ID Telegram (trouve-le via @userinfobot)

# --- Pocket Option (OPTIONNEL, pour scraping) ---
POCKET_OPTION_URL = "https://www.pocketoption.com"  # Ne change pas sauf si le site change
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.pocketoption.com/"
}

# --- Paramètres des stratégies (Ne change pas sauf si tu veux modifier les indicateurs) ---
STRATEGIES = {
    "1min": {
        "timeframe": "1m",
        "expiration": 60,
        "bb_period": 20,
        "bb_dev": 2,
        "sma1_period": 2,
        "sma2_period": 5,
        "rsi_period": 8,
        "rsi_overbought": 70,
        "rsi_oversold": 30
    },
    "2min": {
        "timeframe": "2m",
        "expiration": 120,
        "bb_period": 6,
        "bb_dev": 1.3,
        "macd_fast": 6,
        "macd_slow": 19,
        "macd_signal": 6
    }
}

# --- Paires OTC avec 87%+ payout (À mettre à jour si Pocket Option change) ---
OTC_PAIRS = [
    "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD",
    "NZD/USD", "EUR/GBP", "EUR/JPY", "GBP/JPY", "USD/CHF"
]

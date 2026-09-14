# config/settings.py
import os

# --- Telegram Bot ---
TELEGRAM_TOKEN = "TON_TOKEN_BOT_TELEGRAM"
ADMIN_ID = 123456789  # Ton ID Telegram (pour les logs)

# --- Pocket Option API ---
PO_API_KEY = "TA_CLE_API_POCKET_OPTION"  # Si tu utilises leur API officielle
PO_API_URL = "https://api.pocketoption.com/v1"

# --- Paramètres des stratégies ---
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
    },
    "5min": {
        "timeframe": "5m",
        "expiration": 300,
        # Ajoute les paramètres pour 5min ici
    }
}

# --- Paires OTC avec 87%+ payout (à mettre à jour) ---
OTC_PAIRS = [
    "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD",
    "NZD/USD", "EUR/GBP", "EUR/JPY", "GBP/JPY", "USD/CHF"
]

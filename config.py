import os

# Telegram API Token (Récupéré depuis la variable d'environnement ou valeur par défaut)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "VOTRE_TOKEN_TELEGRAM_ICI")

# Authentification Pocket Option via SSID
POCKET_SSID = os.getenv("POCKET_SSID", "VOTRE_SSID_ICI")
POCKET_WS_URL = "wss://api-fin.po.trade/socket.io/?EIO=4&transport=websocket"

# Liens d'affiliation et réseaux sociaux
LINK_VIDEO = "https://t.me/LegitTrade_academy"
LINK_INSCRIPTION = "https://bit.ly/4ckz9cY"

# Configuration du payout minimum retenu pour l'analyse
MIN_PAYOUT = 87

# Mapping des 57 paires de devises OTC avec leurs identifiants
ACTIFS_CODES = {
    "🇦🇺 AUD/CAD 🇨🇦OTC": "audcad",
    "🇨🇦 CAD/CHF 🇨🇭OTC": "cadchf",
    "🇨🇦 CAD/JPY 🇯🇵OTC": "cadjpy",
    "🇨🇭 CHF/NOK 🇳🇴OTC": "chfnok",
    "🇪🇺 EUR/CHF 🇨🇭OTC": "eurchf",
    "🇪🇺 EUR/TRY 🇹🇷OTC": "eurtry",
    "🇪🇺 EUR/USD 🇺🇸OTC": "eurusd",
    "🇬🇧 GBP/AUD 🇦🇺OTC": "gbpaud",
    "🇬🇧 GBP/JPY 🇯🇵OTC": "gbpjpy",
    "🇬🇧 GBP/USD 🇺🇸OTC": "gbpusd",
    "🇰🇪 KES/USD 🇺🇸OTC": "kesusd",
    "🇳ℤ NZD/USD 🇺🇸OTC": "nzdusd",
    "🇸🇦 SAR/CNY 🇨🇳OTC": "sarcny",
    "🇹🇳 TND/USD 🇺🇸OTC": "tndusd",
    "🇺🇦 UAH/USD 🇺🇸OTC": "uahusd",
    "🇺🇸 USD/BRL 🇧🇷OTC": "usdbrl",
    "🇺🇸 USD/CAD 🇨🇦OTC": "usdcad",
    "🇺🇸 USD/CHF 🇨🇭OTC": "usdchf",
    "🇺🇸 USD/CLP 🇨🇱OTC": "usdclp",
    "🇺🇸 USD/COP 🇨🇴OTC": "usdcop",
    "🇺🇸 USD/EGP 🇪🇬OTC": "usdegp",
    "🇺🇸 USD/IDR 🇮🇩OTC": "usdidr",
    "🇺🇸 USD/PHP 🇵🇭OTC": "usdphp",
    "🇺🇸 USD/RUB 🇷🇺OTC": "usdrub",
    "🇺🇸 USD/THB 🇹🇭OTC": "usdthb",
    "🇾🇪 YER/USD 🇺🇸OTC": "yerusd",
    "🇴🇲 OMR/CNY 🇨🇳OTC": "omrcny",
    "🇺🇸 USD/BDT 🇧🇩OTC": "usdbdt",
    "🇺🇸 USD/MXN 🇲🇽OTC": "usdmxn",
    "🇪🇺 EUR/NZD 🇳ℤOTC": "eurnzd",
    "🇪🇺 EUR/JPY 🇯🇵OTC": "eurjpy",
    "🇧🇭 BHD/CNY 🇨🇳OTC": "bhdcny",
    "🇦🇪 AED/CNY 🇨🇳OTC": "aedcny",
    "🇦🇺 AUD/NZD 🇳ℤOTC": "audnzd",
    "🇦🇺 AUD/CHF 🇨🇭OTC": "audchf",
    "🇦🇺 AUD/JPY 🇯🇵OTC": "audjpy",
    "🇳🇬 NGN/USD 🇺🇸OTC": "ngnusd",
    "🇨🇭 CHF/JPY 🇯🇵OTC": "chfjpy",
    "🇲🇦 MAD/USD 🇺🇸OTC": "madusd",
    "🇶🇦 QAR/CNY 🇨🇳OTC": "qarcny",
    "🇺🇸 USD/SGD 🇸🇬OTC": "usdsgd",
    "🇺🇸 USD/ARS 🇦🇷OTC": "usdars",
    "🇪🇺 EUR/RUB 🇷🇺OTC": "eurrub",
    "🇺🇸 USD/CNH 🇨🇳OTC": "usdcnh",
    "🇺🇸 USD/JPY 🇯🇵OTC": "usdjpy",
    "🇳ℤ NZD/JPY 🇯🇵OTC": "nzdjpy",
    "🇺🇸 USD/VND 🇻🇳OTC": "usdvnd",
    "🇺🇸 USD/MYR 🇲🇾OTC": "usdmyr",
    "🇿🇦 ZAR/USD 🇺🇸OTC": "zarusd",
    "🇦🇺 AUD/USD 🇺🇸OTC": "audusd",
    "🇪🇺 EUR/GBP 🇬🇧OTC": "eurgbp",
    "🇺🇸 USD/PKR 🇵🇰OTC": "usdpkr",
    "🇺🇸 USD/DZD 🇩🇿OTC": "usddzd",
    "🇪🇺 EUR/HUF 🇭🇺OTC": "eurhuf",
    "🇱🇧 LBP/USD 🇺🇸OTC": "lbpusd",
    "🇯🇴 JOD/CNY 🇨🇳OTC": "jodcny",
    "🇺🇸 USD/INR 🇮🇳OTC": "usdinr"
}

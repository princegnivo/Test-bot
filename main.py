# main.py
import asyncio
from core.bot import start_bot

if __name__ == "__main__":
    print("[TERMUX] Bot démarré. Appuie sur Ctrl+C pour arrêter.")
    asyncio.run(start_bot())

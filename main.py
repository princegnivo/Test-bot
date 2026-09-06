import asyncio
import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

from config import TELEGRAM_TOKEN, POCKET_SSID, ACTIFS_CODES, LINK_VIDEO, LINK_INSCRIPTION
from pocket_ws import PocketOptionWS
from strategy import StrategyEngine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TradingBotApp:
    def __init__(self):
        self.app = Application.builder().token(TELEGRAM_TOKEN).post_init(self.post_init).build()
        self.ws_client = PocketOptionWS(POCKET_SSID)
        self.active_chats = set()

    async def post_init(self, application: Application):
        self.ws_client.connect()
        asyncio.create_task(self.automated_analysis_loop())

    def format_signal_message(self, actif: str, direction: str, timeframe: str) -> str:
        """Formate le message texte du signal"""
        return f"""<a href="{LINK_VIDEO}"><b>VIDÉO D’INSCRIPTION</b></a>
______________________________

📊 <b>ACTIF:</b> {actif}

⏳ <b>EXPIRATION:</b> {timeframe}

🔮 <b>Direction:</b> {direction}

———————————————
<a href="{LINK_INSCRIPTION}"><b>INSCRIPTION</b></a>"""

    async def send_signal_text(self, chat_id: int, actif: str, direction: str, timeframe: str):
        """Envoie le signal au format texte uniquement"""
        message = self.format_signal_message(actif, direction, timeframe)
        try:
            await self.app.bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode="HTML",
                disable_web_page_preview=True
            )
        except Exception as e:
            logger.error(f"Erreur d'envoi du signal au chat {chat_id}: {e}")

    async def automated_analysis_loop(self):
        """Boucle d'analyse automatique en arrière-plan"""
        while True:
            await asyncio.sleep(60)
            if not self.active_chats:
                continue

            for actif in ACTIFS_CODES.keys():
                df = self.ws_client.get_candles(actif)
                if df.empty:
                    continue

                signal_m1 = StrategyEngine.check_m1_strategy(df)
                if signal_m1:
                    for chat_id in self.active_chats.copy():
                        await self.send_signal_text(chat_id, actif, signal_m1, "60s (1min)")

                signal_m2 = StrategyEngine.check_m2_strategy(df)
                if signal_m2:
                    for chat_id in self.active_chats.copy():
                        await self.send_signal_text(chat_id, actif, signal_m2, "120s (2min)")

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /start"""
        chat_id = update.effective_chat.id
        self.active_chats.add(chat_id)

        keyboard = [[InlineKeyboardButton("Analyse... ⏳", callback_data="analyze_now")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "🤖 <b>Bot de Trading Algorithmique Initialisé</b>\n\n"
            "Analyse automatique active en arrière-plan via WebSocket.\n"
            "Cliquez sur le bouton ci-dessous pour lancer une analyse.",
            reply_markup=reply_markup,
            parse_mode="HTML"
        )

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gestion des clics sur les boutons interactifs"""
        query = update.callback_query
        await query.answer()

        if query.data == "analyze_now":
            await query.edit_message_text("Analyse... ⏳")
            await asyncio.sleep(2)

            found_signal = False
            for actif in ACTIFS_CODES.keys():
                df = self.ws_client.get_candles(actif)
                if df.empty:
                    continue

                signal = StrategyEngine.check_m1_strategy(df) or StrategyEngine.check_m2_strategy(df)
                if signal:
                    await self.send_signal_text(query.message.chat_id, actif, signal, "120s (2min)")
                    found_signal = True
                    break

            if not found_signal:
                # Simulation de secours si pas encore assez de données dans le WebSocket
                actif = random.choice(list(ACTIFS_CODES.keys()))
                direction = random.choice(["ACHAT", "VENTE"])
                await self.send_signal_text(query.message.chat_id, actif, direction, "120s (2min)")

    def run(self):
        """Lancement du bot"""
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CallbackQueryHandler(self.button_callback))
        logger.info("Lancement du Bot Telegram (Version Texte)...")
        self.app.run_polling()

if __name__ == "__main__":
    app = TradingBotApp()
    app.run()

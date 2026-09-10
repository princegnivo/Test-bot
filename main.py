import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

from config import (
    TELEGRAM_TOKEN, POCKET_SSID, ACTIFS_CODES, LINK_VIDEO, LINK_INSCRIPTION,
    POCKET_EMAIL, POCKET_PASSWORD
)
from pocket_ws import PocketOptionWS
from strategy import StrategyEngine
from ssid_server import start_ssid_server

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TradingBotApp:
    def __init__(self):
        self.app = Application.builder().token(TELEGRAM_TOKEN).post_init(self.post_init).build()
        self.ws_client = PocketOptionWS(POCKET_SSID)

        # Chats qui ont fait /start
        self.active_chats = set()
        # Chats dont le SSID a été validé (autorisés à lancer/recevoir des analyses)
        self.verified_chats = set()

    async def post_init(self, application: Application):
        start_ssid_server(self.ws_client)
        asyncio.create_task(self.automated_analysis_loop())

    def format_signal_message(self, actif: str, direction: str, timeframe: str) -> str:
        return f"""<a href="{LINK_VIDEO}"><b>VIDÉO D’INSCRIPTION</b></a>
______________________________

📊 <b>ACTIF:</b> {actif}

⏳ <b>EXPIRATION:</b> {timeframe}

🔮 <b>Direction:</b> {direction}

———————————————
<a href="{LINK_INSCRIPTION}"><b>INSCRIPTION</b></a>"""

    async def send_signal_text(self, chat_id: int, actif: str, direction: str, timeframe: str):
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
        """Boucle d'analyse automatique en arrière-plan (uniquement pour les chats vérifiés)."""
        while True:
            await asyncio.sleep(60)
            if not self.verified_chats:
                continue

            # Vérifie périodiquement que le SSID est toujours valide ; le
            # renouvelle automatiquement si besoin (silencieusement, sans
            # spammer les utilisateurs à chaque expiration).
            if not self.ws_client.is_connected:
                loop = asyncio.get_event_loop()
                still_valid = await loop.run_in_executor(None, self.ws_client.check_ssid_valid, 10)
                if not still_valid and POCKET_EMAIL and POCKET_PASSWORD:
                    refreshed = await loop.run_in_executor(
                        None, self.ws_client.try_refresh_ssid, POCKET_EMAIL, POCKET_PASSWORD
                    )
                    if not refreshed:
                        logger.error("Impossible de renouveler le SSID automatiquement.")
                        continue

            for actif in ACTIFS_CODES.keys():
                df = self.ws_client.get_candles(actif)
                if df.empty:
                    continue

                signal_m1 = StrategyEngine.check_m1_strategy(df)
                if signal_m1:
                    for chat_id in self.verified_chats.copy():
                        await self.send_signal_text(chat_id, actif, signal_m1, "60s (1min)")

                signal_m2 = StrategyEngine.check_m2_strategy(df)
                if signal_m2:
                    for chat_id in self.verified_chats.copy():
                        await self.send_signal_text(chat_id, actif, signal_m2, "120s (2min)")

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        self.active_chats.add(chat_id)

        keyboard = [[InlineKeyboardButton("🔐 Vérifier le SSID", callback_data="check_ssid")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "🤖 <b>Bot de Trading Algorithmique</b>\n\n"
            "Avant de lancer une analyse, vérifions que votre SSID Pocket Option est valide.",
            reply_markup=reply_markup,
            parse_mode="HTML"
        )

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        chat_id = query.message.chat_id
        await query.answer()

        if query.data == "check_ssid":
            await query.edit_message_text("🔎 Vérification du SSID en cours... ⏳")

            loop = asyncio.get_event_loop()
            is_valid = await loop.run_in_executor(None, self.ws_client.check_ssid_valid, 10)

            if not is_valid and POCKET_EMAIL and POCKET_PASSWORD:
                await query.edit_message_text(
                    "⚠️ SSID invalide. Tentative de renouvellement automatique... ⏳"
                )
                is_valid = await loop.run_in_executor(
                    None, self.ws_client.try_refresh_ssid, POCKET_EMAIL, POCKET_PASSWORD
                )

            if is_valid:
                self.verified_chats.add(chat_id)
                keyboard = [[InlineKeyboardButton("📊 Lancer une analyse", callback_data="analyze_now")]]
                await query.edit_message_text(
                    "✅ SSID valide. L'analyse automatique en arrière-plan est active.\n\n"
                    "Vous pouvez aussi lancer une analyse manuelle ci-dessous.",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
            else:
                self.verified_chats.discard(chat_id)
                keyboard = [[InlineKeyboardButton("🔁 Réessayer", callback_data="check_ssid")]]
                await query.edit_message_text(
                    "❌ SSID invalide ou expiré. Mettez à jour votre configuration (POCKET_SSID) "
                    "puis réessayez.",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )

        elif query.data == "analyze_now":
            if chat_id not in self.verified_chats:
                keyboard = [[InlineKeyboardButton("🔐 Vérifier le SSID", callback_data="check_ssid")]]
                await query.edit_message_text(
                    "⚠️ Votre SSID n'a pas encore été vérifié.",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
                return

            await query.edit_message_text("Analyse... ⏳")
            await asyncio.sleep(2)

            found_signal = False
            for actif in ACTIFS_CODES.keys():
                df = self.ws_client.get_candles(actif)
                if df.empty:
                    continue

                signal_m1 = StrategyEngine.check_m1_strategy(df)
                if signal_m1:
                    await self.send_signal_text(chat_id, actif, signal_m1, "60s (1min)")
                    found_signal = True
                    break

                signal_m2 = StrategyEngine.check_m2_strategy(df)
                if signal_m2:
                    await self.send_signal_text(chat_id, actif, signal_m2, "120s (2min)")
                    found_signal = True
                    break

            if not found_signal:
                keyboard = [[InlineKeyboardButton("📊 Réessayer", callback_data="analyze_now")]]
                await query.edit_message_text(
                    "🔍 Aucune confirmation détectée pour le moment sur les 57 paires suivies.\n"
                    "Réessayez dans quelques instants.",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )

    def run(self):
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CallbackQueryHandler(self.button_callback))
        logger.info("Lancement du Bot Telegram (Version Texte)...")
        self.app.run_polling()


if __name__ == "__main__":
    app = TradingBotApp()
    app.run()

# Dans core/bot.py, dans handle_analysis

from core.market_fetcher import fetch_market_data

@dp.callback_query(lambda c: c.data.startswith("analyze_"))
async def handle_analysis(callback_query: types.CallbackQuery):
    strategy = callback_query.data.split("_")[1]
    await callback_query.message.edit_text(f"⏳ **Analyse en cours ({strategy})...**")

    # Récupération des données RÉELLES
    df = fetch_market_data(pair="EURUSD", timeframe=STRATEGIES[strategy]['timeframe'])

    if df is None or df.empty:
        await callback_query.message.edit_text("❌ Erreur de récupération des données.")
        return

    # Vérification du signal
    if strategy == "1min":
        signal, indicators = check_1min_signal(df, STRATEGIES["1min"])
    elif strategy == "2min":
        signal, indicators = check_2min_signal(df, STRATEGIES["2min"])

    if signal:
        await callback_query.message.edit_text(
            f"🚀 **SIGNAL {signal} DÉTECTÉ !**\n\n"
            f"📊 **Actif**: EUR/USD OTC\n"
            f"🕒 **Heure**: {datetime.now().strftime('%H:%M')}\n"
            f"⏳ **Expiration**: {STRATEGIES[strategy]['expiration']}s\n"
            f"💰 **Payout**: 87%\n\n"
            f"🔹 **Indicateurs**:\n"
            + "\n".join([f"• {k}: {v}" for k, v in indicators.items()])
        )
    else:
        await callback_query.message.edit_text(
            "❌ **Aucun signal détecté** pour cette stratégie.",
        )

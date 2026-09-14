# core/signals.py
from datetime import datetime
from core.indicators import (
    calculate_heikin_ashi, calculate_bollinger_bands,
    calculate_sma, calculate_rsi, calculate_macd
)

def check_1min_signal(df, strategy_params):
    """Vérifie les conditions pour un signal 1min."""
    ha_df = calculate_heikin_ashi(df)
    df = calculate_bollinger_bands(df, strategy_params['bb_period'], strategy_params['bb_dev'])
    df = calculate_sma(df, strategy_params['sma1_period'])
    df = calculate_sma(df, strategy_params['sma2_period'])
    df = calculate_rsi(df, strategy_params['rsi_period'])

    last_row = df.iloc[-1]
    prev_row = df.iloc[-2]

    # Signal CALL (Achat)
    call_conditions = (
        (last_row['ha_close'] >= last_row['bb_lower']) and  # Touche la bande inférieure
        (prev_row[f'sma_{strategy_params["sma1_period"]}'] < prev_row[f'sma_{strategy_params["sma2_period"]}']) and  # SMA2 croise SMA5 vers le haut
        (last_row[f'sma_{strategy_params["sma1_period"]}'] > last_row[f'sma_{strategy_params["sma2_period"]}']) and
        (last_row['rsi'] > prev_row['rsi']) and  # RSI en hausse
        (last_row['rsi'] < strategy_params['rsi_overbought'])  # RSI pas en surachat
    )

    # Signal PUT (Vente)
    put_conditions = (
        (last_row['ha_close'] <= last_row['bb_upper']) and  # Touche la bande supérieure
        (prev_row[f'sma_{strategy_params["sma1_period"]}'] > prev_row[f'sma_{strategy_params["sma2_period"]}']) and  # SMA2 croise SMA5 vers le bas
        (last_row[f'sma_{strategy_params["sma1_period"]}'] < last_row[f'sma_{strategy_params["sma2_period"]}']) and
        (last_row['rsi'] < prev_row['rsi']) and  # RSI en baisse
        (last_row['rsi'] > strategy_params['rsi_oversold'])  # RSI pas en survente
    )

    if call_conditions:
        return "CALL", {
            "rsi": round(last_row['rsi'], 2),
            "bb_upper": round(last_row['bb_upper'], 5),
            "bb_lower": round(last_row['bb_lower'], 5),
            "sma2": round(last_row[f'sma_{strategy_params["sma1_period"]}'], 5),
            "sma5": round(last_row[f'sma_{strategy_params["sma2_period"]}'], 5)
        }
    elif put_conditions:
        return "PUT", {
            "rsi": round(last_row['rsi'], 2),
            "bb_upper": round(last_row['bb_upper'], 5),
            "bb_lower": round(last_row['bb_lower'], 5),
            "sma2": round(last_row[f'sma_{strategy_params["sma1_period"]}'], 5),
            "sma5": round(last_row[f'sma_{strategy_params["sma2_period"]}'], 5)
        }
    else:
        return None, None

def check_2min_signal(df, strategy_params):
    """Vérifie les conditions pour un signal 2min."""
    ha_df = calculate_heikin_ashi(df)
    df = calculate_bollinger_bands(df, strategy_params['bb_period'], strategy_params['bb_dev'])
    df = calculate_macd(df, strategy_params['macd_fast'], strategy_params['macd_slow'], strategy_params['macd_signal'])

    last_row = df.iloc[-1]
    prev_row = df.iloc[-2]

    # Signal CALL (Achat)
    call_conditions = (
        (last_row['ha_close'] >= last_row['bb_upper']) and  # Touche la bande supérieure
        (prev_row['macd'] < prev_row['macd_signal']) and  # MACD croise vers le haut
        (last_row['macd'] > last_row['macd_signal']) and
        (last_row['macd_hist'] > 0)  # Histogramme positif
    )

    # Signal PUT (Vente)
    put_conditions = (
        (last_row['ha_close'] <= last_row['bb_lower']) and  # Touche la bande inférieure
        (prev_row['macd'] > prev_row['macd_signal']) and  # MACD croise vers le bas
        (last_row['macd'] < last_row['macd_signal']) and
        (last_row['macd_hist'] < 0)  # Histogramme négatif
    )

    if call_conditions:
        return "CALL", {
            "macd": round(last_row['macd'], 5),
            "macd_signal": round(last_row['macd_signal'], 5),
            "bb_upper": round(last_row['bb_upper'], 5),
            "bb_lower": round(last_row['bb_lower'], 5)
        }
    elif put_conditions:
        return "PUT", {
            "macd": round(last_row['macd'], 5),
            "macd_signal": round(last_row['macd_signal'], 5),
            "bb_upper": round(last_row['bb_upper'], 5),
            "bb_lower": round(last_row['bb_lower'], 5)
        }
    else:
        return None, None

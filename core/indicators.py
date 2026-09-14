# core/indicators.py
import numpy as np
import pandas as pd
import talib

def calculate_heikin_ashi(df):
    """Convertit les bougies classiques en Heikin Ashi."""
    ha_close = (df['open'] + df['high'] + df['low'] + df['close']) / 4
    ha_open = (df['open'].shift(1) + df['close'].shift(1)) / 2
    ha_high = df[['high', 'open', 'close']].max(axis=1)
    ha_low = df[['low', 'open', 'close']].min(axis=1)

    return pd.DataFrame({
        'ha_open': ha_open,
        'ha_close': ha_close,
        'ha_high': ha_high,
        'ha_low': ha_low
    })

def calculate_bollinger_bands(df, period=20, dev=2):
    """Calcule les Bandes de Bollinger."""
    df['bb_upper'], df['bb_middle'], df['bb_lower'] = talib.BBANDS(
        df['close'], timeperiod=period, nbdevup=dev, nbdevdn=dev
    )
    return df

def calculate_sma(df, period=5):
    """Calcule une SMA."""
    df[f'sma_{period}'] = talib.SMA(df['close'], timeperiod=period)
    return df

def calculate_rsi(df, period=14):
    """Calcule le RSI."""
    df['rsi'] = talib.RSI(df['close'], timeperiod=period)
    return df

def calculate_macd(df, fast=12, slow=26, signal=9):
    """Calcule le MACD."""
    df['macd'], df['macd_signal'], df['macd_hist'] = talib.MACD(
        df['close'], fastperiod=fast, slowperiod=slow, signalperiod=signal
    )
    return df

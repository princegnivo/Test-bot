import pandas as pd
from indicators import TechnicalAnalysis

class StrategyEngine:
    @staticmethod
    def check_m1_strategy(df: pd.DataFrame) -> str:
        """Évalue la stratégie M1 (1 Minute). Renvoie 'ACHAT', 'VENTE' ou None."""
        if len(df) < 20:
            return None
            
        data = TechnicalAnalysis.calculate_m1_indicators(df)
        curr = data.iloc[-1]
        prev = data.iloc[-2]

        # Conditions ACHAT (CALL)
        c1_buy = curr['close'] <= curr['BB_lower'] or prev['close'] <= prev['BB_lower']
        c2_buy = (prev['SMA_2'] <= prev['SMA_5']) and (curr['SMA_2'] > curr['SMA_5'])  # Cross Above
        c3_buy = curr['RSI_8'] > prev['RSI_8'] and curr['RSI_8'] <= 50

        if c1_buy and c2_buy and c3_buy:
            return "ACHAT"

        # Conditions VENTE (PUT)
        c1_sell = curr['close'] >= curr['BB_upper'] or prev['close'] >= prev['BB_upper']
        c2_sell = (prev['SMA_2'] >= prev['SMA_5']) and (curr['SMA_2'] < curr['SMA_5'])  # Cross Below
        c3_sell = curr['RSI_8'] < prev['RSI_8'] and curr['RSI_8'] >= 50

        if c1_sell and c2_sell and c3_sell:
            return "VENTE"

        return None

    @staticmethod
    def check_m2_strategy(df: pd.DataFrame) -> str:
        """Évalue la stratégie M2 (2 Minutes). Renvoie 'ACHAT', 'VENTE' ou None."""
        if len(df) < 20:
            return None

        data = TechnicalAnalysis.calculate_m2_indicators(df)
        curr = data.iloc[-1]
        prev = data.iloc[-2]

        # Bougie forte Heikin Ashi (corps plein)
        is_strong_green = curr['close'] > curr['open'] and (curr['open'] == curr['low'])
        is_strong_red = curr['close'] < curr['open'] and (curr['open'] == curr['high'])

        # Conditions ACHAT (HIGHER)
        c1_buy = (prev['MACD'] <= prev['MACD_signal']) and (curr['MACD'] > curr['MACD_signal'])
        c2_buy = curr['close'] >= curr['BB_upper']
        c3_buy = is_strong_green

        if c1_buy and c2_buy and c3_buy:
            return "ACHAT"

        # Conditions VENTE (LOWER)
        c1_sell = (prev['MACD'] >= prev['MACD_signal']) and (curr['MACD'] < curr['MACD_signal'])
        c2_sell = curr['close'] <= curr['BB_lower']
        c3_sell = is_strong_red

        if c1_sell and c2_sell and c3_sell:
            return "VENTE"

        return None

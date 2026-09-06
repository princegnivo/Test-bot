import pandas as pd
import pandas_ta as ta

class TechnicalAnalysis:
    @staticmethod
    def convert_to_heikin_ashi(df: pd.DataFrame) -> pd.DataFrame:
        """Convertit un DataFrame de bougies OHLC en bougies Heikin Ashi."""
        ha_df = df.copy()
        ha_df['close'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4

        ha_open = [(df['open'].iloc[0] + df['close'].iloc[0]) / 2]
        for i in range(1, len(df)):
            ha_open.append((ha_open[i - 1] + ha_df['close'].iloc[i - 1]) / 2)
        ha_df['open'] = ha_open

        ha_df['high'] = ha_df[['open', 'close']].join(df['high']).max(axis=1)
        ha_df['low'] = ha_df[['open', 'close']].join(df['low']).min(axis=1)
        return ha_df

    @staticmethod
    def calculate_m1_indicators(df: pd.DataFrame) -> pd.DataFrame:
        """Calcule les indicateurs M1: BB(20,2), SMA(2), SMA(5), RSI(8)."""
        ha_df = TechnicalAnalysis.convert_to_heikin_ashi(df)
        
        # Bandes de Bollinger (20, 2)
        bb = ta.bbands(ha_df['close'], length=20, std=2)
        ha_df['BB_lower'] = bb['BBL_20_2.0']
        ha_df['BB_upper'] = bb['BBU_20_2.0']
        
        # SMAs
        ha_df['SMA_2'] = ta.sma(ha_df['close'], length=2)
        ha_df['SMA_5'] = ta.sma(ha_df['close'], length=5)
        
        # RSI (8)
        ha_df['RSI_8'] = ta.rsi(ha_df['close'], length=8)
        return ha_df

    @staticmethod
    def calculate_m2_indicators(df: pd.DataFrame) -> pd.DataFrame:
        """Calcule les indicateurs M2: BB(6, 1.3), MACD(6, 19, 6)."""
        ha_df = TechnicalAnalysis.convert_to_heikin_ashi(df)
        
        # Bandes de Bollinger (6, 1.3)
        bb = ta.bbands(ha_df['close'], length=6, std=1.3)
        ha_df['BB_lower'] = bb['BBL_6_1.3']
        ha_df['BB_upper'] = bb['BBU_6_1.3']
        
        # MACD (6, 19, 6)
        macd = ta.macd(ha_df['close'], fast=6, slow=19, signal=6)
        ha_df['MACD'] = macd['MACD_6_19_6']
        ha_df['MACD_signal'] = macd['MACDs_6_19_6']
        ha_df['MACD_hist'] = macd['MACDh_6_19_6']
        return ha_df

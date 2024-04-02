import pandas as pd

def get_avg_noise_ratio(df : pd.DataFrame) -> float:
    return (1 - abs(df['open']-df['close']) / (df['high']-df['low'])).mean()

def get_range(df : pd.DataFrame) -> float:
    return df['high'].max() - df['low'].min()

def get_volatility(df : pd.DataFrame) -> float:
    return get_range(df) / df.iloc[0]['open']
# technical_indicators.py
import pandas as pd
import numpy as np

def calculate_sma(data, window):
    """Calculate Simple Moving Average (SMA)."""
    return data['Close'].rolling(window=window).mean()

def calculate_ema(data, window):
    """Calculate Exponential Moving Average (EMA)."""
    return data['Close'].ewm(span=window, adjust=False).mean()

def calculate_rsi(data, window=14):
    """Calculate Relative Strength Index (RSI)."""
    delta = data['Close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    """Calculate Moving Average Convergence Divergence (MACD)."""
    short_ema = calculate_ema(data, short_window)
    long_ema = calculate_ema(data, long_window)
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    return macd, signal

# Example usage
if __name__ == "__main__":
    data = pd.read_csv('sample_stock_data.csv')  # Replace with your dataset
    data['SMA_20'] = calculate_sma(data, 20)
    data['EMA_20'] = calculate_ema(data, 20)
    data['RSI_14'] = calculate_rsi(data)
    data['MACD'], data['Signal'] = calculate_macd(data)

    print(data.head())

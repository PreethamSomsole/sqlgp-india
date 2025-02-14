import pyarrow.csv as pv
import pyarrow.compute as pc
import matplotlib.pyplot as plt

from analysis.technical import calculate_sma, calculate_ema, calculate_rsi, calculate_macd
from data.data_loader import load_data

def plot_technical_indicators(data, ticker):
    plt.figure(figsize=(14, 10))

    plt.subplot(3, 1, 1)
    plt.plot(data['Close'].to_numpy(), label='Close Price', color='blue')
    plt.plot(data['SMA_20'].to_numpy(), label='SMA 20', color='orange')
    plt.plot(data['EMA_20'].to_numpy(), label='EMA 20', color='purple')
    plt.title(f'{ticker} Price with SMA and EMA')
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(data['RSI_14'].to_numpy(), label='RSI 14', color='green')
    plt.axhline(70, color='red', linestyle='--')
    plt.axhline(30, color='red', linestyle='--')
    plt.title(f'{ticker} Relative Strength Index (RSI)')
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(data['MACD'].to_numpy(), label='MACD', color='black')
    plt.plot(data['Signal'].to_numpy(), label='Signal Line', color='red')
    plt.title(f'{ticker} MACD')
    plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    table = load_data('sample_stock_data.csv')  # Custom loader from data module
    data = table.to_pandas()
    data['SMA_20'] = calculate_sma(data, 20)
    data['EMA_20'] = calculate_ema(data, 20)
    data['RSI_14'] = calculate_rsi(data)
    data['MACD'], data['Signal'] = calculate_macd(data)

    plot_technical_indicators(data, ticker='Sample Ticker')
"""
Overview of RSI Indicator
RSI(Relative Strength Index) measures the speed and magnitude of price changes to identify overbought or oversold conditions.

Signals:
RSI < 30 → Oversold (Buy signal).
RSI > 70 → Overbought (Sell signal).
"""

import ccxt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Fetch historical price data from Binance
def fetch_historical_data(symbol='BTC/USDT', timeframe='1h', limit=100):
    binance = ccxt.binance({
        'rateLimit': 1200,
        'enableRateLimit': True,
    })
    ohlcv = binance.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')  # Convert timestamp to datetime
    return df

# Fetch data
symbol = 'BTC/USDT'  # You can use any symbol like ETH/USDT, BNB/USDT, etc.
timeframe = '1h'     # 1-hour timeframe
data = fetch_historical_data(symbol, timeframe)
print(data.head())

# Function to calculate RSI
def calculate_rsi(df, period=14):
    delta = df['close'].diff()  # Price difference between consecutive days
    gain = delta.where(delta > 0, 0)  # Gains
    loss = -delta.where(delta < 0, 0)  # Losses
    
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()

    # Calculate RSI
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

# Calculate RSI
data = calculate_rsi(data)
print(data[['timestamp', 'close', 'RSI']].tail())

# Function to generate buy/sell signals based on RSI
def generate_rsi_signals(df, lower=30, upper=70):
    df['Signal'] = None
    for i in range(len(df)):
        if df['RSI'][i] < lower:
            df['Signal'][i] = 'BUY'
        elif df['RSI'][i] > upper:
            df['Signal'][i] = 'SELL'
    return df

# Generate signals
data = generate_rsi_signals(data)
print(data[['timestamp', 'close', 'RSI', 'Signal']].tail())

# Function to plot price, RSI, and signals
def plot_rsi_signals(df):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # Plot Closing Price and Buy/Sell Signals
    ax1.plot(df['timestamp'], df['close'], label='Close Price', color='blue')
    ax1.scatter(df['timestamp'][df['Signal'] == 'BUY'], 
                df['close'][df['Signal'] == 'BUY'], color='green', label='Buy Signal', marker='^', s=100)
    ax1.scatter(df['timestamp'][df['Signal'] == 'SELL'], 
                df['close'][df['Signal'] == 'SELL'], color='red', label='Sell Signal', marker='v', s=100)
    ax1.set_title('Crypto Price with RSI Buy/Sell Signals')
    ax1.legend()

    # Plot RSI
    ax2.plot(df['timestamp'], df['RSI'], label='RSI', color='purple')
    ax2.axhline(30, color='green', linestyle='--', label='Oversold (30)')
    ax2.axhline(70, color='red', linestyle='--', label='Overbought (70)')
    ax2.set_title('Relative Strength Index (RSI)')
    ax2.legend()

    plt.tight_layout()
    plt.show()

# Plot the signals
plot_rsi_signals(data)


"""
Overview: Bollinger Bands 

it consists of:
Middle Band: 20-period Simple Moving Average (SMA).
Upper Band: SMA + (2 * Standard Deviation).
Lower Band: SMA - (2 * Standard Deviation).

Signals:
Buy: When the price touches or drops below the Lower Band (oversold condition).
Sell: When the price touches or exceeds the Upper Band (overbought condition).
"""
import ccxt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to fetch historical data
def fetch_historical_data(symbol='BTC/USDT', timeframe='1h', limit=100):
    binance = ccxt.binance({
        'rateLimit': 1200,
        'enableRateLimit': True,
    })
    ohlcv = binance.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# Fetch historical data
symbol = 'BTC/USDT'  # Change to other symbols like 'ETH/USDT'
timeframe = '1h'
data = fetch_historical_data(symbol, timeframe)
print(data.head())

# Function to calculate Bollinger Bands
def calculate_bollinger_bands(df, period=20):
    df['SMA'] = df['close'].rolling(window=period).mean()
    df['STD'] = df['close'].rolling(window=period).std()
    df['Upper Band'] = df['SMA'] + (2 * df['STD'])
    df['Lower Band'] = df['SMA'] - (2 * df['STD'])
    return df

# Calculate Bollinger Bands
data = calculate_bollinger_bands(data)
print(data[['timestamp', 'close', 'SMA', 'Upper Band', 'Lower Band']].tail())

# Function to generate buy/sell signals
def generate_bollinger_signals(df):
    df['Signal'] = None
    for i in range(len(df)):
        if df['close'][i] <= df['Lower Band'][i]:
            df['Signal'][i] = 'BUY'
        elif df['close'][i] >= df['Upper Band'][i]:
            df['Signal'][i] = 'SELL'
    return df

# Generate signals
data = generate_bollinger_signals(data)
print(data[['timestamp', 'close', 'Signal']].tail())

# Function to plot Bollinger Bands with Buy/Sell signals
def plot_bollinger_bands(df):
    plt.figure(figsize=(12, 8))
    
    # Plot Closing Price
    plt.plot(df['timestamp'], df['close'], label='Close Price', color='blue')
    
    # Plot Bollinger Bands
    plt.plot(df['timestamp'], df['Upper Band'], label='Upper Band', color='red', linestyle='--')
    plt.plot(df['timestamp'], df['Lower Band'], label='Lower Band', color='green', linestyle='--')
    plt.plot(df['timestamp'], df['SMA'], label='SMA (20)', color='orange', linestyle='--')
    
    # Plot Buy/Sell signals
    plt.scatter(df['timestamp'][df['Signal'] == 'BUY'], 
                df['close'][df['Signal'] == 'BUY'], color='green', label='Buy Signal', marker='^', s=100)
    plt.scatter(df['timestamp'][df['Signal'] == 'SELL'], 
                df['close'][df['Signal'] == 'SELL'], color='red', label='Sell Signal', marker='v', s=100)
    
    plt.title('Bollinger Bands Analysis with Buy/Sell Signals')
    plt.xlabel('Timestamp')
    plt.ylabel('Price')
    plt.legend()
    plt.tight_layout()
    plt.show()

# Plot the Bollinger Bands and signals
plot_bollinger_bands(data)

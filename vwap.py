"""
VWAP(Volume Weighted Average Price) is a widely used trading indicator that combines price and volume 
to determine a fair market value during a trading session.

The VWAP Strategy helps traders:
Buy Signal: Price moves below VWAP (potential undervaluation).
Sell Signal: Price moves above VWAP (potential overvaluation).
"""

import ccxt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to fetch historical crypto data
def fetch_historical_data(symbol='BTC/USDT', timeframe='1h', limit=100):
    binance = ccxt.binance({
        'rateLimit': 1200,
        'enableRateLimit': True,
    })
    ohlcv = binance.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')  # Convert timestamp
    return df

# Fetch data
symbol = 'BTC/USDT'  # Choose cryptocurrency pair
timeframe = '15m'    # 15-minute timeframe
data = fetch_historical_data(symbol, timeframe)
print(data.head())

# Function to calculate VWAP
def calculate_vwap(df):
    # Calculate the Typical Price
    df['Typical Price'] = (df['high'] + df['low'] + df['close']) / 3
    
    # Calculate Cumulative Volume and Cumulative Volume-Weighted Price
    df['Cum_Volume'] = df['volume'].cumsum()
    df['Cum_Typical_Price_Volume'] = (df['Typical Price'] * df['volume']).cumsum()
    
    # Calculate VWAP
    df['VWAP'] = df['Cum_Typical_Price_Volume'] / df['Cum_Volume']
    return df

# Calculate VWAP
data = calculate_vwap(data)
print(data[['timestamp', 'close', 'Typical Price', 'VWAP']].tail())

# Function to generate buy/sell signals based on VWAP
def generate_vwap_signals(df):
    df['Signal'] = None
    for i in range(1, len(df)):
        if df['close'][i] > df['VWAP'][i] and df['close'][i-1] <= df['VWAP'][i-1]:
            df['Signal'][i] = 'SELL'
        elif df['close'][i] < df['VWAP'][i] and df['close'][i-1] >= df['VWAP'][i-1]:
            df['Signal'][i] = 'BUY'
    return df

# Generate signals
data = generate_vwap_signals(data)
print(data[['timestamp', 'close', 'VWAP', 'Signal']].tail())

# Function to plot VWAP with Buy/Sell signals
def plot_vwap_signals(df):
    plt.figure(figsize=(12, 8))
    
    # Plot Closing Price and VWAP
    plt.plot(df['timestamp'], df['close'], label='Close Price', color='blue')
    plt.plot(df['timestamp'], df['VWAP'], label='VWAP', color='orange', linestyle='--')
    
    # Plot Buy Signals
    plt.scatter(df['timestamp'][df['Signal'] == 'BUY'], 
                df['close'][df['Signal'] == 'BUY'], color='green', label='BUY', marker='^', s=100)
    
    # Plot Sell Signals
    plt.scatter(df['timestamp'][df['Signal'] == 'SELL'], 
                df['close'][df['Signal'] == 'SELL'], color='red', label='SELL', marker='v', s=100)
    
    # Labels and Legend
    plt.title('VWAP Strategy with Buy/Sell Signals')
    plt.xlabel('Timestamp')
    plt.ylabel('Price')
    plt.legend()
    plt.tight_layout()
    plt.show()

# Plot VWAP and Signals
plot_vwap_signals(data)


"""
Fibonacci Retracement Bot for Crypto Trading
A Fibonacci Retracement Bot identifies potential support and resistance levels 
based on Fibonacci ratios (23.6%, 38.2%, 50%, 61.8%, 78.6%) during uptrends or downtrends. 
It helps traders pinpoint buy/sell signals when price reacts to these levels.
"""

import ccxt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Initialize Binance API (Public access)
def fetch_historical_data(symbol='BTC/USDT', timeframe='1h', limit=100):
    binance = ccxt.binance({
        'rateLimit': 1200,
        'enableRateLimit': True,
    })
    ohlcv = binance.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')  # Convert to datetime
    return df

# Fetch data
symbol = 'BTC/USDT'  # You can use any crypto pair
timeframe = '1h'     # 1-hour timeframe
data = fetch_historical_data(symbol, timeframe)
print(data.head())

def find_swing_high_low(df):
    swing_high = df['high'].max()  # Highest price
    swing_low = df['low'].min()    # Lowest price
    return swing_high, swing_low

swing_high, swing_low = find_swing_high_low(data)
print(f"Swing High: {swing_high}, Swing Low: {swing_low}")


def calculate_fibonacci_levels(swing_high, swing_low):
    ratios = [0.236, 0.382, 0.5, 0.618, 0.786]
    levels = {f"Level {int(ratio*100)}%": swing_high - (ratio * (swing_high - swing_low)) for ratio in ratios}
    levels['Swing High'] = swing_high
    levels['Swing Low'] = swing_low
    return levels

fib_levels = calculate_fibonacci_levels(swing_high, swing_low)
print("Fibonacci Levels:")
for level, price in fib_levels.items():
    print(f"{level}: {price:.2f}")

def plot_fibonacci_levels(df, fib_levels):
    plt.figure(figsize=(12, 8))
    
    # Plot price action
    plt.plot(df['timestamp'], df['close'], label='Close Price', color='blue')
    
    # Add Fibonacci levels
    for level, price in fib_levels.items():
        plt.axhline(y=price, color='grey', linestyle='--', label=f"{level} - {price:.2f}")
    
    plt.title('Fibonacci Retracement Levels with Price Action')
    plt.xlabel('Timestamp')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

plot_fibonacci_levels(data, fib_levels)

def identify_signals(df, fib_levels):
    signals = []
    for i in range(1, len(df)):
        for level, price in fib_levels.items():
            if level in ['Swing High', 'Swing Low']:
                continue  # Ignore extremes
            # Buy signal (bounce at support)
            if df['low'][i] <= price <= df['close'][i] and df['close'][i] > df['close'][i-1]:
                signals.append((df['timestamp'][i], df['close'][i], 'BUY', level))
            # Sell signal (rejection at resistance)
            elif df['high'][i] >= price >= df['close'][i] and df['close'][i] < df['close'][i-1]:
                signals.append((df['timestamp'][i], df['close'][i], 'SELL', level))
    return signals

signals = identify_signals(data, fib_levels)
for signal in signals:
    print(f"{signal[0]} - {signal[2]} at {signal[3]}: ${signal[1]:.2f}")


def plot_with_signals(df, fib_levels, signals):
    plt.figure(figsize=(12, 8))
    plt.plot(df['timestamp'], df['close'], label='Close Price', color='blue')

    # Add Fibonacci levels
    for level, price in fib_levels.items():
        plt.axhline(y=price, color='grey', linestyle='--', label=f"{level} - {price:.2f}")

    # Plot signals
    for signal in signals:
        color = 'green' if signal[2] == 'BUY' else 'red'
        plt.scatter(signal[0], signal[1], color=color, s=100, label=f"{signal[2]} at {signal[3]}")

    plt.title('Fibonacci Retracement Levels with Buy/Sell Signals')
    plt.xlabel('Timestamp')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

plot_with_signals(data, fib_levels, signals)

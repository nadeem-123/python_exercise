import ccxt
import pandas as pd
import matplotlib.pyplot as plt
import time

# Initialize Binance
def fetch_historical_data(symbol='BTC/USDT', timeframe='1h', limit=100):
    binance = ccxt.binance({
        'rateLimit': 1200,
        'enableRateLimit': True,
    })
    # Fetch OHLCV (Open, High, Low, Close, Volume) data
    ohlcv = binance.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')  # Convert to readable format
    return df

# Fetch data
data = fetch_historical_data()
print(data.head())

# Function to calculate MACD and Signal
def calculate_macd(df):
    df['EMA_12'] = df['close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    return df

data = calculate_macd(data)
print(data[['timestamp', 'close', 'MACD', 'Signal']].tail())


# Generate Buy/Sell Signals
def generate_signals(df):
    df['Signal_Type'] = None
    for i in range(1, len(df)):
        if df['MACD'][i] > df['Signal'][i] and df['MACD'][i-1] <= df['Signal'][i-1]:
            df['Signal_Type'][i] = 'BUY'
        elif df['MACD'][i] < df['Signal'][i] and df['MACD'][i-1] >= df['Signal'][i-1]:
            df['Signal_Type'][i] = 'SELL'
    return df

data = generate_signals(data)
print(data[['timestamp', 'close', 'MACD', 'Signal', 'Signal_Type']].tail())


# Plot MACD, Signal, and Buy/Sell Signals
def plot_macd(df):
    plt.figure(figsize=(12, 8))
    
    # Plot closing price
    plt.subplot(2, 1, 1)
    plt.plot(df['timestamp'], df['close'], label='Close Price', color='blue')
    plt.scatter(df['timestamp'][df['Signal_Type'] == 'BUY'], 
                df['close'][df['Signal_Type'] == 'BUY'], color='green', label='Buy Signal', marker='^', s=100)
    plt.scatter(df['timestamp'][df['Signal_Type'] == 'SELL'], 
                df['close'][df['Signal_Type'] == 'SELL'], color='red', label='Sell Signal', marker='v', s=100)
    plt.title('Crypto Price and Buy/Sell Signals')
    plt.legend()
    
    # Plot MACD and Signal
    plt.subplot(2, 1, 2)
    plt.plot(df['timestamp'], df['MACD'], label='MACD', color='purple')
    plt.plot(df['timestamp'], df['Signal'], label='Signal Line', color='orange')
    plt.fill_between(df['timestamp'], df['MACD'] - df['Signal'], 0, color='grey', alpha=0.2)
    plt.title('MACD and Signal Line')
    plt.legend()
    
    plt.tight_layout()
    plt.show()

plot_macd(data)


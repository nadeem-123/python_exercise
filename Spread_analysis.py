import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from binance.client import Client
from datetime import datetime
import time

# Binance API setup
api_key = 'U86UbldzHy7Wn07Wek9BeTjfM7BukG6uXb6kJFJJzo7EK9pm8WDSY25hoEBTzTYH'
api_secret = 'NEe9sJxG7QSRaJbHXz1b3klPo7ObaVmiz9yYdlkVYY1xwwf0Ex6d3w6qFBwuxdSE'
client = Client(api_key, api_secret)

# Fetch bid and ask data
def fetch_bid_ask(symbol="BTCUSDT"):
    """
    Fetches the highest bid and lowest ask from Binance order book.
    
    Parameters:
    symbol : str : Trading pair symbol (default: "BTCUSDT").
    
    Returns:
    dict : A dictionary containing bid, ask, and spread values.
    """
    order_book = client.get_order_book(symbol=symbol, limit=5)
    highest_bid = float(order_book['bids'][0][0])  # Price of highest bid
    lowest_ask = float(order_book['asks'][0][0])  # Price of lowest ask
    spread = lowest_ask - highest_bid             # Bid-ask spread
    
    return {
        "bid": highest_bid,
        "ask": lowest_ask,
        "spread": spread
    }

# Collect spread data over time
def collect_spread_data(symbol="BTCUSDT", duration=60, interval=5):
    """
    Collects bid, ask, and spread data over time.
    
    Parameters:
    symbol : str : Trading pair symbol (default: "BTCUSDT").
    duration : int : Total time to collect data in seconds.
    interval : int : Time interval between data fetches in seconds.
    
    Returns:
    pd.DataFrame : DataFrame containing the collected data.
    """
    data = []
    start_time = datetime.now()

    try:
        while (datetime.now() - start_time).seconds < duration:
            bid_ask_data = fetch_bid_ask(symbol)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data.append([timestamp, bid_ask_data['bid'], bid_ask_data['ask'], bid_ask_data['spread']])
            print(f"{timestamp} - Bid: {bid_ask_data['bid']}, Ask: {bid_ask_data['ask']}, Spread: {bid_ask_data['spread']}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nData collection interrupted by the user.")
    
    # Create a DataFrame
    return pd.DataFrame(data, columns=["Timestamp", "Bid", "Ask", "Spread"])

# Plot spread analysis
def plot_spread_analysis(data):
    """
    Plots the bid-ask spread over time.
    
    Parameters:
    data : pd.DataFrame : DataFrame containing bid, ask, and spread data.
    """
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])  # Convert to datetime for better plotting

    plt.figure(figsize=(12, 6))

    # Plot spread
    plt.plot(data['Timestamp'], data['Spread'], label='Spread', color='red', marker='o', alpha=0.7)

    # Highlight bid and ask levels
    plt.plot(data['Timestamp'], data['Bid'], label='Bid Price', linestyle='--', alpha=0.6)
    plt.plot(data['Timestamp'], data['Ask'], label='Ask Price', linestyle='--', alpha=0.6)

    # Labels and title
    plt.title("Bid-Ask Spread Analysis Over Time", fontsize=16)
    plt.xlabel("Time", fontsize=12)
    plt.ylabel("Price / Spread", fontsize=12)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

# Main script
if __name__ == "__main__":
    symbol = "BTCUSDT"  # Trading pair
    duration = 60       # Collect data for 60 seconds
    interval = 5       # Fetch data every 5 seconds

    # Collect spread data
    spread_data = collect_spread_data(symbol, duration, interval)

    # Save the collected data to a CSV file
    spread_data.to_csv("spread_data.csv", index=False)
    print("Data saved to 'spread_data.csv'.")

    # Plot spread analysis
    plot_spread_analysis(spread_data)
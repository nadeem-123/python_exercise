import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from binance.client import Client
import time

# Binance API setup
api_key = 'U86UbldzHy7Wn07Wek9BeTjfM7BukG6uXb6kJFJJzo7EK9pm8WDSY25hoEBTzTYH'
api_secret = 'NEe9sJxG7QSRaJbHXz1b3klPo7ObaVmiz9yYdlkVYY1xwwf0Ex6d3w6qFBwuxdSE'
client = Client(api_key, api_secret)

def fetch_order_book(symbol="BTCUSDT", limit=10):
    """
    Fetches the order book from Binance for the given trading pair.
    
    Parameters:
    symbol : str : Trading pair symbol (default: "BTCUSDT").
    limit : int : Number of levels in the order book (default: 10).
    
    Returns:
    pd.DataFrame : DataFrame containing bid and ask prices with volumes.
    """
    order_book = client.get_order_book(symbol=symbol, limit=limit)
    bids = pd.DataFrame(order_book['bids'], columns=['Price', 'Volume'], dtype=float)
    asks = pd.DataFrame(order_book['asks'], columns=['Price', 'Volume'], dtype=float)
    return bids, asks

def simulate_trade_impact(order_book, trade_volume, trade_type="buy"):
    """
    Simulates the market impact of a large trade.
    
    Parameters:
    order_book : pd.DataFrame : Order book data (bids or asks).
    trade_volume : float : Volume of the trade.
    trade_type : str : "buy" or "sell".
    
    Returns:
    float : The price impact caused by the trade.
    """
    remaining_volume = trade_volume
    total_cost = 0
    for _, row in order_book.iterrows():
        level_price = row['Price']
        level_volume = row['Volume']
        
        if remaining_volume <= level_volume:
            total_cost += remaining_volume * level_price
            break
        else:
            total_cost += level_volume * level_price
            remaining_volume -= level_volume
    
    avg_trade_price = total_cost / trade_volume
    initial_price = order_book.iloc[0]['Price']
    price_impact = avg_trade_price - initial_price if trade_type == "buy" else initial_price - avg_trade_price
    
    return avg_trade_price, price_impact

def market_impact_analysis(symbol="BTCUSDT", trade_volumes=[1, 5, 10], trade_type="buy"):
    """
    Analyzes the market impact for a range of trade volumes.
    
    Parameters:
    symbol : str : Trading pair symbol (default: "BTCUSDT").
    trade_volumes : list : List of trade volumes to simulate.
    trade_type : str : "buy" or "sell".
    
    Returns:
    pd.DataFrame : DataFrame containing market impact analysis results.
    """
    bids, asks = fetch_order_book(symbol)
    order_book = asks if trade_type == "buy" else bids
    results = []
    
    for volume in trade_volumes:
        avg_price, impact = simulate_trade_impact(order_book, volume, trade_type)
        results.append({"Trade Volume": volume, "Average Price": avg_price, "Price Impact": impact})
    
    return pd.DataFrame(results)

def plot_market_impact(results):
    """
    Plots the market impact as a function of trade volume.
    
    Parameters:
    results : pd.DataFrame : DataFrame containing market impact results.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(results["Trade Volume"], results["Price Impact"], marker='o', label="Price Impact")
    plt.title("Market Impact Analysis")
    plt.xlabel("Trade Volume")
    plt.ylabel("Price Impact")
    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    symbol = "BTCUSDT"  # Trading pair
    trade_volumes = [1, 5, 10, 20, 50]  # Trade volumes to simulate
    trade_type = "buy"  # "buy" or "sell"

    # Analyze market impact
    results = market_impact_analysis(symbol, trade_volumes, trade_type)
    print(results)

    # Visualize the results
    plot_market_impact(results)

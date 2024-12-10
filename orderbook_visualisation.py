
import pandas as pd
import matplotlib.pyplot as plt
from binance.client import Client
from datetime import datetime

# Binance API setup
api_key = 'U86UbldzHy7Wn07Wek9BeTjfM7BukG6uXb6kJFJJzo7EK9pm8WDSY25hoEBTzTYH'
api_secret = 'NEe9sJxG7QSRaJbHXz1b3klPo7ObaVmiz9yYdlkVYY1xwwf0Ex6d3w6qFBwuxdSE'
client = Client(api_key, api_secret)

# Fetch order book data
def fetch_order_book(symbol="BTCUSDT", limit=10):
    """
    Fetches the order book from Binance for the given trading pair.
    """
    order_book = client.get_order_book(symbol=symbol, limit=limit)
    bids = pd.DataFrame(order_book['bids'], columns=['Price', 'Volume'], dtype=float)
    asks = pd.DataFrame(order_book['asks'], columns=['Price', 'Volume'], dtype=float)
    return bids, asks

# Plot order book
def plot_order_book(bids, asks):
    """
    Plots the order book using bid and ask data, with date and time in the title.
    """
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    plt.figure(figsize=(10, 6))

    # Plot bids and asks
    plt.barh(bids['Price'], bids['Volume'], color='green', label='Bids', alpha=0.7)
    plt.barh(asks['Price'], asks['Volume'], color='red', label='Asks', alpha=0.7)

    # Highlight bid-ask spread
    highest_bid = bids['Price'].max()
    lowest_ask = asks['Price'].min()
    plt.axhline(y=highest_bid, color='blue', linestyle='--', label=f'Highest Bid: {highest_bid}')
    plt.axhline(y=lowest_ask, color='purple', linestyle='--', label=f'Lowest Ask: {lowest_ask}')

    # Labels and title with date and time
    plt.xlabel('Volume')
    plt.ylabel('Price')
    plt.title(f'Real-Time Order Book Visualization\n{current_time}')
    plt.legend()
    plt.grid()

    plt.show()

# Main script
if __name__ == "__main__":
    symbol = "BTCUSDT"  # Trading pair
    limit = 10          # Number of levels to fetch
    bids, asks = fetch_order_book(symbol, limit)
    plot_order_book(bids, asks)

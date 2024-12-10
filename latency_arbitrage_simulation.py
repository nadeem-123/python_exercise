import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from datetime import datetime

def generate_market_data(base_price=100, volatility=1, steps=100):
    """
    Generates simulated market price data.
    
    Parameters:
    base_price : float : Starting price.
    volatility : float : Standard deviation of price changes.
    steps : int : Number of price updates.
    
    Returns:
    np.ndarray : Simulated price data.
    """
    np.random.seed(42)
    return np.cumsum(np.random.normal(0, volatility, steps)) + base_price

def simulate_latency(data, delay=2):
    """
    Simulates latency by delaying updates in the data.
    
    Parameters:
    data : np.ndarray : Price data.
    delay : int : Number of steps to delay.
    
    Returns:
    np.ndarray : Delayed price data.
    """
    delayed_data = np.roll(data, delay)
    delayed_data[:delay] = data[0]  # Fill initial values to avoid NaN
    return delayed_data

def detect_arbitrage(prices_a, prices_b, threshold=0.5):
    """
    Detects arbitrage opportunities between two price streams.
    
    Parameters:
    prices_a : np.ndarray : Prices from market A.
    prices_b : np.ndarray : Prices from market B.
    threshold : float : Minimum price difference to trigger an arbitrage signal.
    
    Returns:
    pd.DataFrame : DataFrame containing arbitrage opportunities.
    """
    arbitrage_signals = []
    for i in range(len(prices_a)):
        diff = prices_a[i] - prices_b[i]
        if abs(diff) > threshold:
            arbitrage_signals.append((i, prices_a[i], prices_b[i], diff))
    
    return pd.DataFrame(arbitrage_signals, columns=["Index", "Price_A", "Price_B", "Difference"])

def simulate_trading(arbitrage_opportunities, trade_size=1):
    """
    Simulates trading based on arbitrage opportunities.
    
    Parameters:
    arbitrage_opportunities : pd.DataFrame : DataFrame of arbitrage opportunities.
    trade_size : float : Size of each trade (in units).
    
    Returns:
    float : Total profit from simulated trades.
    """
    total_profit = 0
    for _, row in arbitrage_opportunities.iterrows():
        total_profit += abs(row["Difference"]) * trade_size
    return total_profit


def plot_arbitrage(prices_a, prices_b, arbitrage_opportunities):
    """
    Plots price streams and highlights arbitrage opportunities.
    
    Parameters:
    prices_a : np.ndarray : Prices from market A.
    prices_b : np.ndarray : Prices from market B.
    arbitrage_opportunities : pd.DataFrame : DataFrame of arbitrage opportunities.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(prices_a, label="Market A Prices", alpha=0.7)
    plt.plot(prices_b, label="Market B Prices", alpha=0.7)
    plt.scatter(arbitrage_opportunities["Index"], 
                arbitrage_opportunities["Price_A"], 
                color="red", label="Arbitrage Opportunity", alpha=0.7)
    plt.title("Latency Arbitrage Simulation")
    plt.xlabel("Time Step")
    plt.ylabel("Price")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Simulate price data for two markets
    steps = 100
    base_price = 100
    volatility = 1
    latency_delay = 2
    arbitrage_threshold = 0.5
    
    prices_a = generate_market_data(base_price, volatility, steps)
    prices_b = simulate_latency(prices_a, delay=latency_delay)
    
    # Detect arbitrage opportunities
    arbitrage_opportunities = detect_arbitrage(prices_a, prices_b, threshold=arbitrage_threshold)
    print("Arbitrage Opportunities:\n", arbitrage_opportunities)
    
    # Simulate trading
    trade_size = 1
    total_profit = simulate_trading(arbitrage_opportunities, trade_size)
    print(f"Total Profit from Arbitrage: {total_profit:.2f}")
    
    # Visualize results
    plot_arbitrage(prices_a, prices_b, arbitrage_opportunities)

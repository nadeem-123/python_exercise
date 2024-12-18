"""Project Overview: This project will simulate the performance of various options 
trading strategies (e.g., straddle, strangle, bull call spread) using historical data. 
It will calculate profit and loss (P&L), visualize results, and evaluate strategy performance.

Input: Historical options data or simulated data.

Strategies:
Straddle: Buy call and put at the same strike price.
Strangle: Buy call and put at different strike prices.
Bull Call Spread: Buy a call and sell a higher strike call.
Others can be added as extensions.

Output:
P&L for each strategy.
Visual representation of performance.
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from scipy.stats import norm

def fetch_historical_data(ticker, start, end):
    """
    Fetch historical price data for the given ticker.
    
    Parameters:
        ticker (str): Stock/ETF ticker (e.g., "AAPL", "SPY").
        start (str): Start date (YYYY-MM-DD).
        end (str): End date (YYYY-MM-DD).
    
    Returns:
        DataFrame: Historical price data.
    """
    data = yf.download(ticker, start=start, end=end)
    data['Mid Price'] = (data['High'] + data['Low']) / 2  # Calculate mid-price
    return data

# Example usage
ticker = "CXM"
data = fetch_historical_data(ticker, start="2023-01-01", end="2023-12-31")
print(data.head())

def simulate_option_price(S, K, T, r, sigma, option_type="call"):
    """
    Simulate option price using Black-Scholes formula.
    
    Parameters:
        S (float): Current stock price.
        K (float): Strike price.
        T (float): Time to expiration (in years).
        r (float): Risk-free rate.
        sigma (float): Volatility of the underlying asset.
        option_type (str): "call" or "put".
    
    Returns:
        float: Simulated option price.
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == "call":
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == "put":
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type")
    
    return price

# Simulate option prices for a range of strikes
data['Call Price'] = simulate_option_price(S=data['Mid Price'], K=150, T=0.1, r=0.01, sigma=0.2, option_type="call")
data['Put Price'] = simulate_option_price(S=data['Mid Price'], K=150, T=0.1, r=0.01, sigma=0.2, option_type="put")
print(data[['Mid Price', 'Call Price', 'Put Price']].head())

def straddle_pnl(data, strike_price):
    """
    Calculate P&L for a straddle strategy.
    
    Parameters:
        data (DataFrame): Historical data with mid prices.
        strike_price (float): Strike price of the options.
    
    Returns:
        Series: P&L for the straddle.
    """
    call_pnl = np.maximum(data['Mid Price'] - strike_price, 0) - data['Call Price']
    put_pnl = np.maximum(strike_price - data['Mid Price'], 0) - data['Put Price']
    return call_pnl + put_pnl

data['Straddle PnL'] = straddle_pnl(data, strike_price=150)

def strangle_pnl(data, lower_strike, upper_strike):
    """
    Calculate P&L for a strangle strategy.
    
    Parameters:
        data (DataFrame): Historical data with mid prices.
        lower_strike (float): Lower strike price of the put option.
        upper_strike (float): Upper strike price of the call option.
    
    Returns:
        Series: P&L for the strangle.
    """
    call_pnl = np.maximum(data['Mid Price'] - upper_strike, 0) - data['Call Price']
    put_pnl = np.maximum(lower_strike - data['Mid Price'], 0) - data['Put Price']
    return call_pnl + put_pnl

data['Strangle PnL'] = strangle_pnl(data, lower_strike=140, upper_strike=160)

def bull_call_spread_pnl(data, lower_strike, upper_strike):
    """
    Calculate P&L for a bull call spread strategy.
    
    Parameters:
        data (DataFrame): Historical data with mid prices.
        lower_strike (float): Strike price of the long call.
        upper_strike (float): Strike price of the short call.
    
    Returns:
        Series: P&L for the bull call spread.
    """
    long_call_pnl = np.maximum(data['Mid Price'] - lower_strike, 0) - data['Call Price']
    short_call_pnl = -np.maximum(data['Mid Price'] - upper_strike, 0)
    return long_call_pnl + short_call_pnl

data['Bull Call Spread PnL'] = bull_call_spread_pnl(data, lower_strike=140, upper_strike=160)

def plot_strategy_pnl(data):
    plt.figure(figsize=(12, 8))
    
    plt.plot(data.index, data['Straddle PnL'], label='Straddle', color='blue')
    plt.plot(data.index, data['Strangle PnL'], label='Strangle', color='green')
    plt.plot(data.index, data['Bull Call Spread PnL'], label='Bull Call Spread', color='red')
    
    plt.title('Options Strategy P&L Over Time')
    plt.xlabel('Date')
    plt.ylabel('Profit/Loss')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

plot_strategy_pnl(data)


"""
Objective: Analyze historical futures contract data and backtest trading strategies like momentum or mean reversion.

Key Features:
Fetch historical futures prices.
Implement and backtest trading strategies.
Calculate performance metrics: P&L, Sharpe Ratio, Max Drawdown.
Visualize strategy performance.

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

def fetch_futures_data(ticker, start, end, margin_rate=0.1):
    """
    Fetch historical futures price data based on underlying asset data.
    
    Parameters:
        ticker (str): Underlying asset ticker (e.g., "CL=F" for crude oil).
        start (str): Start date (YYYY-MM-DD).
        end (str): End date (YYYY-MM-DD).
        margin_rate (float): Margin rate for futures (default is 10%).
    
    Returns:
        DataFrame: Historical price data with futures margin-based P&L.
    """
    data = yf.download(ticker, start=start, end=end)
    data['Futures Price'] = data['Adj Close'] / margin_rate  # Simulate futures price
    return data

# Example usage
ticker = "AAPL"  # Replace with a futures ticker
start_date = "2023-01-01"
end_date = "2023-12-31"
data = fetch_futures_data(ticker, start=start_date, end=end_date)
print(data.head())

def momentum_strategy(data, window=20):
    """
    Implement a simple momentum strategy.
    
    Parameters:
        data (DataFrame): Historical price data.
        window (int): Lookback window for the moving average.
    
    Returns:
        DataFrame: Data with momentum signals and P&L.
    """
    data['SMA'] = data['Futures Price'].rolling(window=window).mean()
    data['Signal'] = np.where(data['Futures Price'] > data['SMA'], 1, -1)  # 1 for long, -1 for short
    data['Daily Returns'] = data['Futures Price'].pct_change()
    data['Strategy Returns'] = data['Signal'].shift(1) * data['Daily Returns']  # Use previous signal
    return data

data = momentum_strategy(data)
print(data[['Futures Price', 'SMA', 'Signal', 'Strategy Returns']].tail())

def mean_reversion_strategy(data, window=20, threshold=0.02):
    """
    Implement a mean reversion strategy.
    
    Parameters:
        data (DataFrame): Historical price data.
        window (int): Lookback window for the moving average.
        threshold (float): Threshold for deviation from the moving average.
    
    Returns:
        DataFrame: Data with mean reversion signals and P&L.
    """
    data['SMA'] = data['Futures Price'].rolling(window=window).mean()
    data['Deviation'] = (data['Futures Price'] - data['SMA']) / data['SMA']
    data['Signal'] = np.where(data['Deviation'] < -threshold, 1, 
                              np.where(data['Deviation'] > threshold, -1, 0))
    data['Daily Returns'] = data['Futures Price'].pct_change()
    data['Strategy Returns'] = data['Signal'].shift(1) * data['Daily Returns']  # Use previous signal
    return data

data = mean_reversion_strategy(data)
print(data[['Futures Price', 'SMA', 'Deviation', 'Signal', 'Strategy Returns']].tail())

def calculate_sharpe_ratio(strategy_returns, risk_free_rate=0.01):
    """
    Calculate the Sharpe Ratio for a strategy.
    
    Parameters:
        strategy_returns (Series): Daily returns of the strategy.
        risk_free_rate (float): Annualized risk-free rate.
    
    Returns:
        float: Sharpe Ratio.
    """
    excess_returns = strategy_returns.mean() * 252 - risk_free_rate
    volatility = strategy_returns.std() * np.sqrt(252)
    sharpe_ratio = excess_returns / volatility
    return sharpe_ratio

def calculate_max_drawdown(cumulative_returns):
    """
    Calculate the maximum drawdown for a strategy.
    
    Parameters:
        cumulative_returns (Series): Cumulative returns of the strategy.
    
    Returns:
        float: Maximum drawdown.
    """
    peak = cumulative_returns.cummax()
    drawdown = (cumulative_returns - peak) / peak
    max_drawdown = drawdown.min()
    return max_drawdown

def plot_strategy_performance(data):
    """
    Plot the strategy's performance.
    
    Parameters:
        data (DataFrame): Data with strategy returns and cumulative performance.
    """
    data['Cumulative Strategy Returns'] = (1 + data['Strategy Returns']).cumprod()
    data['Cumulative Market Returns'] = (1 + data['Daily Returns']).cumprod()
    
    plt.figure(figsize=(12, 8))
    plt.plot(data.index, data['Cumulative Strategy Returns'], label='Strategy Returns', color='blue')
    plt.plot(data.index, data['Cumulative Market Returns'], label='Market Returns', color='orange')
    plt.title('Strategy vs. Market Performance')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Returns')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

plot_strategy_performance(data)

# Parameters
margin_rate = 0.1
window = 20
threshold = 0.02

# Fetch data and implement strategies
data = fetch_futures_data(ticker="AAPL", start=start_date, end=end_date, margin_rate=margin_rate)
data = momentum_strategy(data, window=window)

# Calculate performance metrics
sharpe_ratio = calculate_sharpe_ratio(data['Strategy Returns'])
max_drawdown = calculate_max_drawdown((1 + data['Strategy Returns']).cumprod())

# Print metrics
print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
print(f"Maximum Drawdown: {max_drawdown:.2%}")

# Visualize performance
plot_strategy_performance(data)


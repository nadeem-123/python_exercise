'''
"Portfolio Optimization Using Python"
This project demonstrates how to optimize a portfolio of assets to achieve the best risk-return trade-off using Python. The tool calculates key portfolio metrics such as expected returns, risk (standard deviation), and the Sharpe ratio. It uses mathematical optimization to find the optimal asset weights that maximize the Sharpe ratio, representing the most efficient portfolio. The project also visualizes the Efficient Frontier, highlighting the trade-offs between risk and return for various portfolio combinations.

Key Features:

1. Calculates portfolio metrics like returns, risk, and Sharpe ratio.
2. Uses scipy.optimize for portfolio weight optimization.
3. Visualizes the Efficient Frontier to show optimal portfolios.
4. Simulates real-world financial data for practical insights.


About the Output
Efficient Frontier Plot
X-axis: Risk (Standard Deviation) of the portfolio.
Y-axis: Expected Return of the portfolio.
Curve: The frontier of optimal portfolios. Each point represents a portfolio with the best possible return for a given level of risk.'''

# Import Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Portfolio Performance Function
def portfolio_performance(weights, mean_returns, cov_matrix, risk_free_rate=0):
    returns = np.dot(weights, mean_returns)
    risk = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    sharpe_ratio = (returns - risk_free_rate) / risk
    return returns, risk, sharpe_ratio

# Negative Sharpe Ratio for Optimization
def negative_sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate=0):
    _, _, sharpe = portfolio_performance(weights, mean_returns, cov_matrix, risk_free_rate)
    return -sharpe

# Portfolio Optimization Function
def optimize_portfolio(mean_returns, cov_matrix, risk_free_rate=0):
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix, risk_free_rate)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})  # Sum of weights = 1
    bounds = tuple((0, 1) for _ in range(num_assets))  # No short selling
    result = minimize(negative_sharpe_ratio, 
                      num_assets * [1. / num_assets], 
                      args=args, 
                      method='SLSQP', 
                      bounds=bounds, 
                      constraints=constraints)
    return result

# Efficient Frontier Calculation
def efficient_frontier(mean_returns, cov_matrix, risk_free_rate=0):
    results = []
    for target_return in np.linspace(0.001, 0.002, 50):  # Adjust range based on data
        constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
                       {'type': 'eq', 'fun': lambda x: np.dot(x, mean_returns) - target_return}]
        result = minimize(lambda x: np.sqrt(np.dot(x.T, np.dot(cov_matrix, x))), 
                          len(mean_returns) * [1. / len(mean_returns)], 
                          method='SLSQP', 
                          bounds=[(0, 1)] * len(mean_returns), 
                          constraints=constraints)
        if result.success:
            results.append((result.fun, target_return))
    return np.array(results)

# Plot Efficient Frontier with Highlights
def plot_efficient_frontier_with_highlights(frontier, mean_returns, cov_matrix):
    # Efficient Frontier
    plt.plot(frontier[:, 0], frontier[:, 1], label='Efficient Frontier', linewidth=2)
    
    # Optimal Portfolio (Max Sharpe Ratio)
    optimal = optimize_portfolio(mean_returns, cov_matrix)
    opt_weights = optimal.x
    opt_return, opt_risk, opt_sharpe = portfolio_performance(opt_weights, mean_returns, cov_matrix)

    plt.scatter(opt_risk, opt_return, color='red', label=f'Optimal Portfolio (Sharpe: {opt_sharpe:.2f})', s=100, zorder=5)
    
    # Labels and Annotations
    plt.title('Efficient Frontier with Optimal Portfolio', fontsize=14)
    plt.xlabel('Risk (Standard Deviation)', fontsize=12)
    plt.ylabel('Return', fontsize=12)
    plt.legend()
    plt.grid(True)
    
    # Annotate Optimal Portfolio
    plt.annotate('Optimal Portfolio',
                 xy=(opt_risk, opt_return),
                 xytext=(opt_risk + 0.01, opt_return + 0.001),
                 arrowprops=dict(facecolor='black', arrowstyle='->'),
                 fontsize=10)
    
    # Show Plot
    plt.show()

# Main Code Flow
if __name__ == "__main__":
    # Simulated Stock Data
    np.random.seed(42)
    stocks = ['Stock A', 'Stock B', 'Stock C']
    returns = np.random.normal(0.001, 0.02, (1000, 3))  # 1000 days of random data
    data = pd.DataFrame(returns, columns=stocks)
    
    # Calculate Portfolio Metrics
    mean_returns = data.mean()
    cov_matrix = data.cov()

    # Generate Efficient Frontier Data
    frontier = efficient_frontier(mean_returns, cov_matrix)

    # Plot the Efficient Frontier with Highlights
    plot_efficient_frontier_with_highlights(frontier, mean_returns, cov_matrix)

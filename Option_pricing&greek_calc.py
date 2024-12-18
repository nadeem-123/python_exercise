"""
Options Pricing and Greeks Calculator. 
This project focuses on pricing European options using the Black-Scholes model and 
calculating their Greeks (Delta, Gamma, Vega, Theta, Rho).

Greeks measure sensitivity to various factors:

Delta: Sensitivity to the underlying price.
Gamma: Sensitivity of Delta to price changes.
Vega: Sensitivity to volatility.
Theta: Sensitivity to time decay.
Rho: Sensitivity to interest rates.

"""


import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

def black_scholes(S, K, T, r, sigma, option_type="call"):
    """
    Calculate the price of a European option using the Black-Scholes model.
    
    Parameters:
        S (float): Current stock price
        K (float): Strike price
        T (float): Time to maturity (in years)
        r (float): Risk-free interest rate
        sigma (float): Volatility of the underlying asset
        option_type (str): "call" or "put"
        
    Returns:
        float: Option price
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == "call":
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == "put":
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("Option type must be 'call' or 'put'")
    
    return price

def calculate_greeks(S, K, T, r, sigma, option_type="call"):
    """
    Calculate the Greeks of a European option.
    
    Parameters:
        S (float): Current stock price
        K (float): Strike price
        T (float): Time to maturity (in years)
        r (float): Risk-free interest rate
        sigma (float): Volatility of the underlying asset
        option_type (str): "call" or "put"
        
    Returns:
        dict: Greeks (Delta, Gamma, Vega, Theta, Rho)
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    delta = norm.cdf(d1) if option_type == "call" else -norm.cdf(-d1)
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T)
    theta = - (S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) - \
            (r * K * np.exp(-r * T) * norm.cdf(d2 if option_type == "call" else -d2))
    rho = K * T * np.exp(-r * T) * norm.cdf(d2 if option_type == "call" else -d2)
    
    return {
        "Delta": delta,
        "Gamma": gamma,
        "Vega": vega,
        "Theta": theta,
        "Rho": rho
    }

def main():
    print("European Option Pricing and Greeks Calculator")
    
    # User inputs
    S = float(input("Enter current stock price (S): "))
    K = float(input("Enter strike price (K): "))
    T = float(input("Enter time to maturity in years (T): "))
    r = float(input("Enter risk-free interest rate (r) in decimal (e.g., 0.05): "))
    sigma = float(input("Enter volatility (sigma) in decimal (e.g., 0.2): "))
    option_type = input("Enter option type ('call' or 'put'): ").lower()
    
    # Calculate option price and Greeks
    price = black_scholes(S, K, T, r, sigma, option_type)
    greeks = calculate_greeks(S, K, T, r, sigma, option_type)
    
    # Display results
    print(f"\nOption Price ({option_type.capitalize()}): {price:.2f}")
    print("Greeks:")
    for greek, value in greeks.items():
        print(f"  {greek}: {value:.2f}")

if __name__ == "__main__":
    main()

def plot_greeks(S_range, K, T, r, sigma, option_type="call"):
    deltas, gammas, vegas, thetas, rhos = [], [], [], [], []
    
    for S in S_range:
        greeks = calculate_greeks(S, K, T, r, sigma, option_type)
        deltas.append(greeks["Delta"])
        gammas.append(greeks["Gamma"])
        vegas.append(greeks["Vega"])
        thetas.append(greeks["Theta"])
        rhos.append(greeks["Rho"])
    
    plt.figure(figsize=(10, 6))
    plt.plot(S_range, deltas, label="Delta")
    plt.plot(S_range, gammas, label="Gamma")
    plt.plot(S_range, vegas, label="Vega")
    plt.plot(S_range, thetas, label="Theta")
    plt.plot(S_range, rhos, label="Rho")
    plt.title(f"Greeks for {option_type.capitalize()} Option")
    plt.xlabel("Stock Price (S)")
    plt.ylabel("Value")
    plt.legend()
    plt.grid()
    plt.show()

# Define range of stock prices
S_range = np.linspace(50, 150, 100)
plot_greeks(S_range, K=100, T=1, r=0.05, sigma=0.2, option_type="call")


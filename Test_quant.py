#libraries
import pandas as pd
import matplotlib.pyplot as plt
import os

# File paths
file_path = '/Users/mdnadeem/Documents/Python/nifty_data/Test data/NIFTY_2023-08-10.csv' #filepath of local csv file which needs to analyse
processed_data_path = '/Users/mdnadeem/Documents/Python/nifty_data/Test data/processed_straddle_data.csv' #Output file 1: saved in local storage
trade_results_path = '/Users/mdnadeem/Documents/Python/nifty_data/Test data/trade_results.csv' #Output file 2: saved in local storage
backtesting_results_path = '/Users/mdnadeem/Documents/Python/nifty_data/Test data/backtesting_results.csv' ##Output file 3: saved in local storage

# Load the CSV file
try:
    data = pd.read_csv(file_path)
    print("Data loaded successfully.")
except FileNotFoundError as e: #error handling
    print(f"File not found: {e}")
    exit()

# Step 1: Prepare the Data
data['timestamp'] = pd.to_datetime(data['timestamp'])
data.set_index('timestamp', inplace=True)

# Step 2: Calculate Synthetic ATM
def calculate_synthetic_atm(data):
    opening_data = data.between_time('09:15', '09:15')
    if opening_data.empty:
        print("No opening data found for '09:15'.")
        return None
    atm = opening_data['strike_price'].median()
    return round(atm, -2)

synthetic_atm = calculate_synthetic_atm(data)
if synthetic_atm is None:
    print("Synthetic ATM calculation failed.")
    exit()

# Step 3: Select Straddles Around ATM
def select_straddles(data, atm):
    strikes = [atm - 200, atm - 100, atm, atm + 100, atm + 200]
    return data[data['strike_price'].isin(strikes)]

selected_straddles = select_straddles(data, synthetic_atm)

# Step 4: Simulate Entry/Exit Logic
def simulate_entry_exit(data, indicator_threshold=1950):
    trades = []
    for timestamp, row in data.iterrows():
        if row['close'] < indicator_threshold:
            trades.append((timestamp, row['strike_price'], row['close'], "ENTRY"))
        elif row['close'] > indicator_threshold + 50:
            trades.append((timestamp, row['strike_price'], row['close'], "EXIT"))
    return trades

trades = simulate_entry_exit(selected_straddles)
trades_df = pd.DataFrame(trades, columns=['Timestamp', 'Strike Price', 'Price', 'Action'])

# Step 5: Calculate Profit/Loss for Each Trade
trades_df['PnL'] = 0
for i in range(1, len(trades_df)):
    if trades_df.iloc[i]['Action'] == 'EXIT' and trades_df.iloc[i - 1]['Action'] == 'ENTRY':
        trades_df.loc[i, 'PnL'] = trades_df.iloc[i]['Price'] - trades_df.iloc[i - 1]['Price']

# Step 6: Calculate Cumulative Metrics
trades_df['CumulativePnL'] = trades_df['PnL'].cumsum()

# Save Tabular Data to CSV
data.to_csv(processed_data_path)
trades_df.to_csv(trade_results_path)

# Step 7: Show Plot
plt.figure(figsize=(12, 6))
for strike in selected_straddles['strike_price'].unique():
    strike_data = selected_straddles[selected_straddles['strike_price'] == strike]
    plt.plot(strike_data.index, strike_data['close'], label=f"Strike {strike}")

# Highlight entry and exit trades
entry_trades = trades_df[trades_df['Action'] == 'ENTRY']
exit_trades = trades_df[trades_df['Action'] == 'EXIT']

plt.scatter(entry_trades['Timestamp'], entry_trades['Price'], color='green', label='Entry Trades', marker='^')
plt.scatter(exit_trades['Timestamp'], exit_trades['Price'], color='red', label='Exit Trades', marker='v')

plt.title("Straddle Prices with Entry and Exit Points")
plt.xlabel("Time")
plt.ylabel("Price")
plt.legend()
plt.grid()
plt.show()

# Step 8: Display Backtesting Results
print("Backtesting Results:")
print(trades_df[['Timestamp', 'Strike Price', 'Price', 'Action', 'PnL', 'CumulativePnL']])

trades_df[['Timestamp', 'Strike Price', 'Price', 'Action', 'PnL', 'CumulativePnL']].to_csv(backtesting_results_path, index=False)
print(f"Backtesting results saved to {backtesting_results_path}")

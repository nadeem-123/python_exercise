import pandas as pd
import matplotlib.pyplot as plt


file_path = '/Users/mdnadeem/Documents/Python/nifty_data/Test data/NIFTY_2023-08-10.csv' #filepath of local csv file which needs to analyse
processed_data_path = '/Users/mdnadeem/Documents/Python/nifty_data/Test data/processed_straddle_data.csv' #Output file 1: saved in local storage
trade_results_path = '/Users/mdnadeem/Documents/Python/nifty_data/Test data/trade_results.csv' #Output file 2: saved in local storage
backtesting_results_path = '/Users/mdnadeem/Documents/Python/nifty_data/Test data/backtesting_results.csv' ##Output file 3: saved in local storage

# Load the CSV file
data = pd.read_csv(file_path)
data['timestamp'] = pd.to_datetime(data['timestamp'])
data.set_index('timestamp', inplace=True)

# Step 1: Calculate Synthetic ATM
def calculate_synthetic_atm(data):
    opening_data = data.between_time('09:15', '09:15')
    if opening_data.empty:
        print("No opening data found for '09:15'.")
        return None
    atm = opening_data['strike_price'].median()
    print(f"Synthetic ATM: {atm}")
    return round(atm, -2)

synthetic_atm = calculate_synthetic_atm(data)
if synthetic_atm is None:
    print("Failed to calculate synthetic ATM.")
    exit()

# Step 2: Select Straddles

def select_straddles(data, atm):
    strikes = [atm - 200, atm - 100, atm, atm + 100, atm + 200]
    filtered_data = data[data['strike_price'].isin(strikes)]
    return filtered_data

selected_straddles = select_straddles(data, synthetic_atm)

# Step 3: Simulate Entry and Exit with Conditions

def simulate_entry_exit(data, indicator_threshold, stop_loss_points=30, trailing_sl=True):
    trades = []
    is_in_trade = False
    entry_price = 0
    tsl = 0  # Trailing Stop Loss

    for timestamp, row in data.iterrows():
        if not is_in_trade and row['close'] < indicator_threshold:  # Entry Condition
            trades.append((timestamp, row['strike_price'], row['close'], "ENTRY"))
            is_in_trade = True
            entry_price = row['close']
            tsl = entry_price - stop_loss_points if trailing_sl else None
        elif is_in_trade:
            if row['close'] > entry_price + stop_loss_points:  # Stop Loss Exit
                trades.append((timestamp, row['strike_price'], row['close'], "EXIT"))
                is_in_trade = False
            elif trailing_sl and row['close'] < tsl:  # Trailing SL Exit
                trades.append((timestamp, row['strike_price'], row['close'], "EXIT"))
                is_in_trade = False
            else:  # Update TSL
                tsl = max(tsl, row['close'] - stop_loss_points)
    return trades

indicator_threshold = selected_straddles['close'].mean()  # Dynamic threshold
trades = simulate_entry_exit(selected_straddles, indicator_threshold)

# Step 4: Create Trades DataFrame
trades_df = pd.DataFrame(trades, columns=['Timestamp', 'Strike Price', 'Price', 'Action'])

# Step 5: Calculate PnL
trades_df['PnL'] = 0
for i in range(1, len(trades_df)):
    if trades_df.iloc[i]['Action'] == 'EXIT' and trades_df.iloc[i - 1]['Action'] == 'ENTRY':
        trades_df.loc[i, 'PnL'] = trades_df.iloc[i - 1]['Price'] - trades_df.iloc[i]['Price']

trades_df['CumulativePnL'] = trades_df['PnL'].cumsum()

# Step 6: Save Results
data.to_csv(processed_data_path)
trades_df.to_csv(trade_results_path)

# Step 7: Plot Results
plt.figure(figsize=(12, 6))
for strike in selected_straddles['strike_price'].unique():
    strike_data = selected_straddles[selected_straddles['strike_price'] == strike]
    plt.plot(strike_data.index, strike_data['close'], label=f"Strike {strike}")

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

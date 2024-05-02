import pandas as pd

# Load historical data
# Assuming CSV files with columns for 'Date', 'Strike', 'Type', 'Bid', 'Ask', 'IV', 'UnderlyingPrice'
options_data = pd.read_csv('options_data.csv')
stock_data = pd.read_csv('stock_data.csv')

# Function to calculate returns for credit spreads
def calculate_spread_returns(options_data):
    results = []
    # Filter for specific conditions, e.g., high IV periods
    filtered_data = options_data[options_data['IV'] > options_data['IV'].quantile(0.75)]
    
    for index, row in filtered_data.iterrows():
        if row['Type'] == 'call':
            # Find matching put with the same expiration and strike
            matching_put = options_data[(options_data['Date'] == row['Date']) & 
                                        (options_data['Strike'] == row['Strike']) & 
                                        (options_data['Type'] == 'put')]
            if not matching_put.empty:
                spread_credit = row['Bid'] - matching_put.iloc[0]['Ask']
                spread_debit = row['Ask'] - matching_put.iloc[0]['Bid']
                # Simplified assumption: midpoint of credit and debit for entry/exit
                spread_return = (spread_credit + spread_debit) / 2
                results.append({
                    'Date': row['Date'],
                    'Strike': row['Strike'],
                    'Spread Return': spread_return
                })
    
    return pd.DataFrame(results)

# Analyze spread returns
spread_returns = calculate_spread_returns(options_data)
print(spread_returns.describe())  # Summarize the results

# Save or further analyze the results
spread_returns.to_csv('spread_returns_analysis.csv', index=False)
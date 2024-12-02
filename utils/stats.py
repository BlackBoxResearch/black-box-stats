import pandas as pd
from utils.db import execute_query

def get_account_trades(api_account_id):
    """
    Fetch trades for a specific API account ID.
    
    Args:
        api_account_id (int): The API account ID for which to fetch trades.
        
    Returns:
        list: A list of tuples containing trade details, or an empty list if no trades found.
    """
    query = '''
        SELECT *
        FROM trades
        WHERE api_account_id = :api_account_id
    '''
    
    result = execute_query(query, {'api_account_id': api_account_id})
    
    if result:  # Check if there are any trades
        return result  # Return the raw result (list of tuples)
    else:
        return []  # Return an empty list if no trades are found

def get_user_accounts(user_id):
    """
    Retrieves a list of account numbers for a given user ID where the connection status is 'connected'.
    Args:
        user_id (int): The ID of the user.
    Returns:
        list: A list of account numbers associated with the user.
    """
    # Query to get the account numbers for the user
    query = '''
        SELECT account_number
        FROM accounts
        WHERE user_id = :user_id
        AND connection_status IS 'connected'
    '''

    # Execute the query using the helper function
    result = execute_query(query, {'user_id': user_id})

    # Extract and return the account_number values
    account_numbers = [row[0] for row in result]
    return account_numbers

def get_account_info(user_id, account_number):
    """
    Fetch account information based on user_id and account_number.
    
    Args:
        user_id (int): The ID of the user.
        account_number (str): The account number.
        
    Returns:
        tuple: (api_account_id, account_id) if found, else None.
    """
    query = '''
        SELECT api_account_id, account_id
        FROM accounts
        WHERE user_id = :user_id AND account_number = :account_number
    '''
    
    result = execute_query(query, {'user_id': user_id, 'account_number': account_number})

    if result:  # Check if result contains any rows
        return result[0]  # Return the first row as a tuple
    else:
        return None  # Return None if no data found

def calculate_trade_statistics(trades_df):
    """
    Calculate key statistics from the trade data.
    
    Args:
        trades_df (pd.DataFrame): DataFrame containing trade data.
    
    Returns:
        dict: Dictionary containing formatted key statistics.
    """
    # Ensure datetime columns are parsed correctly
    trades_df['open_time'] = pd.to_datetime(trades_df['open_time'])
    trades_df['close_time'] = pd.to_datetime(trades_df['close_time'])
    
    # Calculate Total Gain
    total_gain = trades_df['gain'].sum()
    
    # Calculate Win Rate
    total_trades = len(trades_df)
    winning_trades = trades_df[trades_df['success'] == 'won'].shape[0]
    win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
    
    # Calculate Profit Factor
    total_profit = trades_df[trades_df['profit'] > 0]['profit'].sum()
    total_loss = abs(trades_df[trades_df['profit'] < 0]['profit'].sum())
    profit_factor = (total_profit / total_loss) if total_loss > 0 else float('inf')
    
    # Calculate Account Age
    account_age_days = (trades_df['close_time'].max() - trades_df['open_time'].min()).days
    
    # Determine Most Traded Symbol
    most_traded_symbol = trades_df['symbol'].mode()[0] if not trades_df['symbol'].mode().empty else None
    
    # Calculate Trade Efficiency Stats
    avg_trade_duration = trades_df['duration_mins'].mean()
    avg_profit_per_trade = trades_df['profit'].mean()
    max_profit = trades_df['profit'].max()
    min_profit = trades_df['profit'].min()
    most_frequent_trade_type = trades_df['type'].mode()[0] if not trades_df['type'].mode().empty else None
    
    # Risk Analysis Stats
    max_drawdown = trades_df['cum_gain'].min()
    avg_risk_per_trade = trades_df[trades_df['profit'] < 0]['profit'].mean()
    sharpe_ratio = total_profit / trades_df['profit'].std() if trades_df['profit'].std() > 0 else float('inf')
    risk_reward_ratio = total_profit / abs(total_loss) if total_loss > 0 else float('inf')
    trades_at_risk = (len(trades_df[trades_df['profit'] < 0]) / total_trades) * 100 if total_trades > 0 else 0
    
    # Behavioural Patterns Stats
    most_frequent_symbol = trades_df['symbol'].mode()[0] if not trades_df['symbol'].mode().empty else None
    most_active_time = trades_df['open_time'].dt.hour.mode()[0] if not trades_df['open_time'].dt.hour.mode().empty else None
    avg_trade_volume = trades_df['volume'].mean()
    largest_volume_trade = trades_df['volume'].max()
    most_frequent_trade_outcome = trades_df['success'].mode()[0] if not trades_df['success'].mode().empty else None
    
    # Market Condition Stats
    best_symbol_profit = trades_df.groupby('symbol')['profit'].sum().idxmax() if not trades_df.empty else None
    worst_symbol_profit = trades_df.groupby('symbol')['profit'].sum().idxmin() if not trades_df.empty else None
    avg_profit_by_symbol = trades_df.groupby('symbol')['profit'].mean().to_dict()
    profit_volatility_by_symbol = trades_df.groupby('symbol')['profit'].std().to_dict()
    
    # Daily Aggregation
    trades_df['day'] = trades_df['close_time'].dt.date
    daily_profit = trades_df.groupby('day')['profit'].sum()
    best_day_profit = daily_profit.idxmax() if not daily_profit.empty else None
    worst_day_profit = daily_profit.idxmin() if not daily_profit.empty else None
    avg_daily_profit = daily_profit.mean()

    
    # Weekly Aggregation
    trades_df['week'] = trades_df['close_time'].dt.to_period('W').apply(lambda r: r.start_time)
    weekly_profit = trades_df.groupby('week')['profit'].sum()
    best_week_profit = weekly_profit.idxmax() if not weekly_profit.empty else None
    worst_week_profit = weekly_profit.idxmin() if not weekly_profit.empty else None

    # Compile results into a dictionary with formatting
    stats = {
        # Overview Stats
        "Total Gain": f"{total_gain:.2f}%",
        "Win Rate": f"{win_rate:.2f}%",
        "Profit Factor": f"{profit_factor:.2f}",
        "Account Age": f"{account_age_days} days",
        "Most Traded Symbol": most_traded_symbol,
        # Trade Efficiency
        "Avg Trade Duration": f"{avg_trade_duration:.2f} mins",
        "Avg Profit Per Trade": f"{avg_profit_per_trade:.2f}",
        "Max Profit": f"{max_profit:.2f}",
        "Min Profit": f"{min_profit:.2f}",
        "Most Frequent Type": most_frequent_trade_type,
        # Risk Analysis
        "Max Drawdown": f"{max_drawdown:.2f}",
        "Avg Risk Per Trade": f"{avg_risk_per_trade:.2f}",
        "Sharpe Ratio": f"{sharpe_ratio:.2f}",
        "Risk Reward Ratio": f"{risk_reward_ratio:.2f}",
        "Trades at Risk": f"{trades_at_risk:.2f}%",
        # Behavioural Patterns
        "Most Frequent Symbol": most_frequent_symbol,
        "Most Active Time": f"{most_active_time}:00",
        "Avg Trade Volume": f"{avg_trade_volume:.2f}",
        "Largest Volume Trade": f"{largest_volume_trade:.2f}",
        "Most Frequent Outcome": most_frequent_trade_outcome,
        # Market Condition
        "Best Day Profit": f"{daily_profit[best_day_profit]:.2f}" if best_day_profit else "N/A",
        "Worst Day Profit": f"{daily_profit[worst_day_profit]:.2f}" if worst_day_profit else "N/A",
        "Average Daily Profit": f"{avg_daily_profit:.2f}" if not daily_profit.empty else "N/A",
        "Best Week Profit": f"{weekly_profit[best_week_profit]:.2f}" if best_week_profit else "N/A",
        "Worst Week Profit": f"{weekly_profit[worst_week_profit]:.2f}" if worst_week_profit else "N/A",
        "Best Symbol Profit": best_symbol_profit,
        "Worst Symbol Profit": worst_symbol_profit,
        "Avg Profit By Symbol": avg_profit_by_symbol,
        "Profit Volatility By Symbol": profit_volatility_by_symbol
        }
    
    return stats

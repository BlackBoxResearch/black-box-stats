import asyncio
import psycopg2
from metaapi_cloud_sdk import MetaApi
from datetime import datetime, timedelta, timezone
from db import execute_query

# Database connection parameters
DB_HOST = "analytiq-test-database.c102eee68lij.eu-west-2.rds.amazonaws.com"
DB_PORT = 5432
DB_NAME = "postgres"
DB_USER = "blackboxresearch"
DB_PASSWORD = "!Audacious2011"

# MetaApi credentials
TOKEN = 'eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiIyYTY2MGNmN2Q0ZWRlZDUzNzgwYTI2ZDcxODk2MjQ3NCIsInBlcm1pc3Npb25zIjpbXSwiYWNjZXNzUnVsZXMiOlt7ImlkIjoidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpIiwibWV0aG9kcyI6WyJ0cmFkaW5nLWFjY291bnQtbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZXN0LWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1ycGMtYXBpIiwibWV0aG9kcyI6WyJtZXRhYXBpLWFwaTp3czpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZWFsLXRpbWUtc3RyZWFtaW5nLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFzdGF0cy1hcGkiLCJtZXRob2RzIjpbIm1ldGFzdGF0cy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoicmlzay1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsicmlzay1tYW5hZ2VtZW50LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJjb3B5ZmFjdG9yeS1hcGkiLCJtZXRob2RzIjpbImNvcHlmYWN0b3J5LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtdC1tYW5hZ2VyLWFwaSIsIm1ldGhvZHMiOlsibXQtbWFuYWdlci1hcGk6cmVzdDpkZWFsaW5nOio6KiIsIm10LW1hbmFnZXItYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6ImJpbGxpbmctYXBpIiwibWV0aG9kcyI6WyJiaWxsaW5nLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19XSwiaWdub3JlUmF0ZUxpbWl0cyI6ZmFsc2UsInRva2VuSWQiOiIyMDIxMDIxMyIsImltcGVyc29uYXRlZCI6ZmFsc2UsInJlYWxVc2VySWQiOiIyYTY2MGNmN2Q0ZWRlZDUzNzgwYTI2ZDcxODk2MjQ3NCIsImlhdCI6MTczNDU2NTk2MH0.ZVIKOvJ3Q9LLbrEf0QE1PdnYv6osSaB4mcUmg2Ma4q1hjEeKzeD37oWZ1ZxhtMZXbLHZDySiYoPt5A0sWmFxM_9i9rMnPE-BPpySFI-vnobOp-u9iWdZmyii7_EH3NTBuyDw_srL72H3s7nDOykQ4dwp7AnwFmfdWjdrmxu2wdu6fMZXgZLGgvPmX4Z6tPXi-3dTRV7wjjh87uOi3Ls9_TVlz5FaLVC438wAwLrRZyO8j5RYz4ufKBk5Jl008doFMoxaoe5fBndR9AcDBAlGZz51k7Ln0D8w1W5O0V9QrdUYm54xB9ZobTnWRsSlyWn0ywvn-hPHya-76T8gmp-okNBlG3pcbDSbB9bWLWnOCoYtaq1s-jvo1rZwtDpaCGikTOb1B1EClnVv-cxHv-yZfVqjAIJB4t86Ru3U5EOMqwhUaXrUOEPwevBe7yAOZazBqHvMj8ridEmAo0ZCkFQtWJol0tYD-HQfbiytmGot-8C8Dw7fnkDB-zo2CFt1yKyCQxeYs8hMIGYZ-lHOFUK1HINB9A8e9Uj5WMTX7URaRigiQsffr77uUFHFRbcTLSdXgKfwBHHp8Poet-2mryGNBjZuWN4Z7iq6nNyQV45r7JaRHBJxpzEVL0EEi4mrX6seSlZx5IbHJ8t7myGKzgpLWf6F_50aANQ33Y4qEjn3_I4'
USER_ID = 1  # Example user ID

def register_user(first_name, last_name, email, country, password_hash, password_hint, marketing):
    """
    Registers a new user in the database.

    Args:
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        email (str): The user's email address.
        country (str): The user's country of residence.
        password_hash (str): The hashed password for the user.
        password_hint (str): A password hint for the user.
        marketing (bool): Whether the user opts into marketing communications.

    Returns:
        dict: A success message if the user is registered successfully, or an error message if something goes wrong.
    """
    query = '''
        INSERT INTO users (
            first_name, 
            last_name, 
            email, 
            country, 
            password_hash, 
            password_hint, 
            marketing
        ) 
        VALUES (
            %s, %s, %s, %s, %s, %s, %s
        );
    '''
    params = (
        first_name,
        last_name,
        email,
        country,
        password_hash,
        password_hint,
        marketing
    )

    try:
        # Execute the query without fetching results
        execute_query(query, params, fetch_results=False)
        print(f"User {email} registered successfully.")
        return {"status": "success", "message": f"User {email} registered successfully."}
    except Exception as e:
        print(f"Error registering user {email}: {e}")
        return {"status": "error", "message": f"An error occurred while registering the user: {str(e)}"}

def process_deals(deals, account_id):
    """
    Processes a list of deals into positions and balance operations.

    Args:
        deals (list): List of deal objects.
        account_id (str): The ID of the account associated with the deals.

    Returns:
        tuple: A tuple containing two lists:
            - positions: Processed positions grouped by positionId.
            - balance_operations: Processed balance operations.
    """
    positions = {}
    balance_operations = []

    for deal in deals:
        deal_type = deal.get('type')
        if deal_type == 'DEAL_TYPE_BALANCE':
            # Process balance operation
            balance_operations.append({
                'account_id': account_id,
                'time': deal.get('time'),
                'type': 'deposit' if deal.get('profit', 0) > 0 else 'withdrawal',
                'amount': deal.get('profit', 0),  # Positive or negative profit
                'comment': deal.get('comment', '')  # Optional, if available
            })
            continue

        # Process positions
        position_id = deal.get('positionId')
        if not position_id:
            continue

        if position_id not in positions:
            positions[position_id] = {
                'position_id': position_id,
                'account_id': account_id,
                'symbol': deal.get('symbol'),
                'volume': deal.get('volume', 0.0),
                'type': 'BUY' if deal.get('type') == 'DEAL_TYPE_BUY' else 'SELL',
                'open_time': None,
                'open_price': None,
                'stop_loss': None,
                'take_profit': None,
                'close_time': None,
                'close_price': None,
                'commission': 0.0,
                'swap': 0.0,
                'profit': 0.0
            }

        # Update trade details based on deal type
        if deal.get('entryType') == 'DEAL_ENTRY_IN':
            positions[position_id]['open_time'] = deal.get('time')
            positions[position_id]['open_price'] = deal.get('price')
        elif deal.get('entryType') == 'DEAL_ENTRY_OUT':
            positions[position_id]['stop_loss'] = deal.get('stopLoss')
            positions[position_id]['take_profit'] = deal.get('takeProfit')
            positions[position_id]['close_time'] = deal.get('time')
            positions[position_id]['close_price'] = deal.get('price')

        # Accumulate financial data
        positions[position_id]['commission'] += deal.get('commission', 0.0)
        positions[position_id]['swap'] += deal.get('swap', 0.0)
        positions[position_id]['profit'] += deal.get('profit', 0.0)

    return list(positions.values()), balance_operations

def save_account(user_id, account_id, account_info, account_name):
    query = '''
        INSERT INTO accounts (
            user_id,
            account_id,
            platform,
            type,
            broker,
            currency,
            server,
            leverage,
            margin_mode,
            name,
            login
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    params = (
        user_id,
        account_id,
        account_info['platform'],
        account_info['type'],
        account_info['broker'],
        account_info['currency'],
        account_info['server'],
        account_info['leverage'],
        account_info['marginMode'],
        account_name,
        account_info['login']
    )
    execute_query(query, params, fetch_results=False)
    print("Account information saved to database.")

def save_positions(account_id, positions):
    query = '''
        INSERT INTO trades (
            account_id,
            position_id,
            symbol,
            volume,
            type,
            open_time,
            open_price,
            stop_loss,
            take_profit,
            close_time,
            close_price,
            commission,
            swap,
            profit
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    for position in positions:
        params = (
            account_id,
            position['position_id'],
            position['symbol'],
            position['volume'],
            position['type'],
            position['open_time'],
            position['open_price'],
            position['stop_loss'],
            position['take_profit'],
            position['close_time'],
            position['close_price'],
            position['commission'],
            position['swap'],
            position['profit'],
        )
        execute_query(query, params, fetch_results=False)

def save_balance_operations(account_id, balance_operations):
    query = '''
        INSERT INTO balance_operations (
            account_id,
            time,
            type,
            amount,
            comment
        ) 
        VALUES (%s, %s, %s, %s, %s)
    '''
    for operation in balance_operations:
        params = (
            account_id,
            operation['time'],
            operation['type'],
            operation['amount'],
            operation['comment']
        )
        execute_query(query, params, fetch_results=False)

async def deploy_account(user_id, name, login, password, server_name, platform):
    api = MetaApi(TOKEN)

    accounts = await api.metatrader_account_api.get_accounts_with_infinite_scroll_pagination()
    account = next((item for item in accounts if item.login == login and item.type.startswith('cloud')), None)

    if account:
        print(f"Account already exists on MetaApi with ID: {account.id}")
        return account

    print("Creating a new account...")

    account = await api.metatrader_account_api.create_account({
        'name': name,
        'type': 'cloud',
        'login': login,
        'password': password,
        'server': server_name,
        'platform': platform,
        'application': 'MetaApi',
        'magic': 1000,
    })

    print(f"Account created with ID: {account.id}.")

    print('Deploying account...')
    await account.deploy()

    print('Waiting for API server to connect to broker (may take a couple of minutes)...')
    await account.wait_connected()

    # Connect to MetaApi API
    connection = account.get_rpc_connection()
    await connection.connect()

    # Wait until the terminal state is synchronized
    print('Waiting for SDK to synchronize to terminal state (may take some time depending on your history size)...')
    await connection.wait_synchronized(600)

    # Access account information using appropriate SDK methods
    print('Testing terminal state access...')
    account_info = await connection.get_account_information()
    print('Account information:', account_info)

    save_account(user_id, account.id, account_info, name)
    print("Account added to database")

    # Ensure start_time and end_time are datetime objects
    start_time = datetime(2020, 1, 1, tzinfo=timezone.utc)
    end_time = datetime.now(timezone.utc)

    deals_response = await connection.get_deals_by_time_range(start_time, end_time)

    deals = deals_response.get('deals', [])

    positions, balance_operations = process_deals(deals, account.id)

    save_positions(account.id, positions)
    save_balance_operations(account.id, balance_operations)

async def main():
    # Define account details
    name = "FTMO 10k account"
    login = "520183149"
    password = "J!6xlX@7?21pE"
    server_name = "FTMO-Server2"
    platform = "mt5"
    
    await deploy_account(USER_ID, name, login, password, server_name, platform)

# Run the test
if __name__ == "__main__":
    asyncio.run(main())
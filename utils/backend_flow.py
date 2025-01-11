import asyncio
import psycopg2
from metaapi_cloud_sdk import MetaApi
from datetime import datetime, timedelta
from db import execute_query

# Database connection parameters
DB_HOST = "analytiq-test-database.c102eee68lij.eu-west-2.rds.amazonaws.com"
DB_PORT = 5432
DB_NAME = "postgres"
DB_USER = "blackboxresearch"
DB_PASSWORD = "!Audacious2011"

# MetaApi credentials
TOKEN = 'eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiIyYTY2MGNmN2Q0ZWRlZDUzNzgwYTI2ZDcxODk2MjQ3NCIsInBlcm1pc3Npb25zIjpbXSwiYWNjZXNzUnVsZXMiOlt7ImlkIjoidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpIiwibWV0aG9kcyI6WyJ0cmFkaW5nLWFjY291bnQtbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZXN0LWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1ycGMtYXBpIiwibWV0aG9kcyI6WyJtZXRhYXBpLWFwaTp3czpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZWFsLXRpbWUtc3RyZWFtaW5nLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFzdGF0cy1hcGkiLCJtZXRob2RzIjpbIm1ldGFzdGF0cy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoicmlzay1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsicmlzay1tYW5hZ2VtZW50LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJjb3B5ZmFjdG9yeS1hcGkiLCJtZXRob2RzIjpbImNvcHlmYWN0b3J5LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtdC1tYW5hZ2VyLWFwaSIsIm1ldGhvZHMiOlsibXQtbWFuYWdlci1hcGk6cmVzdDpkZWFsaW5nOio6KiIsIm10LW1hbmFnZXItYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6ImJpbGxpbmctYXBpIiwibWV0aG9kcyI6WyJiaWxsaW5nLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19XSwiaWdub3JlUmF0ZUxpbWl0cyI6ZmFsc2UsInRva2VuSWQiOiIyMDIxMDIxMyIsImltcGVyc29uYXRlZCI6ZmFsc2UsInJlYWxVc2VySWQiOiIyYTY2MGNmN2Q0ZWRlZDUzNzgwYTI2ZDcxODk2MjQ3NCIsImlhdCI6MTczNDU2NTk2MH0.ZVIKOvJ3Q9LLbrEf0QE1PdnYv6osSaB4mcUmg2Ma4q1hjEeKzeD37oWZ1ZxhtMZXbLHZDySiYoPt5A0sWmFxM_9i9rMnPE-BPpySFI-vnobOp-u9iWdZmyii7_EH3NTBuyDw_srL72H3s7nDOykQ4dwp7AnwFmfdWjdrmxu2wdu6fMZXgZLGgvPmX4Z6tPXi-3dTRV7wjjh87uOi3Ls9_TVlz5FaLVC438wAwLrRZyO8j5RYz4ufKBk5Jl008doFMoxaoe5fBndR9AcDBAlGZz51k7Ln0D8w1W5O0V9QrdUYm54xB9ZobTnWRsSlyWn0ywvn-hPHya-76T8gmp-okNBlG3pcbDSbB9bWLWnOCoYtaq1s-jvo1rZwtDpaCGikTOb1B1EClnVv-cxHv-yZfVqjAIJB4t86Ru3U5EOMqwhUaXrUOEPwevBe7yAOZazBqHvMj8ridEmAo0ZCkFQtWJol0tYD-HQfbiytmGot-8C8Dw7fnkDB-zo2CFt1yKyCQxeYs8hMIGYZ-lHOFUK1HINB9A8e9Uj5WMTX7URaRigiQsffr77uUFHFRbcTLSdXgKfwBHHp8Poet-2mryGNBjZuWN4Z7iq6nNyQV45r7JaRHBJxpzEVL0EEi4mrX6seSlZx5IbHJ8t7myGKzgpLWf6F_50aANQ33Y4qEjn3_I4'
TEST_ACCOUNT_1 = 'ab9bbaba-bc20-440d-9b3a-fa2e9a72267f'

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

async def create_and_deploy_account(api, login, password, server_name, platform):
    """
    Initializes the account on MetaApi: checks if it exists, creates and deploys it if not.
    """
    accounts = await api.metatrader_account_api.get_accounts_with_infinite_scroll_pagination()
    account = next((item for item in accounts if item.login == login and item.type.startswith('cloud')), None)

    if account:
        print(f"Account already exists on MetaApi with ID: {account.id}")
        return account

    print("Creating a new account...")
    account = await api.metatrader_account_api.create_account({
        'name': f'{platform} Account {login}',
        'type': 'cloud',
        'login': login,
        'password': password,
        'server': server_name,
        'platform': platform,
        'application': 'MetaApi',
        'magic': 1000,
    })
    print(f"Account created with ID: {account.id}. Deploying...")
    await account.deploy()
    return account

async def fetch_historical_data(connection, account_id, start_time, end_time):
    """
    Fetches historical deals and processes them into positions and balance operations.
    """
    deals_response = await connection.get_deals_by_time_range(start_time, end_time)
    deals = deals_response.get('deals', [])
    positions, balance_operations = process_deals(deals, account_id)
    return positions, balance_operations

def save_account_to_db(user_id, account_info, account_id, platform, server_name, login):
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
        platform,
        account_info['type'],
        account_info['broker'],
        account_info['currency'],
        server_name,
        account_info['leverage'],
        account_info['marginMode'],
        f'{platform} Account {login}',
        login
    )
    execute_query(query, params, fetch_results=False)
    print("Account information saved to database.")

def save_positions_to_db(account_id, positions):
    query = '''
        INSERT INTO positions (
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

def save_balance_operations_to_db(account_id, balance_operations):
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
            operation['account_id'],
            operation['time'],
            operation['type'],
            operation['amount'],
            operation['comment']
        )
        execute_query(query, params, fetch_results=False)

async def connect_and_fetch_account(user_id, login, password, server_name, platform):
    api = MetaApi(TOKEN)

    try:
        # Step 1: Initialize Account
        account = await create_and_deploy_account(api, login, password, server_name, platform)
        api_account_id = account.id

        # Step 2: Retrieve Account Info
        print('Waiting for API server to connect to broker (may take couple of minutes)')
        await account.wait_connected()
        connection = account.get_rpc_connection()
        await connection.connect()
        # wait until terminal state synchronized to the local state
        print('Waiting for SDK to synchronize to terminal state (may take some time depending on your history size)')
        await connection.wait_synchronized()

        account_info = await connection.get_account_information()

        # Step 3: Fetch Historical Data
        start_time = "2020-01-01T00:00:00.000Z"
        end_time = "2025-01-01T00:00:00.000Z"
        positions, balance_operations = await fetch_historical_data(connection, api_account_id, start_time, end_time)

        # Step 4: Save to Database
        save_account_to_db(user_id, account_info, api_account_id, platform, server_name, login)
        save_positions_to_db(api_account_id, positions)
        save_balance_operations_to_db(api_account_id, balance_operations)

        print("Account connected, deployed, and historical data saved successfully.")
        return {"status": "success", "api_account_id": api_account_id}

    except Exception as e:
        print(f"Error in connecting and deploying account: {e}")
        return {"status": "error", "message": str(e)}

response = register_user(
    first_name="Ben",
    last_name="Hardman",
    email="drummerben@me.com",
    country="United Kingdom",
    password_hash="0a6baa6ef716d698b27fe42ca535d5709cb024885a6592b2671213780be8b405",
    password_hint="usual",
    marketing=True
)

print(response)

USER_ID = 1  # Example user ID

async def main():
    # Define account details
    login = "520183149"
    password = "J!6xlX@7?21pE"
    server_name = "FTMO-Server2"
    platform = "mt5"

    # Run the connection and deployment process
    response = await connect_and_fetch_account(
        USER_ID,  # Pass the user ID
        login,
        password,
        server_name,
        platform
    )
    print(response)

# Run the test
if __name__ == "__main__":
    asyncio.run(main())
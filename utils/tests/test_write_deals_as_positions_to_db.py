import asyncio
import psycopg2
from metaapi_cloud_sdk import MetaApi
from datetime import datetime, timedelta

# Database connection parameters
DB_HOST = "analytiq-test-database.c102eee68lij.eu-west-2.rds.amazonaws.com"
DB_PORT = 5432
DB_NAME = "postgres"
DB_USER = "blackboxresearch"
DB_PASSWORD = "!Audacious2011"

# MetaApi credentials
TOKEN = 'eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiIyYTY2MGNmN2Q0ZWRlZDUzNzgwYTI2ZDcxODk2MjQ3NCIsInBlcm1pc3Npb25zIjpbXSwiYWNjZXNzUnVsZXMiOlt7ImlkIjoidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpIiwibWV0aG9kcyI6WyJ0cmFkaW5nLWFjY291bnQtbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZXN0LWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1ycGMtYXBpIiwibWV0aG9kcyI6WyJtZXRhYXBpLWFwaTp3czpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZWFsLXRpbWUtc3RyZWFtaW5nLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFzdGF0cy1hcGkiLCJtZXRob2RzIjpbIm1ldGFzdGF0cy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoicmlzay1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsicmlzay1tYW5hZ2VtZW50LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJjb3B5ZmFjdG9yeS1hcGkiLCJtZXRob2RzIjpbImNvcHlmYWN0b3J5LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtdC1tYW5hZ2VyLWFwaSIsIm1ldGhvZHMiOlsibXQtbWFuYWdlci1hcGk6cmVzdDpkZWFsaW5nOio6KiIsIm10LW1hbmFnZXItYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6ImJpbGxpbmctYXBpIiwibWV0aG9kcyI6WyJiaWxsaW5nLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19XSwiaWdub3JlUmF0ZUxpbWl0cyI6ZmFsc2UsInRva2VuSWQiOiIyMDIxMDIxMyIsImltcGVyc29uYXRlZCI6ZmFsc2UsInJlYWxVc2VySWQiOiIyYTY2MGNmN2Q0ZWRlZDUzNzgwYTI2ZDcxODk2MjQ3NCIsImlhdCI6MTczNDU2NTk2MH0.ZVIKOvJ3Q9LLbrEf0QE1PdnYv6osSaB4mcUmg2Ma4q1hjEeKzeD37oWZ1ZxhtMZXbLHZDySiYoPt5A0sWmFxM_9i9rMnPE-BPpySFI-vnobOp-u9iWdZmyii7_EH3NTBuyDw_srL72H3s7nDOykQ4dwp7AnwFmfdWjdrmxu2wdu6fMZXgZLGgvPmX4Z6tPXi-3dTRV7wjjh87uOi3Ls9_TVlz5FaLVC438wAwLrRZyO8j5RYz4ufKBk5Jl008doFMoxaoe5fBndR9AcDBAlGZz51k7Ln0D8w1W5O0V9QrdUYm54xB9ZobTnWRsSlyWn0ywvn-hPHya-76T8gmp-okNBlG3pcbDSbB9bWLWnOCoYtaq1s-jvo1rZwtDpaCGikTOb1B1EClnVv-cxHv-yZfVqjAIJB4t86Ru3U5EOMqwhUaXrUOEPwevBe7yAOZazBqHvMj8ridEmAo0ZCkFQtWJol0tYD-HQfbiytmGot-8C8Dw7fnkDB-zo2CFt1yKyCQxeYs8hMIGYZ-lHOFUK1HINB9A8e9Uj5WMTX7URaRigiQsffr77uUFHFRbcTLSdXgKfwBHHp8Poet-2mryGNBjZuWN4Z7iq6nNyQV45r7JaRHBJxpzEVL0EEi4mrX6seSlZx5IbHJ8t7myGKzgpLWf6F_50aANQ33Y4qEjn3_I4'
TEST_ACCOUNT = 'ab9bbaba-bc20-440d-9b3a-fa2e9a72267f'

def process_deals(deals):
    """
    Processes a list of deals and groups them by positionId to create a structured
    dictionary for each position with the required fields.
    """
    positions = {}

    for deal in deals:
        position_id = deal.get('positionId')
        if not position_id:
            continue

        if position_id not in positions:
            positions[position_id] = {
                'position_id': position_id,
                'account_id': TEST_ACCOUNT,  # Add account_id here
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

    return list(positions.values())


async def meta_api_synchronization():
    api = MetaApi(TOKEN)

    try:
        # Retrieve MetaApi account
        account = await api.metatrader_account_api.get_account(TEST_ACCOUNT)
        await account.wait_connected()

        connection = account.get_rpc_connection()
        await connection.connect()
        await connection.wait_synchronized()

        # Fetch deals within the last 90 days
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=90)
        deals_response = await connection.get_deals_by_time_range(start_time, end_time)
        deals = deals_response.get('deals', [])

        if deals:
            positions = process_deals(deals)
            write_to_database(positions)

        await connection.close()

    except Exception as err:
        print(f"An error occurred: {err}")

def write_to_database(positions):
    """
    Writes the processed positions into the trades table in the PostgreSQL database.
    """
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # Insert positions into the trades table
        for position in positions:
            cursor.execute("""
                INSERT INTO trades (
                    account_id, position_id, symbol, volume, type, open_time, open_price, 
                    stop_loss, take_profit, close_time, close_price, 
                    commission, swap, profit
                ) VALUES (
                    %(account_id)s, %(position_id)s, %(symbol)s, %(volume)s, %(type)s, %(open_time)s, %(open_price)s, 
                    %(stop_loss)s, %(take_profit)s, %(close_time)s, %(close_price)s, 
                    %(commission)s, %(swap)s, %(profit)s
                )
                ON CONFLICT (position_id) DO NOTHING;
            """, position)

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()
        print("Positions successfully written to the trades table!")

    except Exception as e:
        print(f"An error occurred while writing to the database: {e}")

# Run the asynchronous main function
if __name__ == "__main__":
    asyncio.run(meta_api_synchronization())

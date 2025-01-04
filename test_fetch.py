import asyncio
import time
from metaapi_cloud_sdk import MetaApi

async def continuous_streaming(api_token, account_ids, fetch_interval=2):
    """
    Continuously connects to MetaTrader accounts (which are already deployed),
    and then fetches & prints account data in a regular interval.
    
    :param api_token: Your MetaApi token
    :param account_ids: List of MetaTrader account IDs to stream
    :param fetch_interval: Interval in seconds between fetch cycles
    """
    api = MetaApi(api_token)
    connections = []
    
    try:
        # ---------------------------------------------------------------------
        # 1. Fetch and connect to all accounts (NO deploy calls)
        # ---------------------------------------------------------------------
        # Assume your accounts are already deployed in MetaAPI.
        # We'll just retrieve their objects and wait for them to connect.
        accounts = [
            await api.metatrader_account_api.get_account(account_id) 
            for account_id in account_ids
        ]
        
        # Wait for each account to be in "connected" state 
        await asyncio.gather(*(account.wait_connected() for account in accounts))
        
        # Create & synchronize RPC connections for continuous streaming
        for account in accounts:
            connection = account.get_rpc_connection()
            await connection.connect()
            await connection.wait_synchronized()
            connections.append(connection)
        
        print(f"All {len(connections)} accounts are connected and synchronized.")
        
        # ---------------------------------------------------------------------
        # 2. Continuously fetch and print account data
        # ---------------------------------------------------------------------
        while True:
            start_time = time.time()
            
            # Prepare tasks in parallel
            tasks = [fetch_account_data(conn) for conn in connections]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            end_time = time.time()
            elapsed = end_time - start_time
            
            # Print the timing measurement for the fetch cycle
            print(f"----- Fetch cycle completed in {elapsed:.2f} seconds -----")
            
            # Print each account's data
            for data in results:
                if isinstance(data, dict):
                    print(
                        f"Account {data.get('id')} | "
                        f"Name: {data.get('name')} | "
                        f"Balance: {data.get('balance')} | "
                        f"Equity: {data.get('equity')} | "
                        f"Server Time: {data.get('server_time')}"
                    )
                else:
                    # If there's an exception, print it
                    print(f"Error fetching data: {data}")
            
            print("-----------------------------------------------------\n")
            
            # Wait until next fetch cycle
            await asyncio.sleep(fetch_interval)

    except Exception as e:
        print(f"Error in continuous_streaming: {e}")

    finally:
        # Optional: close the RPC connections if needed
        # (This does NOT undeploy the accounts; it only closes client connections.)
        await asyncio.gather(*[conn.close() for conn in connections], return_exceptions=True)
        print("Connections closed. (Accounts remain deployed.)")


async def fetch_account_data(connection):
    """
    Helper coroutine to fetch & return account information from a given connection.
    """
    account_info = await connection.get_account_information()
    server_time = await connection.get_server_time()
    return {
        "id": account_info.get("login"),
        "name": account_info.get("name"),
        "balance": account_info.get("balance"),
        "equity": account_info.get("equity"),
        "server_time": server_time
    }

def replicate_account_ids(base_id, n):
    """
    Returns a list containing `base_id` repeated `n` times.
    
    :param base_id: The single account ID to duplicate
    :param n: The number of times to replicate the ID
    :return: A list of length `n`, with each element set to `base_id`
    """
    return [base_id] * n

# Example usage with asyncio
if __name__ == "__main__":
    async def main():
        api_token = 'eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiIyYTY2MGNmN2Q0ZWRlZDUzNzgwYTI2ZDcxODk2MjQ3NCIsInBlcm1pc3Npb25zIjpbXSwiYWNjZXNzUnVsZXMiOlt7ImlkIjoidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpIiwibWV0aG9kcyI6WyJ0cmFkaW5nLWFjY291bnQtbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZXN0LWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1ycGMtYXBpIiwibWV0aG9kcyI6WyJtZXRhYXBpLWFwaTp3czpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZWFsLXRpbWUtc3RyZWFtaW5nLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFzdGF0cy1hcGkiLCJtZXRob2RzIjpbIm1ldGFzdGF0cy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoicmlzay1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsicmlzay1tYW5hZ2VtZW50LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJjb3B5ZmFjdG9yeS1hcGkiLCJtZXRob2RzIjpbImNvcHlmYWN0b3J5LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtdC1tYW5hZ2VyLWFwaSIsIm1ldGhvZHMiOlsibXQtbWFuYWdlci1hcGk6cmVzdDpkZWFsaW5nOio6KiIsIm10LW1hbmFnZXItYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6ImJpbGxpbmctYXBpIiwibWV0aG9kcyI6WyJiaWxsaW5nLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19XSwiaWdub3JlUmF0ZUxpbWl0cyI6ZmFsc2UsInRva2VuSWQiOiIyMDIxMDIxMyIsImltcGVyc29uYXRlZCI6ZmFsc2UsInJlYWxVc2VySWQiOiIyYTY2MGNmN2Q0ZWRlZDUzNzgwYTI2ZDcxODk2MjQ3NCIsImlhdCI6MTczNDU2NTk2MH0.ZVIKOvJ3Q9LLbrEf0QE1PdnYv6osSaB4mcUmg2Ma4q1hjEeKzeD37oWZ1ZxhtMZXbLHZDySiYoPt5A0sWmFxM_9i9rMnPE-BPpySFI-vnobOp-u9iWdZmyii7_EH3NTBuyDw_srL72H3s7nDOykQ4dwp7AnwFmfdWjdrmxu2wdu6fMZXgZLGgvPmX4Z6tPXi-3dTRV7wjjh87uOi3Ls9_TVlz5FaLVC438wAwLrRZyO8j5RYz4ufKBk5Jl008doFMoxaoe5fBndR9AcDBAlGZz51k7Ln0D8w1W5O0V9QrdUYm54xB9ZobTnWRsSlyWn0ywvn-hPHya-76T8gmp-okNBlG3pcbDSbB9bWLWnOCoYtaq1s-jvo1rZwtDpaCGikTOb1B1EClnVv-cxHv-yZfVqjAIJB4t86Ru3U5EOMqwhUaXrUOEPwevBe7yAOZazBqHvMj8ridEmAo0ZCkFQtWJol0tYD-HQfbiytmGot-8C8Dw7fnkDB-zo2CFt1yKyCQxeYs8hMIGYZ-lHOFUK1HINB9A8e9Uj5WMTX7URaRigiQsffr77uUFHFRbcTLSdXgKfwBHHp8Poet-2mryGNBjZuWN4Z7iq6nNyQV45r7JaRHBJxpzEVL0EEi4mrX6seSlZx5IbHJ8t7myGKzgpLWf6F_50aANQ33Y4qEjn3_I4'

        # Choose how many duplicates you want for testing
        num_accounts = 100  # or 1_000, for example

        # Replicate the single base ID
        base_id = 'ab9bbaba-bc20-440d-9b3a-fa2e9a72267f'
        account_ids = replicate_account_ids(base_id, num_accounts)
        
        # Run the streaming with your duplicated list
        await continuous_streaming(api_token, account_ids, fetch_interval=10)

    asyncio.run(main())

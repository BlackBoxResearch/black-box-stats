from metaapi_cloud_sdk import MetaApi
import asyncio
import time

api_token = 'eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiIyYTY2MGNmN2Q0ZWRlZDUzNzgwYTI2ZDcxODk2MjQ3NCIsInBlcm1pc3Npb25zIjpbXSwiYWNjZXNzUnVsZXMiOlt7ImlkIjoidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpIiwibWV0aG9kcyI6WyJ0cmFkaW5nLWFjY291bnQtbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZXN0LWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1ycGMtYXBpIiwibWV0aG9kcyI6WyJtZXRhYXBpLWFwaTp3czpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZWFsLXRpbWUtc3RyZWFtaW5nLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFzdGF0cy1hcGkiLCJtZXRob2RzIjpbIm1ldGFzdGF0cy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoicmlzay1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsicmlzay1tYW5hZ2VtZW50LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJjb3B5ZmFjdG9yeS1hcGkiLCJtZXRob2RzIjpbImNvcHlmYWN0b3J5LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtdC1tYW5hZ2VyLWFwaSIsIm1ldGhvZHMiOlsibXQtbWFuYWdlci1hcGk6cmVzdDpkZWFsaW5nOio6KiIsIm10LW1hbmFnZXItYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6ImJpbGxpbmctYXBpIiwibWV0aG9kcyI6WyJiaWxsaW5nLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19XSwiaWdub3JlUmF0ZUxpbWl0cyI6ZmFsc2UsInRva2VuSWQiOiIyMDIxMDIxMyIsImltcGVyc29uYXRlZCI6ZmFsc2UsInJlYWxVc2VySWQiOiIyYTY2MGNmN2Q0ZWRlZDUzNzgwYTI2ZDcxODk2MjQ3NCIsImlhdCI6MTczNDU2NTk2MH0.ZVIKOvJ3Q9LLbrEf0QE1PdnYv6osSaB4mcUmg2Ma4q1hjEeKzeD37oWZ1ZxhtMZXbLHZDySiYoPt5A0sWmFxM_9i9rMnPE-BPpySFI-vnobOp-u9iWdZmyii7_EH3NTBuyDw_srL72H3s7nDOykQ4dwp7AnwFmfdWjdrmxu2wdu6fMZXgZLGgvPmX4Z6tPXi-3dTRV7wjjh87uOi3Ls9_TVlz5FaLVC438wAwLrRZyO8j5RYz4ufKBk5Jl008doFMoxaoe5fBndR9AcDBAlGZz51k7Ln0D8w1W5O0V9QrdUYm54xB9ZobTnWRsSlyWn0ywvn-hPHya-76T8gmp-okNBlG3pcbDSbB9bWLWnOCoYtaq1s-jvo1rZwtDpaCGikTOb1B1EClnVv-cxHv-yZfVqjAIJB4t86Ru3U5EOMqwhUaXrUOEPwevBe7yAOZazBqHvMj8ridEmAo0ZCkFQtWJol0tYD-HQfbiytmGot-8C8Dw7fnkDB-zo2CFt1yKyCQxeYs8hMIGYZ-lHOFUK1HINB9A8e9Uj5WMTX7URaRigiQsffr77uUFHFRbcTLSdXgKfwBHHp8Poet-2mryGNBjZuWN4Z7iq6nNyQV45r7JaRHBJxpzEVL0EEi4mrX6seSlZx5IbHJ8t7myGKzgpLWf6F_50aANQ33Y4qEjn3_I4'

async def batch_deploy_and_fetch(api_token, account_ids):
    """
    Deploys a batch of MetaTrader accounts, fetches account data using RPC connections,
    and undeploys the accounts to minimize resource usage.
    """
    api = MetaApi(api_token)
    account_data = []
    start_time = time.time()  # Start timing the process

    try:
        # Fetch and deploy all accounts
        accounts = [await api.metatrader_account_api.get_account(account_id) for account_id in account_ids]
        print("Deploying accounts...")
        await asyncio.gather(*(account.deploy() for account in accounts))
        await asyncio.gather(*(account.wait_connected() for account in accounts))
        print("All accounts deployed and connected.")

        # Fetch data for all accounts
        for account in accounts:
            connection = account.get_rpc_connection()
            await connection.connect()
            await connection.wait_synchronized()
            
            # Fetch required information
            data = await connection.get_account_information()
            account_data.append({
                "id": account.id,
                "name": data.get("name"),
                "balance": data.get("balance"),
                "equity": data.get("equity"),
                "server_time": await connection.get_server_time()
            })

            # Close the connection
            await connection.close()
        
        print("Account data fetched:", account_data)

    except Exception as e:
        print(f"Error during batch operation: {e}")

    finally:
        # Undeploy all accounts to minimize resource usage
        print("Undeploying accounts...")
        await asyncio.gather(*(account.undeploy() for account in accounts))
        print("All accounts undeployed.")

        end_time = time.time()  # End timing the process
        print(f'Total time taken: {end_time - start_time:.2f} seconds')
        
    return account_data


# Example usage
async def main():
    account_ids = ['573b4688-0b9d-4b26-b38d-742de1248235', 'ab9bbaba-bc20-440d-9b3a-fa2e9a72267f']
    account_data = await batch_deploy_and_fetch(api_token, account_ids)
    print(account_data)

asyncio.run(main())

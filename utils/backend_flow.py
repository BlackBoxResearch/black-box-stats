'''
Overview: The purpose of this file is to step by step test the 
concept flow of our apps backend, from deploying an account to 
MetaAPI, fetching historical deals and converting to positions, 
to real-time streaming to listen for new deals.
'''

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
TEST_ACCOUNT_2 = '573b4688-0b9d-4b26-b38d-742de1248235'

def add_user(first_name, last_name, email, country, password_hash, password_hint, marketing):
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

    # Execute the query without fetching results
    execute_query(query, params, fetch_results=False)


async def deploy_account(login, password, server_name, platform):
    '''
    Step 2: Deploy a new account to MetaAPI.
    '''
    api = MetaApi(TOKEN)
    api_account_id = ''

    try:
        # Get the list of accounts and find the matching one
        accounts = await api.metatrader_account_api.get_accounts_with_infinite_scroll_pagination()
        account = None
        for item in accounts:
            if item.login == login and item.type.startswith('cloud'):
                account = item
                break

        # If the account exists, save the ID
        if account:
            api_account_id = account.id
            print('Account already exists on MetaAPI!')
        else:
            # If the account doesn't exist on MetaAPI, create it
            print('Adding account.')
            account = await api.metatrader_account_api.create_account(
                {
                    'name': 'Test account',
                    'type': 'cloud',
                    'login': login,
                    'password': password,
                    'server': server_name,
                    'platform': platform,
                    'application': 'MetaApi',
                    'magic': 1000,
                }
            )
            api_account_id = account.id

        # Deploy the account and wait until it's connected
        print('Deploying account')
        await account.deploy()

    except Exception as e:
        print(f"Error in adding account: {e}")


async def get_account_info(account_id):
    api = MetaApi(TOKEN)

    try:
        # Retrieve MetaApi account
        account = await api.metatrader_account_api.get_account(TEST_ACCOUNT_1)

        await account.wait_connected()
        connection = account.get_rpc_connection()
        await connection.connect()
        await connection.wait_synchronized()

        account_info = await connection.get_account_information()
        print(account_info)

    except Exception as e:
        print(f"Error in continuous_streaming: {e}")


if __name__ == "__main__":
    asyncio.run(get_account_info(TEST_ACCOUNT_1))

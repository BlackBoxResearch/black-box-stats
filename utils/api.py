from metaapi_cloud_sdk import MetaApi
from metaapi_cloud_sdk import MetaStats
import asyncio
import streamlit as st
from datetime import datetime

api_token = 'eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiJiMzIyZjNiOTlmZGM4YmUxOTJmNGY5Y2QwNzRmMjRjYSIsInBlcm1pc3Npb25zIjpbXSwiYWNjZXNzUnVsZXMiOlt7ImlkIjoidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpIiwibWV0aG9kcyI6WyJ0cmFkaW5nLWFjY291bnQtbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZXN0LWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1ycGMtYXBpIiwibWV0aG9kcyI6WyJtZXRhYXBpLWFwaTp3czpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZWFsLXRpbWUtc3RyZWFtaW5nLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFzdGF0cy1hcGkiLCJtZXRob2RzIjpbIm1ldGFzdGF0cy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoicmlzay1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsicmlzay1tYW5hZ2VtZW50LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJjb3B5ZmFjdG9yeS1hcGkiLCJtZXRob2RzIjpbImNvcHlmYWN0b3J5LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtdC1tYW5hZ2VyLWFwaSIsIm1ldGhvZHMiOlsibXQtbWFuYWdlci1hcGk6cmVzdDpkZWFsaW5nOio6KiIsIm10LW1hbmFnZXItYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6ImJpbGxpbmctYXBpIiwibWV0aG9kcyI6WyJiaWxsaW5nLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19XSwidG9rZW5JZCI6IjIwMjEwMjEzIiwiaW1wZXJzb25hdGVkIjpmYWxzZSwicmVhbFVzZXJJZCI6ImIzMjJmM2I5OWZkYzhiZTE5MmY0ZjljZDA3NGYyNGNhIiwiaWF0IjoxNzI5OTE0NjA0LCJleHAiOjE3Mzc2OTA2MDR9.K4iIWm0547TBw9G_lyxJezZ_sYr9uAKhYBAyLBQ5cwho-aVToMg9RqFM7zjzS0RRXY4xuShm0nLo5_xVyLpLMtkq1vzoU01Rdc0_YEUt89ITCxM62nYJvJngqE6rgyN-zLxRtelkIqbr_AYQpPh03QdvMacypHC8qTtchLEO-c94yT2KHm796pd1cD7hcvAItmFq4RbF2Dv2Gv9EDCvnKu-9rV6AkA_W9g0eY5X-F4P8Qi6SvOn6cvwhbKk3y8cxd733u7RRvlmd1N0X75cv7s2nSzS5pW3XQTmKCb7Ky-m0HLfJn6UDHn4giX-PBr-IELMQM4jwmmauEzqtTRDhllVdvuE-G1K7YG9afotA3Nsyw00CZrarwpH-SIkO-mZyQ4doaAzYNtIp-O5UJ6nkzv_pVxwozMWgg-5ebyLwUFhIObJylyoN7GsVl2fNDSvWiu2mW84Yx1cavYekMmPVfOhshF2-uRN9Bkuk7OCPm4BYhxx2oxkvnr2C8U5Gzra9UsQFP9u1kwJ814BdBihYImKAPD4x6GOcRJFpRaj9Rk-HkwYD8Mk0qSxkNL1GmDrfGsp_0JI0LCfyKFat30vrs3etu3c4tzmOG0M1T1zCUHviaOYAngmI3pabNlkTdtU7XkQK9476HZq4dxiWhW8eD3Dat_oDadSkcqfJ3ueMOgQ'

async def AddAccount(user_id, login, password, server_name, platform):
    global api_account_id
    api = MetaApi(api_token)

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

        # # Deploy the account and wait until it's connected
        #print('Deploying account')
        #await account.deploy()
        # print('Waiting for API server to connect to broker (may take a couple of minutes)')
        # await account.wait_connected()

        # Add or update the account in the database
        conn = st.connection('analytiq_db', type='sql')

        with conn.session as s:
            try:
                # Check if the account exists in the database with a 'disconnected' status
                result = s.execute('''
                    SELECT user_id, connection_status
                    FROM accounts
                    WHERE account_number = :account_number AND server_name = :server_name
                ''', {
                    'account_number': login,
                    'server_name': server_name
                }).fetchone()

                # If the account exists in the database
                if result:
                    db_user_id, db_connection_status = result

                    # If it's registered to the same user and is 'disconnected', update to 'connected'
                    if db_user_id == user_id and db_connection_status == 'disconnected':
                        s.execute('''
                            UPDATE accounts
                            SET connection_status = :new_status, api_account_id = :api_account_id
                            WHERE account_number = :account_number AND server_name = :server_name AND user_id = :user_id
                        ''', {
                            'new_status': 'connected',
                            'api_account_id': api_account_id,
                            'account_number': login,
                            'server_name': server_name,
                            'user_id': user_id
                        })
                        print(f"Account {login} reconnected for user {user_id}.")
                    else:
                        # If the account is registered to a different user, return an error message
                        error_message = f"Account {login} is already registered to another user."
                        print(error_message)
                        return None, None, error_message
                else:
                    # If the account doesn't exist in the database, insert it as a new row
                    s.execute('''
                        INSERT INTO accounts (user_id, account_number, server_name, platform, api_account_id, connection_status)
                        VALUES (:user_id, :account_number, :server_name, :platform, :api_account_id, :connection_status)
                    ''', {
                        'user_id': user_id,
                        'account_number': login,
                        'server_name': server_name,
                        'platform': platform,
                        'api_account_id': api_account_id,
                        'connection_status': "connected"
                    })
                    print(f"Account {login} added to the database.")

                # Commit the transaction to save changes
                s.commit()

            except Exception as e:
                error_message = f"An error occurred while trying to add or update the account: {str(e)}"
                print(error_message)
                return None, None, error_message

        # Optionally, you can return if the account is a demo or live based on the `account` object if available
        return api_account_id, account.name, None

    except Exception as err:
        # Handle exceptions and print error details
        if hasattr(err, 'details'):
            if err.details == 'E_SRV_NOT_FOUND':
                error_message = 'Server not found: ' + str(err)
            elif err.details == 'E_AUTH':
                error_message = 'Authentication error: ' + str(err)
            elif err.details == 'E_SERVER_TIMEZONE':
                error_message = 'Server timezone issue: ' + str(err)
            else:
                error_message = api.format_error(err)
        else:
            error_message = api.format_error(err)

        print(error_message)
        return None, None, error_message

async def RemoveAccount(account_id):
    api = MetaApi(api_token)
    try:
        # Get the specified account
        account = await api.metatrader_account_api.get_account(account_id)
        if account:
            # Attempt to remove the account
            await account.remove()
            print('Account removed.')

            # Update the connection status of the account in the database
            conn = st.connection('analytiq_db', type='sql')

            with conn.session as s:
                try:
                    # Update the connection_status to "disconnected"
                    s.execute('''
                        UPDATE accounts
                        SET connection_status = :new_status
                        WHERE api_account_id = :account_id
                    ''', {
                        'new_status': "disconnected",
                        'account_id': account_id
                    })

                    # Commit the transaction to save changes
                    s.commit()
                    print(f"Account {account_id} status updated to disconnected.")
                    return True  # Return True to indicate success
                except Exception as e:
                    print(f"An error occurred while updating the account status: {e}")
                    return False
        else:
            print('Account does not exist!')
            return False
    except Exception as e:
        print(f"An error occurred while removing the account: {e}")
        return False

async def FetchStats(api_account_id, account_id, user_id, login):
    api = MetaApi(api_token)
    meta_stats = MetaStats(api_token)

    try:
        # Get the specified account
        account = await api.metatrader_account_api.get_account(api_account_id)

        if account:
            print('Deploying account')
            await account.deploy()

            print('Waiting for API server to connect to broker (may take a couple of minutes)')
            await account.wait_connected()

            # Connect to MetaApi
            connection = account.get_rpc_connection()
            await connection.connect()

            # Wait until the terminal state is synchronized
            print('Waiting for SDK to synchronize to terminal state (may take some time depending on your history size)')
            await connection.wait_synchronized()

            # Fetch and return the required metrics
            metrics = await meta_stats.get_metrics(api_account_id)

            # Fetch trades within a specified time range
            trades = await meta_stats.get_account_trades(api_account_id, '2000-01-01 00:00:00.000',
                                                         datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])

            # Close the connection and undeploy the account
            await connection.close()
            await account.undeploy()

            # Add trades to the database
            conn = st.connection('analytiq_db', type='sql')
            with conn.session as s:
                for trade in trades:
                    # Print each trade structure to inspect its contents
                    print("Trade data structure:", trade)

                    # Only proceed if essential fields are present, e.g., 'symbol' for a trade
                    if 'symbol' in trade and 'volume' in trade:
                        s.execute('''
                            INSERT INTO trades (user_id, account_id, api_account_id, login, ticket, symbol, type, volume,
                                                open_time, open_price, close_time, close_price, profit, pips, gain, success, duration_mins)
                            VALUES (:user_id, :account_id, :api_account_id, :login, :ticket, :symbol, :type, :volume,
                                    :open_time, :open_price, :close_time, :close_price, :profit, :pips, :gain, :success, :duration_mins)
                        ''', {
                            'user_id': user_id,
                            'account_id': account_id,
                            'api_account_id': api_account_id,
                            'login': login,
                            'ticket': trade.get('positionId', trade.get('_id')),  # Use '_id' if 'positionId' is missing
                            'symbol': trade['symbol'],
                            'type': trade['type'],
                            'volume': trade['volume'],
                            'open_time': trade['openTime'],
                            'open_price': trade.get('openPrice', None),
                            'close_time': trade['closeTime'],
                            'close_price': trade.get('closePrice', None),
                            'profit': trade['profit'],
                            'pips': trade.get('pips', 0),  # Default pips to 0 if not present
                            'gain': trade.get('gain', 0),  # Default gain to 0 if not present
                            'success': trade.get('success', 'unknown'),  # Default success to 'unknown' if not present
                            'duration_mins': trade.get('durationInMinutes', 0)  # Default duration to 0 if not present
                        })
                s.commit()
            print("Trades added to the database.")

            return metrics  # Return the fetched metrics

        else:
            print('Account does not exist!')
            return None

    except Exception as err:
        # Handle specific error cases and return None if an error occurs
        if hasattr(err, 'details'):
            if err.details == 'E_SRV_NOT_FOUND':
                print('Server not found:', err)
            elif err.details == 'E_AUTH':
                print('Authentication error:', err)
            elif err.details == 'E_SERVER_TIMEZONE':
                print('Server timezone issue:', err)
        else:
            print('Unexpected error:', api.format_error(err))

        return None  # Return None for any exception

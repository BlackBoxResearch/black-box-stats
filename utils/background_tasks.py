import streamlit as st
import asyncio
from utils.api import FetchStats
import datetime

@st.fragment(run_every="5m")  # Run every 5 minutes
async def batch_update_stats():
    # Connect to the database to fetch all accounts marked as 'connected'
    conn = st.connection('analytiq_db', type='sql')
    with conn.session as s:
        connected_accounts = s.execute(
            '''
            SELECT api_account_id, account_id, user_id, account_number
            FROM accounts
            WHERE connection_status = 'connected'
            '''
        ).fetchall()

    # Run FetchStats for each connected account
    for account in connected_accounts:
        api_account_id, account_id, user_id, login = account
        await FetchStats(api_account_id, account_id, user_id, login)

    # Optionally, update a timestamp in session state to track the last run
    st.session_state["last_update_time"] = datetime.datetime.now()

# Function to initialize the background process
def initialize_background_updates():
    # Only start the fragment once per session
    if "background_initialized" not in st.session_state:
        # Use asyncio.run to ensure the coroutine is awaited
        asyncio.run(batch_update_stats())
        st.session_state["background_initialized"] = True

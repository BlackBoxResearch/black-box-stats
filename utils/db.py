from sqlalchemy.sql import text
import streamlit as st


def execute_query(query, params=None):
    """
    Executes a read-only SQL query and returns the result.
    Args:
        query (str): The SQL query to execute.
        params (dict): Parameters for the query, if any.
    Returns:
        list: List of rows resulting from the query.
    """
    conn = st.connection('blackboxstats_db', type='sql')
    with conn.session as s:
        try:
            # Mark the query as a text object
            result = s.execute(text(query), params or {})
            return result.fetchall()
        except Exception as e:
            st.error(f"Error executing query: {e}")
            return []


def execute_write(query, params=None):
    """
    Executes a write (INSERT/UPDATE/DELETE) SQL query and commits the changes.
    Args:
        query (str): The SQL query to execute.
        params (dict): Parameters for the query, if any.
    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    conn = st.connection('blackboxstats_db', type='sql')
    with conn.session as s:
        try:
            # Execute the query
            s.execute(text(query), params or {})
            # Commit the transaction
            s.commit()
            st.success("Operation successful!")
            return True
        except Exception as e:
            # Rollback in case of an error
            s.rollback()
            st.error(f"Error executing write operation: {e}")
            return False


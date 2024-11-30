import hashlib
import streamlit as st
from utils.db import execute_query, execute_write

def hash_password(password):
    """
    Hashes a plaintext password using SHA-256 encryption.
    
    Args:
        password (str): The plaintext password to be hashed.
    
    Returns:
        str: The resulting SHA-256 hash of the password.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def check_login(email, password):
    """
    Validates user credentials by checking the email and password against the database.

    Args:
        email (str): The email address of the user.
        password (str): The plaintext password provided by the user.

    Returns:
        tuple: A tuple containing the user's details (user_id, email, first_name, last_name, subscription_level)
               if the credentials are valid. Returns (None, None, None, None, None) otherwise.
    """
    # Query to fetch user details by email
    query = '''
        SELECT user_id, email, first_name, last_name, subscription_level, password_hash
        FROM users
        WHERE email = :email
    '''
    # Execute the query to get the user details
    result = execute_query(query, {'email': email})

    if result:
        # Extract user details
        user_id, email, first_name, last_name, subscription_level, password_hash = result[0]
        print(f"User found: {email}, {first_name}, {subscription_level}")
        print(f"Stored hash: {password_hash}")
        print(f"Computed hash: {hash_password(password)}")

        # Validate the password
        if hash_password(password) == password_hash:
            return user_id, email, first_name, last_name, subscription_level

    # Return None values if authentication fails
    return None, None, None, None, None

def register_user(first_name, last_name, email, country, password, password_hint):
    """
    Registers a new user in the database.
    Args:
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        email (str): Email address of the user.
        country (str): Country of the user.
        password (str): Plaintext password of the user.
        password_hint (str): Password hint for the user.
    """
    # Check if the email already exists
    query_check = 'SELECT email FROM users WHERE email = :email'
    existing_user = execute_query(query_check, {'email': email})

    if existing_user:
        st.error("User already exists. Please use a different email.")
    else:
        # Hash the password before storing it
        password_hash = hash_password(password)
        # Insert the new user
        query_insert = '''
            INSERT INTO users (first_name, last_name, email, country, password_hash, password_hint)
            VALUES (:first_name, :last_name, :email, :country, :password_hash, :password_hint)
        '''
        params = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'country': country,
            'password_hash': password_hash,
            'password_hint': password_hint
        }
        # Execute the write operation
        if execute_write(query_insert, params):
            st.success("Registration successful! You can now log in with your credentials.")



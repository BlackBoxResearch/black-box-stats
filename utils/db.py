import psycopg2
from psycopg2.extras import RealDictCursor

# Database connection parameters
DB_HOST = "analytiq-test-database.c102eee68lij.eu-west-2.rds.amazonaws.com"
DB_PORT = 5432
DB_NAME = "postgres"
DB_USER = "blackboxresearch"
DB_PASSWORD = "!Audacious2011"

def execute_query(query, params=None, fetch_results=True):
    """
    Executes a SQL query and optionally fetches results.
    Args:
        query (str): The SQL query to execute.
        params (tuple or dict): Parameters for the query, if any.
        fetch_results (bool): Whether to fetch results (for SELECT queries).
    Returns:
        list or None: Query results or None for write operations.
    """
    try:
        # Connect to the PostgreSQL database
        with psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        ) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Execute the query with parameters
                cursor.execute(query, params)

                # Commit for write queries
                if not fetch_results:
                    conn.commit()
                    print("Query executed and committed successfully.")
                    return None

                # Fetch and return results for read-only queries
                result = cursor.fetchall()
                print("Query executed successfully.")
                return result

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
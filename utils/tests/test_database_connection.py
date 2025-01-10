import psycopg2

# Database connection parameters
DB_HOST = "analytiq-test-database.c102eee68lij.eu-west-2.rds.amazonaws.com"
DB_PORT = 5432
DB_NAME = "postgres"
DB_USER = "blackboxresearch"
DB_PASSWORD = "!Audacious2011"

try:
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    print("Connected to the AWS RDS PostgreSQL database!")
    
    # Open a cursor to execute SQL commands
    cursor = conn.cursor()

    # Create the trades table
    create_table_query = """
    CREATE TABLE trades (
        id SERIAL PRIMARY KEY,
        account_id VARCHAR(50) NOT NULL,
        position_id VARCHAR(50) UNIQUE NOT NULL,
        symbol VARCHAR(20) NOT NULL,
        volume NUMERIC(12, 4) NOT NULL,
        type VARCHAR(4) NOT NULL CHECK (type IN ('BUY', 'SELL')),
        open_time TIMESTAMP WITH TIME ZONE NOT NULL,
        open_price NUMERIC(12, 5) NOT NULL,
        stop_loss NUMERIC(12, 5),
        take_profit NUMERIC(12, 5),
        close_time TIMESTAMP WITH TIME ZONE,
        close_price NUMERIC(12, 5),
        commission NUMERIC(15, 2) NOT NULL DEFAULT 0.00,
        swap NUMERIC(15, 2) NOT NULL DEFAULT 0.00,
        profit NUMERIC(15, 2) NOT NULL DEFAULT 0.00,
        gain NUMERIC(15, 2) DEFAULT NULL, -- Add gain column (e.g., numeric to track percentage gain or value gain)
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
    );
    """

    cursor.execute(create_table_query)
    conn.commit()  # Commit the changes
    print("Trades table created successfully!")

    # Close the cursor and connection
    cursor.close()
    conn.close()

except Exception as e:
    print(f"An error occurred: {e}")

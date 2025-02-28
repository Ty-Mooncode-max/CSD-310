"""
Tyler Moon
02/27/2025
Assignment 10.1
"""
import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values

# Load .env file
secrets = dotenv_values(".env")

# Database configuration
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True
}

# Test connection
try:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    print(f"Connected to database: {config['database']}")
    
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist")
    else:
        print(err)
    exit(1)  # Exit if connection fails


# Function to fetch and display tables in the Winery database
def show_tables():
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    return [table[0] for table in tables]


# Function to fetch and display data from all tables
def fetch_all_tables_data():
    # Get all tables in the Winery database
    tables = show_tables()

    # Loop through each table
    for table in tables:
        print(f"\nTable: {table}")

        # Query to fetch all data from the current table
        query = f"SELECT * FROM {table}"
        cursor.execute(query)

        # Fetch all rows from the result
        rows = cursor.fetchall()

        # Fetch column names to display them as headers
        columns = [desc[0] for desc in cursor.description]

        # Print the column names (formatted as headers)
        print(" | ".join(columns))
        print("-" * 50)

        # Print each row of data
        for row in rows:
            print(" | ".join(str(cell) for cell in row))

        print("-" * 50)


# Fetch and display data from all tables
fetch_all_tables_data()

# Close the cursor and connection when done
cursor.close()
connection.close()

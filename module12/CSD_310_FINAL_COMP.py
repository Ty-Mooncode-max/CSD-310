"""
Tyler Moon, Destiny Bazan
3/8/2025
Assignment 11.1
"""
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import os
from datetime import datetime
from tabulate import tabulate

# Load .env file
load_dotenv(".env")

# Database configuration using environment variables
config = {
    "user": os.getenv("USER"),
    "password": os.getenv("PASSWORD"),
    "host": os.getenv("HOST"),
    "database": os.getenv("DATABASE"),
}

# Connect to the database
try:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    print("Connected to the database.")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password are invalid.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist.")
    else:
        print(f"Error: {err}")
    exit(1)

# TABLES SECTION
print("\nTABLES\n" + "=" * 50)

# Function to fetch and display tables in the Winery database
def show_tables():
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    return [table[0] for table in tables]


# Function to fetch and display data from all tables
def fetch_all_tables_data():
    tables = show_tables()  # Get all table names

    for table in tables:
        print(f"\nTable: {table}")

        query = f"SELECT * FROM {table}"
        cursor.execute(query)
        rows = cursor.fetchall()

        # Fetch column names
        columns = [desc[0] for desc in cursor.description]

        # Print headers
        print(" | ".join(columns))
        print("-" * 50)

        # Print row data
        for row in rows:
            print(" | ".join(str(cell) for cell in row))

        print("-" * 50)


# Fetch and display tables first
fetch_all_tables_data()

# REPORTS SECTION
print("\nREPORTS\n" + "=" * 50)

def print_report_with_header(report_name, query, columns):
    cursor.execute(query)
    results = cursor.fetchall()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"\n{report_name} (Generated on {current_time})")
    print("-" * 50)
    print(tabulate(results, headers=columns, tablefmt='pretty'))


# 1. Report Tracking Supplier Performance
def supplier_performance_report():
    query = """
    SELECT 
        S.Name as SupplierName,
        SO.OrderDate,
        SO.ExpectedDelivery,
        SO.ActualDelivery,
        DATEDIFF(SO.ActualDelivery, SO.ExpectedDelivery) as DeliveryDifference
    FROM 
        Supplier S
    JOIN 
        SupplyOrder SO ON S.SupplierID = SO.SupplierID
    WHERE 
        SO.ExpectedDelivery IS NOT NULL
    """
    print_report_with_header("Supplier Performance Report", query,
                             ["Supplier Name", "Order Date", "Expected Delivery", "Actual Delivery",
                              "Delivery Difference (days)"])


# 2. Wine Sales by Type and Distributor
def wine_sales_report():
    query = """
    SELECT 
        W.WineName,
        W.WineType,
        D.Name as DistributorName,
        SUM(SR.SalesVolume) as TotalSales
    FROM 
        Wine W
    JOIN 
        WineDistribution WD ON W.WineID = WD.WineID
    JOIN 
        Distributor D ON WD.DistributorID = D.DistributorID
    JOIN 
        SalesReport SR ON W.WineID = SR.WineID
    GROUP BY 
        W.WineName, W.WineType, D.Name
    ORDER BY 
        TotalSales DESC
    """
    print_report_with_header("Wine Sales Report", query, ["Wine Name", "Wine Type", "Distributor Name", "Total Sales"])


# 3. Employee Hours Report
def employee_hours_report():
    query = """
    SELECT 
        E.Name, 
        SUM(E.WorkWeekHours) as TotalHours
    FROM 
        Employee E
    GROUP BY 
        E.Name
    """
    print_report_with_header("Employee Hours Report (Last Four Quarters)", query,
                             ["Employee Name", "Total Hours Worked"])


# Generate reports
supplier_performance_report()
wine_sales_report()
employee_hours_report()

# Close the cursor and connection
cursor.close()
connection.close()



"""
Tyler Moon, Destiny Bazan, Cassiany Noel
3/1/2025
Assignment 11.1
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
    cursor.execute(query)
    results = cursor.fetchall()

    print("\nSupplier Performance Report")
    print("-" * 50)
    for row in results:
        print(
            f"Supplier: {row[0]}, Order Date: {row[1]}, Expected Delivery: {row[2]}, Actual Delivery: {row[3]}, Delivery Difference: {row[4]} days")


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
    cursor.execute(query)
    results = cursor.fetchall()

    print("\nWine Sales Report")
    print("-" * 50)
    best_selling = {}
    worst_selling = {}

    for row in results:
        print(f"Wine: {row[0]}, Type: {row[1]}, Distributor: {row[2]}, Total Sales: {row[3]}")

        # Tracking best and worst selling wines
        if row[1] not in best_selling:
            best_selling[row[1]] = (row[0], row[3])
            worst_selling[row[1]] = (row[0], row[3])
        else:
            if row[3] > best_selling[row[1]][1]:
                best_selling[row[1]] = (row[0], row[3])
            if row[3] < worst_selling[row[1]][1]:
                worst_selling[row[1]] = (row[0], row[3])

    print("\nBest Selling Wines by Type:")
    for wine_type, data in best_selling.items():
        print(f"Type: {wine_type}, Wine: {data[0]}, Total Sales: {data[1]}")

    print("\nWorst Selling Wines by Type:")
    for wine_type, data in worst_selling.items():
        print(f"Type: {wine_type}, Wine: {data[0]}, Total Sales: {data[1]}")


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
    cursor.execute(query)
    results = cursor.fetchall()

    print("\nEmployee Hours Report (Last Four Quarters)")
    print("-" * 50)
    for row in results:
        print(f"Employee: {row[0]}, Total Hours Worked: {row[1]} hours")


# Generate reports
supplier_performance_report()
wine_sales_report()
employee_hours_report()

# Close cursor and connection
cursor.close()
connection.close()


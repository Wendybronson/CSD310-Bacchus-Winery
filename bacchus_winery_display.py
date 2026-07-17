# ---------------------------------------------------------
# Group C
# Wendy Bronson
# Eric Sengvanhpheng
# William Judd
# Luis Cortez
# Martha Guzman
#
# July 2026
# Database Development and Use
# Module 9.1 Milestone #2
# Case Study: Bacchus Winery
#
# Purpose:
# Connect to the Bacchus Winery MySQL database and provide
# the main program structure used to display database tables.
# ---------------------------------------------------------

import mysql.connector
from mysql.connector import Error

from db_config import DATABASE_CONFIG


def create_database_connection():
    """
    Creates and returns a connection to the Bacchus Winery
    MySQL database.

    Returns:
        MySQLConnection: An active database connection.

    Raises:
        Error: If MySQL cannot establish the connection.
    """

    connection = mysql.connector.connect(**DATABASE_CONFIG)

    if connection.is_connected():
        print("Successfully connected to the Bacchus Winery database.")

    return connection
def display_table(cursor, table_name, display_title):
    """
    Displays all records from a database table.
    """

    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    column_names = [column[0] for column in cursor.description]

    print("\n" + "=" * 80)
    print(display_title)
    print("=" * 80)

    print(" | ".join(column_names))
    print("-" * 80)

    if not rows:
        print("No records found.")
    else:
        for row in rows:
            values = []

            for value in row:
                if value is None:
                    values.append("NULL")
                else:
                    values.append(str(value))

            print(" | ".join(values))

    print()

def display_employee_tables(cursor):
        """
        Displays the employee-related tables.
        """

        display_table(cursor, "department", "DEPARTMENT TABLE")
        display_table(cursor, "employee", "EMPLOYEE TABLE")
        display_table(cursor, "employee_time", "EMPLOYEE TIME TABLE")

def display_supplier_inventory_tables(cursor):
    """
    Displays the supplier and inventory-related tables.
    """

    display_table(cursor, "supplier", "SUPPLIER TABLE")
    display_table(cursor, "inventory_item", "INVENTORY ITEM TABLE")
    display_table(cursor, "supplier_delivery", "SUPPLIER DELIVERY TABLE")
    display_table(
        cursor,
        "supplier_delivery_item",
        "SUPPLIER DELIVERY ITEM TABLE"
    )
def main():
    """
    Controls the main program and manages the database
    connection and cursor.
    """

    connection = None
    cursor = None

    try:
        connection = create_database_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT DATABASE();")
        selected_database = cursor.fetchone()

        if selected_database:
            print(f"Current database: {selected_database[0]}")

        # Display the employee-related tables
        display_employee_tables(cursor)
        # Display the supplier and inventory-related tables
        display_supplier_inventory_tables(cursor)

    except Error as error:
        print(f"\nUnable to connect to the MySQL database.")
        print(f"MySQL error: {error}")

    finally:
        if cursor is not None:
            cursor.close()
            print("Database cursor closed.")

        if connection is not None and connection.is_connected():
            connection.close()
            print("MySQL connection closed.")


if __name__ == "__main__":
    main()
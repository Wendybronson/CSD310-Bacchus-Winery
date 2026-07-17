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

        # This test query confirms that Python is connected
        # to the correct MySQL database.
        cursor.execute("SELECT DATABASE();")
        selected_database = cursor.fetchone()

        if selected_database:
            print(f"Current database: {selected_database[0]}")

        # The table-display functions created by the team
        # will be called from this section later.

    except Error as error:
        print("\nUnable to connect to the MySQL database.")
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
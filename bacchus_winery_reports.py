# ---------------------------------------------------------
# Group C
# Wendy Bronson
# Eric Sengvanhpheng
# William Judd
# Luis Cortez
# Martha Guzman
#
# July 22, 2026
# Database Development and Use
# Module 10.1 Milestone #3
# Case Study: Bacchus Winery
#
# Purpose:
# Connect to the Bacchus Winery MySQL database and provide
# three business reports.
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


def display_table(cursor, query, display_title):
    """
    Displays a database table with formatted column headings 
    and aligned output.
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]

    # create empty list, convert values to strings and replace NULL values
    formatted_rows = []

    for row in rows:
        formatted_rows.append(
            [
                "NULL" if value is None else str(value)
                for value in row
            ]
        )

    # calculate the width needed for each column
    column_widths = []

    for index, column in enumerate(column_names):
        max_width = len(column)

        for row in formatted_rows:
            max_width = max(max_width, len(row[index]))
        
        column_widths.append(max_width)

    # build formatted table header using calculated column widths
    header = " | ".join(
        column_names[i].ljust(column_widths[i])
        for i in range(len(column_names))
    )

    print("\n" + "=" * len(header))
    print(display_title)
    print("=" * len(header))
    
    print(header)
    print("-" * len(header))

    # display each row using the calculated column widths
    for row in formatted_rows:
        print(
            " | ".join(
                row[i].ljust(column_widths[i])
                for i in range(len(row))
            )
        )

    print()


# =========================================================
# REPORT: SUPPLIER DELIVERY PERFORMANCE
#
# Summarizes supplier delivery performance by month.
# Calculates average delivery delays to identify suppliers
# that may have late delivery issues
# =========================================================

def supplier_delivery_monthly_report(cursor):
    query = """
    SELECT
        s.supplier_name,
        MONTH(sd.expected_delivery_date) AS delivery_month_number,
        MONTHNAME(sd.expected_delivery_date) AS delivery_month, 
        COUNT(sd.delivery_id) AS total_deliveries,
        AVG(
            DATEDIFF(
                sd.actual_delivery_date,
                sd.expected_delivery_date
            )
        ) AS avg_days_late
    FROM supplier AS s
    JOIN supplier_delivery AS sd
        ON s.supplier_id = sd.supplier_id
    GROUP BY
        s.supplier_name,
        MONTH(sd.expected_delivery_date),
        MONTHNAME(sd.expected_delivery_date)
    ORDER BY 
        MONTH(sd.expected_delivery_date),
        avg_days_late DESC;
    """

    display_table(
        cursor,
        query,
        "MONTHLY SUPPLIER DELIVERY PERFORMANCE"
)

# =========================================================
# REPORT: WINE DISTRIBUTION
#
# Displays wine sales by distributor, including the total
# quantity ordered and total sales revenue. 
# Helps identify which wines are selling well and which
# distributors carry each wine.
# =========================================================

def wine_distribution(cursor):
    query= """
    SELECT
        w.wine_name,
        d.distributor_name,
        SUM(od.quantity_ordered) AS total_quantity_ordered,
        SUM(
            od.quantity_ordered * od.price_at_purchase
        ) AS total_sales
    FROM wine AS w
    JOIN order_detail AS od
        ON w.wine_id = od.wine_id
    JOIN distributor_order AS dor
        ON od.order_id = dor.order_id
    JOIN distributor AS d
        ON dor.distributor_id = d.distributor_id
    GROUP BY
        w.wine_id,
        w.wine_name,
        d.distributor_name
    ORDER BY 
        total_quantity_ordered DESC;
    """

    display_table(
        cursor,
        query,
        "WINE DISTRIBUTION"
)

# =========================================================
# REPORT: EMPLOYEE HOURS BY QUARTER
#
# Displays employee hours per quarter throughout four quarters.
# =========================================================

def employees_hours_quarter(cursor):
    query= """
    SELECT
        e.employee_id,
        CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
        YEAR(et.work_date) AS work_year,
        QUARTER(et.work_date) AS work_quarter,
        SUM(et.hours_worked) AS total_hours
    FROM employee AS e
    JOIN employee_time AS et
        ON e.employee_id = et.employee_id
    WHERE et.work_date >= DATE_SUB(
        (SELECT MAX(work_date) FROM employee_time),
        INTERVAL 4 QUARTER
    )
    GROUP BY
        e.employee_id,
        e.first_name,
        e.last_name,
        YEAR(et.work_date),
        QUARTER(et.work_date)
    ORDER BY
        e.employee_id,
        work_year,
        work_quarter;
    """

    display_table(
        cursor,
        query,
        "EMPLOYEE HOURS BY QUARTER"
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

        # Call report functions
        supplier_delivery_monthly_report(cursor)
        wine_distribution(cursor)
        employees_hours_quarter(cursor)


    except Error as error:
        print(f"\nA database error occurreed.")
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
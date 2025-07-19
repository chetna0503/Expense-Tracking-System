import logging

import mysql.connector
from contextlib import contextmanager
from backend.logging_setup import setup_logger

logger = setup_logger("db_helper")

@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="557799",
        database="expense_manager"
    )

    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    print("Closing cursor")
    cursor.close()
    connection.close()


def fetch_all_records():
    query = "SELECT * from expenses"
    with get_db_cursor() as cursor:
        cursor.execute(query)
        expenses = cursor.fetchall()
        return expenses


def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        expenses = cursor.fetchall()
        return expenses


def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense called with date:{expense_date}, amount:{amount}, category: {category}, notes:{notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )


def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))


def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary with start_date:{start_date}, end_date:{end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT category, SUM(amount) as total 
                        FROM expenses 
                        WHERE expense_date BETWEEN %s AND %s 
                        GROUP BY category;''',
                       (start_date, end_date)
        )
        summary = cursor.fetchall()
        return summary


def fetch_monthly_expense_summary():
    logger.info(f"fetch_expense_summary_by_months")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT month(expense_date) as expense_month, 
               monthname(expense_date) as month_name,
               sum(amount) as total FROM expenses
               GROUP BY expense_month, month_name;
            '''
        )
        data = cursor.fetchall()
        return data


if __name__ == "__main__":
    print(fetch_monthly_expense_summary())







import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "database.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_sales_with_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.id, p.name, s.quantity, p.selling_price, 
               (s.quantity * p.selling_price) as total, s.created_at
        FROM sales s
        JOIN products p ON s.pid = p.id
        ORDER BY s.created_at DESC
    """)
    sales = cursor.fetchall()
    cursor.close()
    conn.close()
    return sales

def get_stock_with_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT st.id, p.name, st.stock_quantity, st.created_at
        FROM stock st
        JOIN products p ON st.pid = p.id
        ORDER BY st.created_at DESC
    """)
    stock = cursor.fetchall()
    cursor.close()
    conn.close()
    return stock

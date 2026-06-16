import psycopg2
from psycopg2 import Error

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "5758",
    "dbname": "myduka"
}

def get_db_connection():
    """Helper to create a connection"""
    return psycopg2.connect(**DB_CONFIG)

# ==========================
# 📦 PRODUCTS
# ==========================
def get_products():
    """Fetch all products"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name, buying_price, selling_price FROM products ORDER BY id")
        return cursor.fetchall()
    except Error as e:
        print(f"Error fetching products: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def insert_product(name, buying_price, selling_price):
    """Add a new product"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO products (name, buying_price, selling_price) VALUES (%s, %s, %s)",
            (name, buying_price, selling_price)
        )
        conn.commit()
        return True
    except Error as e:
        print(f"Error inserting product: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

# ==========================
# 📦 STOCK
# ==========================
def get_stock_with_products():
    """Fetch stock joined with product names"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT st.id, p.name, st.stock_quantity, st.created_at
            FROM stock st
            JOIN products p ON st.pid = p.id
            ORDER BY st.created_at DESC
        """)
        return cursor.fetchall()
    except Error as e:
        print(f"Error fetching stock: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def add_stock(pid, quantity):
    """Add stock for a specific product"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO stock (pid, stock_quantity) VALUES (%s, %s)",
            (pid, quantity)
        )
        conn.commit()
        return True
    except Error as e:
        print(f"Error adding stock: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def get_available_stock(pid):
    """Calculate: Total Stock Added - Total Sold"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Total added
        cursor.execute("SELECT COALESCE(SUM(stock_quantity), 0) FROM stock WHERE pid = %s", (pid,))
        total_stock = cursor.fetchone()[0]
        
        # Total sold
        cursor.execute("SELECT COALESCE(SUM(quantity), 0) FROM sales WHERE pid = %s", (pid,))
        total_sold = cursor.fetchone()[0]
        
        return total_stock - total_sold
    except Error as e:
        print(f"Error calculating stock: {e}")
        return 0
    finally:
        cursor.close()
        conn.close()

# ==========================
# 💰 SALES
# ==========================
def get_sales_with_products():
    """Fetch sales joined with product details"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT s.id, p.name, s.quantity, p.selling_price, 
                   (s.quantity * p.selling_price) as total, s.created_at
            FROM sales s
            JOIN products p ON s.pid = p.id
            ORDER BY s.created_at DESC
        """)
        return cursor.fetchall()
    except Error as e:
        print(f"Error fetching sales: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def add_sale(pid, quantity):
    """Record a sale"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO sales (pid, quantity) VALUES (%s, %s)",
            (pid, quantity)
        )
        conn.commit()
        return True
    except Error as e:
        print(f"Error recording sale: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

# ==========================
# 📊 DASHBOARD STATS
# ==========================
def get_dashboard_stats():
    """Get summary numbers for the dashboard"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        stats = {}
        
        cursor.execute("SELECT COUNT(*) FROM products")
        stats['total_products'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COALESCE(SUM(s.quantity * p.selling_price), 0) FROM sales s JOIN products p ON s.pid = p.id")
        stats['total_revenue'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COALESCE(SUM(st.stock_quantity * p.buying_price), 0) FROM stock st JOIN products p ON st.pid = p.id")
        stats['total_stock_value'] = cursor.fetchone()[0]
        
        return stats
    except Error as e:
        print(f"Error fetching stats: {e}")
        return {'total_products': 0, 'total_revenue': 0, 'total_stock_value': 0}
    finally:
        cursor.close()
        conn.close()
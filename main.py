from flask import Flask, render_template, request, redirect, url_for, flash
from database import (
    get_products,
    get_sales_with_products,
    get_stock_with_products,
    add_stock,
    add_sale,
    get_available_stock,
    insert_product,
    get_dashboard_stats
)

# Flask instance
app = Flask(__name__)
app.secret_key = "myduka_secret_key_123"  # Required for flash messages

@app.route('/')
def home():
    """Redirect home to dashboard"""
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    """Show dashboard with summary stats"""
    stats = get_dashboard_stats()
    return render_template('dashboard.html', stats=stats)

@app.route('/products')
def products():
    """Display all products"""
    products_data = get_products()
    return render_template('products.html', products=products_data)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    """Add a new product via form"""
    if request.method == 'POST':
        name = request.form['name'].strip()
        buying_price = float(request.form['buying_price'])
        selling_price = float(request.form['selling_price'])
        
        if buying_price < 0 or selling_price < 0:
            flash(' Prices cannot be negative!', 'danger')
            return redirect(url_for('add_product'))
        
        if selling_price < buying_price:
            flash(' Selling price is less than buying price!', 'warning')
        
        if insert_product(name, buying_price, selling_price):
            flash(f' Product "{name}" added successfully!', 'success')
            return redirect(url_for('products'))
        else:
            flash(' Failed to add product.', 'danger')
    
    return render_template('add_product.html')

@app.route('/stock')
def stock():
    """Display stock records with product names"""
    stock_data = get_stock_with_products()
    return render_template('stock.html', stock=stock_data)

@app.route('/add_stock', methods=['GET', 'POST'])
def add_stock_route():
    """Add stock via form"""
    if request.method == 'POST':
        pid = int(request.form['product_id'])
        quantity = int(request.form['quantity'])
        
        if quantity <= 0:
            flash(' Quantity must be greater than zero!', 'danger')
            return redirect(url_for('add_stock_route'))
        
        if add_stock(pid, quantity):
            # Get product name for message
            products = get_products()
            product_name = next((p[1] for p in products if p[0] == pid), "Unknown")
            flash(f'Added {quantity} units of "{product_name}" to stock!', 'success')
            return redirect(url_for('stock'))
        else:
            flash(' Failed to add stock.', 'danger')
    
    # GET: show form with product dropdown
    products = get_products()
    return render_template('add_stock.html', products=products)

@app.route('/sales')
def sales():
    """Display sales records with product details"""
    sales_data = get_sales_with_products()
    return render_template('sales.html', sales=sales_data)

@app.route('/add_sale', methods=['GET', 'POST'])
def add_sale_route():
    """Record a sale via form (with stock validation)"""
    if request.method == 'POST':
        pid = int(request.form['product_id'])
        quantity = int(request.form['quantity'])
        
        if quantity <= 0:
            flash(' Quantity must be greater than zero!', 'danger')
            return redirect(url_for('add_sale_route'))
        
        # 🔍 CRITICAL: Check available stock before allowing sale
        available = get_available_stock(pid)
        if quantity > available:
            products = get_products()
            product_name = next((p[1] for p in products if p[0] == pid), "Unknown")
            flash(f' Only {available} units of "{product_name}" available!', 'warning')
            return redirect(url_for('add_sale_route'))
        
        if add_sale(pid, quantity):
            products = get_products()
            product_name = next((p[1] for p in products if p[0] == pid), "Unknown")
            flash(f' Sold {quantity} units of "{product_name}"!', 'success')
            return redirect(url_for('sales'))
        else:
            flash(' Failed to record sale.', 'danger')
    
    # GET: show form with product dropdown
    products = get_products()
    return render_template('add_sale.html', products=products)

@app.route('/register')
def register():
    """Show registration form"""
    return render_template('register.html')

@app.route('/login')
def login():
    """Show login form"""
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout user (placeholder)"""
    flash(' You have been logged out.', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    # debug=True auto-reloads on code changes (development only)
    app.run(debug=True, port=5000)
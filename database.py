import psycopg2

connection = psycopg2.connect(
    host="localhost",
    port=5432,
    user="postgres",
    password="5758",
    dbname="myduka"
)

cursor = connection.cursor()

def get_products():
    cursor.execute("select * from products")
    products = cursor.fetchall()
    return products 

# 1. insert two record of sales in sql shell and use psycopg2 to display them in your terminal

def get_sales():
    cursor.execute("select * from sales")
    sales = cursor.fetchall()
    return sales



cursor.execute("Insert into products (name, buying_price, selling_price) values ('gaming chair', 1000, 1500)")
connection.commit()
products = get_products()
print(products)


def insert_product(name, buying_price, selling_price):
    cursor.execute("Insert into products (name, buying_price, selling_price) values (%s, %s, %s)", (name, buying_price, selling_price))
    connection.commit()

product3=("gaming table", 3000, 5000)
insert_product(product3[0], product3[1], product3[2])


def insert_stock(values):
    cursor.execute(f"insert into stock(pid,stock_quantity)values{values}")
    connection.commit()

stock1=(1,400)
stock2=(2,800)

insert_stock(stock1)
insert_stock(stock2)

def get_stock():
    cursor.execute("select * from stock")
    stock_data = cursor.fetchall()
    return stock_data
import mysql.connector
import json

my_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="777_zone"
)
my_cursor = my_db.cursor()

with open('sql.txt', 'r', encoding='utf-8') as f:
    list_products = json.load(f)

product_sql = "INSERT INTO products (brand_category_id, name, slug, price, quantity, specs, description) VALUES "
for product in reversed(list_products):
    brand_category_id = f"get_brand_category_id('{product['brand_name']}', 3)"
    name = product['name']
    slug = product['slug']
    price = product['price']
    quantity = product['quantity']
    specs = product['specs']
    description = product['description']
    product_sql += f"({brand_category_id}, '{name}', '{slug}', {price}, {quantity}, '{specs}', '{description}'),"
product_sql = product_sql.rstrip(",")

my_cursor.execute(product_sql)
my_db.commit()


# -----------PRODUCT IMAGE------------- #

image_sql = "INSERT INTO product_images (product_id, link, type) VALUES "
for product in reversed(list_products):
    product_id = f"get_product_id('{product['slug']}')"
    for image in product['images']:
        image_sql += f"({product_id}, '{image}', 'fptshop'),"
image_sql = image_sql.rstrip(",")

my_cursor.execute(image_sql)
my_db.commit()

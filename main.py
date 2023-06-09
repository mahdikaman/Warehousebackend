from flask_cors import CORS
from flask import Flask, Response, request
import mysql.connector
from mysql.connector import MySQLConnection
import threading
import datetime
import json
from decimal import Decimal

app = Flask(__name__)
CORS(app)

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


@app.route('/total', methods=['GET'])
def fetch_data_delivery():
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="AgueroAguero123!",
        database="exsitec"
    )
    cursor = connection.cursor()
    query = "SELECT ROW_NUMBER() OVER () AS ID, Product, Destination, SUM(Quantity) FROM Delivery GROUP BY Product, Destination"
    cursor.execute(query)
    rows = cursor.fetchall()

    data = []
    for row in rows:
        row_id = row[0]
        product = row[1]
        destination = row[2]
        sum_quantity = row[3]
        item = {
        "ID": row_id,
        "Product": product,
        "destination": destination,
        "Sum of quantity": sum_quantity
        }
        data.append(item)
         
    cursor.close()
    connection.close()
    json_data = json.dumps(data, cls=DecimalEncoder)
    # Have the headers to allow cross origin from frontend and have no cors problems
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    return Response(json_data, headers=headers)

@app.route('/products', methods=['GET'])
def fetch_data_products():
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="AgueroAguero123!",
        database="exsitec"
    )
    cursor = connection.cursor()
    query = "SELECT ID, ProductNumber, Name, Price FROM Products"
    cursor.execute(query)
    rows = cursor.fetchall()

    data = []
    for row in rows:
        row_id = row[0]
        product_number = row[1]
        produt_name = row[2]
        price = row[3]
        item = {
        "ID": row_id,
        "ProductNumber": product_number,
        "Name": produt_name,
        "Price": price
        }
        data.append(item)

    cursor.close()
    connection.close()
    json_data = json.dumps(data, cls=DecimalEncoder)
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    return Response(json_data, headers=headers)

@app.route('/inventory', methods=['GET'])
def fetch_data_inventory():
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="AgueroAguero123!",
        database="exsitec"
    )
    cursor = connection.cursor()
    query = "SELECT ID, InventoryNumber, City FROM Inventory"
    cursor.execute(query)
    rows = cursor.fetchall()

    data = []
    for row in rows:
        row_id = row[0]
        inventory_number = row[1]
        city = row[2]
        
        item = {
        "ID": row_id,
        "InventoryNumber": inventory_number,
        "City": city,
        }
        data.append(item)

    cursor.close()
    connection.close()
    json_data = json.dumps(data, cls=DecimalEncoder)
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    return Response(json_data, headers=headers)

@app.route('/add/delivery', methods=['POST'])
def insert_row_delivery():
    product = request.json.get('product')
    destination = request.json.get('destination')
    quantity = request.json.get('quantity')

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="AgueroAguero123!",
        database="exsitec"
    )
    cursor = connection.cursor()
    query = "INSERT INTO Delivery (Date, Product, Destination, Quantity) VALUES (%s, %s, %s, %s)"
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    values = (date, product, destination, quantity)
    try:
        cursor.execute(query, values)
        connection.commit()
        print("New row inserted successfully.")
    except mysql.connector.Error as error:
        print("Error inserting row:", error)
    finally:
        cursor.close()
        connection.close()
        fetch_data_delivery()

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    return Response("Data inserted successfully.", headers=headers)

@app.route('/add/products', methods=['POST'])
def insert_row_products():

    product_number = request.json.get('productNumber')
    product_name = request.json.get('productName')
    product_price = request.json.get('price')

    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="AgueroAguero123!",
        database="exsitec"
    )
    cursor = connection.cursor()
    query = "INSERT INTO Products (ProductNumber, Name, Price) VALUES (%s, %s, %s)"
    values = (product_number, product_name, product_price)
    try:
        cursor.execute(query, values)
        connection.commit()
        print("New row inserted successfully.")
    except mysql.connector.Error as error:
        print("Error inserting row:", error)
    finally:
        cursor.close()
        connection.close()
        fetch_data_delivery()

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    return Response("Data inserted successfully.", headers=headers)

@app.route('/add/inventory', methods=['POST'])
def insert_row_inventory():

    inventory_number = request.json.get('inventoryNumber')
    city = request.json.get('city')

    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="AgueroAguero123!",
        database="exsitec"
    )
    cursor = connection.cursor()
    query = "INSERT INTO Inventory (InventoryNumber, City) VALUES (%s, %s)"
    values = (inventory_number, city)
    try:
        cursor.execute(query, values)
        connection.commit()
        print("New row inserted successfully.")
    except mysql.connector.Error as error:
        print("Error inserting row:", error)
    finally:
        cursor.close()
        connection.close()
        fetch_data_delivery()

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    return Response("Data inserted successfully.", headers=headers)

def delete_row_products(productnumber):
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="AgueroAguero123!",
        database="exsitec"
    )
    cursor = connection.cursor()
    query = "DELETE FROM Products WHERE ID = %s"
    values = (productnumber,)
    try:
        cursor.execute(query, values)
        connection.commit()
        print("Row deleted successfully.")
    except mysql.connector.Error as error:
        print("Error deleting row:", error)
    finally:
        cursor.close()
        connection.close()


def delete_row_inventory(productnumber):
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="AgueroAguero123!",
        database="exsitec"
    )
    cursor = connection.cursor()
    query = "DELETE FROM Inventory WHERE ID = %s"
    values = (productnumber,)
    try:
        cursor.execute(query, values)
        connection.commit()
        print("Row deleted successfully.")
    except mysql.connector.Error as error:
        print("Error deleting row:", error)
    finally:
        cursor.close()
        connection.close()
    
def delete_row_delivery(productnumber):
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="AgueroAguero123!",
        database="exsitec"
    )
    cursor = connection.cursor()
    query = "DELETE FROM Delivery WHERE ID = %s"
    values = (productnumber,)
    try:
        cursor.execute(query, values)
        connection.commit()
        print("Row deleted successfully.")
    except mysql.connector.Error as error:
        print("Error deleting row:", error)
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=8000, debug=False)
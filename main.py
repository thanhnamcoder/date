import sqlite3
from flask import Flask, request, jsonify, send_file
import pandas as pd
import json

app = Flask(__name__)

def add_data_to_database(data):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (barcode, productname, expiration_date, product_quantity) VALUES (?, ?, ?, ?)",
                   (data['barcode'], data['productName'], data['expirationDate'], data['productQuantity']))
    conn.commit()
    conn.close()


@app.route('/receive_data', methods=['POST'])
def receive_data():

    
    # Nhận dữ liệu JSON từ yêu cầu POST
    data = request.json
    add_data_to_database(data)
    print(data)
    # Trả về thông báo
    return jsonify({"message": "Data received and saved successfully!"})

from flask import jsonify

from flask import jsonify, abort

@app.route('/export_data', methods=['GET'])
def export_data():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()

    if len(products) == 0:
        # Trả về mã lỗi 404 và thông báo khi không có dữ liệu
        return jsonify({"error": "No data available"}), 404

    columns = ['ID', 'Barcode', 'ProductName', 'ProductQuantity', 'ExpirationDate']  

    df = pd.DataFrame(products, columns=columns) 

    df['ExpirationDate'] = pd.to_datetime(df['ExpirationDate'], format='%m/%Y')
    df['ExpirationDate'] = df['ExpirationDate'].dt.strftime('%m/%Y')

    pivot_df = df.pivot_table(
        values='ProductQuantity',
        index=['Barcode', 'ProductName'], 
        columns='ExpirationDate',
        aggfunc='first').reset_index()

    # Convert DataFrame to JSON format
    data_json = pivot_df.to_json(orient='records', force_ascii=False)

    return jsonify(json.loads(data_json))




# Function to delete all data from the database
def delete_all_data():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products")
    conn.commit()
    conn.close()

@app.route('/delete_all_data', methods=['POST']) 
def delete_all_data_route():
    try:
        delete_all_data()
        return '', 200 # 204 No Content
    except Exception as e:
        print(e)
        return jsonify({"error": "Failed to delete data"}), 500 # 500 Internal Server Error

def export_data_to_excel():
    # Kết nối vào cơ sở dữ liệu SQLite và truy vấn dữ liệu
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()

    if len(products) == 0:
        print("No data")
        return

    # Định nghĩa các cột trong dataframe
    columns = ['ID', 'Barcode', 'ProductName', 'ProductQuantity', 'ExpirationDate']

    # Tạo DataFrame từ kết quả truy vấn
    df = pd.DataFrame(products, columns=columns)

    # Chuyển đổi cột ngày hết hạn sang định dạng tháng/năm
    df['ExpirationDate'] = pd.to_datetime(df['ExpirationDate'], format='%m/%Y')
    df['ExpirationDate'] = df['ExpirationDate'].dt.strftime('%m/%Y')

    # Pivot dữ liệu theo Barcode, ProductName và ExpirationDate
    pivot_df = df.pivot_table(
        values='ProductQuantity',
        index=['Barcode','ProductName'], 
        columns='ExpirationDate',
        aggfunc='first').reset_index()

    # Ghi dataframe vào tệp Excel
    outfile = 'products.xlsx'
    pivot_df.to_excel(outfile, index=False)
    return outfile



@app.route('/export', methods=['GET'])
def export_and_send_file():
    outfile = export_data_to_excel()
    if outfile:
        return send_file(outfile, as_attachment=True)
    else:
        return 'No data to export'
if __name__ == '__main__':
    app.run(host='0.0.0.0')
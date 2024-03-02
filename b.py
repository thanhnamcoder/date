import sqlite3
from flask import Flask, request, jsonify
import pandas as pd

def export_data_to_excel():

    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()

    if len(products) == 0:
        print("No data")
        return

    columns = ['ID', 'Barcode', 'ProductName', 'ProductQuantity', 'ExpirationDate']  

    df = pd.DataFrame(products, columns=columns) 

    df['ExpirationDate'] = pd.to_datetime(df['ExpirationDate'])
    df['ExpirationDate'] = df['ExpirationDate'].dt.strftime('%m/%Y')

    pivot_df = df.pivot_table(
        values='ProductQuantity',
        index=['Barcode','ProductName'], 
        columns='ExpirationDate',
        aggfunc='first').reset_index()

    outfile = 'products.xlsx'
    # pivot_df.to_excel(outfile, index=False)
    print(pivot_df)

    print(f'Data exported to {outfile}')

# Gọi hàm để thực hiện việc xuất dữ liệu
export_data_to_excel()
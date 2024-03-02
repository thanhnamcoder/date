import sqlite3

def create_table():
    # Kết nối đến hoặc tạo một cơ sở dữ liệu SQLite mới
    conn = sqlite3.connect('products.db')

    # Tạo một đối tượng Cursor để thao tác với cơ sở dữ liệu
    cursor = conn.cursor()

    # Tạo bảng products
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY,
                        barcode TEXT,
                        productname TEXT,
                        product_quantity TEXT,
                        expiration_date TEXT
                      )''')

    # Lưu thay đổi và đóng kết nối
    conn.commit()
    conn.close()

def create_expiry_dates_table():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expiry_dates (
                        id INTEGER PRIMARY KEY,
                        expiry_date TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()

create_expiry_dates_table()
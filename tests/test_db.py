import pymysql

try:
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='todos'
    )
    print("✅ MySQL connection successful!")
    conn.close()
except Exception as e:
    print(f"❌ MySQL connection failed: {e}")
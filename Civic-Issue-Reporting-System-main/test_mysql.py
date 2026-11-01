import mysql.connector

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="civic_issues_db",
        port=3306
    )

    print("[SUCCESS] MySQL connected successfully!")
    db.close()

except mysql.connector.Error as err:
    print("[ERROR] MySQL connection failed:")
    print(err)
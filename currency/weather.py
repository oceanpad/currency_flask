import mysql.connector
conn = mysql.connector.connect(user='root', password='root', database='currency', use_unicode=True)
cursor = conn.cursor()

cursor.execute('select * from rates where currency_code = %s', (22,))
values = cursor.fetchall()

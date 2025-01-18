import sqlite3

conn = sqlite3.connect('news_data.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM news_table")
rows = cursor.fetchall()
print(rows)  # This will print all the rows in the news_table

conn.close()

import sqlite3

conn = sqlite3.connect("recipe.db")

cursor = conn.cursor()

cursor.execute("PRAGMA table_info(recipes)")

columns = cursor.fetchall()

for column in columns:
    print(column)

conn.close()
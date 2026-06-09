# add_notes_column.py
import sqlite3

conn = sqlite3.connect("recipe.db")

cursor = conn.cursor()

try:
    cursor.execute("""
        ALTER TABLE recipes
        ADD COLUMN notes TEXT
    """)

    conn.commit()

    print("Notes column added successfully!")

except Exception as e:
    print("Error:", e)

finally:
    conn.close()
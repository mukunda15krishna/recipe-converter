import sqlite3

conn = sqlite3.connect("recipe.db")

cursor = conn.cursor()

cursor.execute(
    """
    ALTER TABLE note_requests
    ADD COLUMN submitted_by TEXT
    """
)

conn.commit()

conn.close()

print("submitted_by column added successfully")
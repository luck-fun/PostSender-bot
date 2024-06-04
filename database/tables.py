import sqlite3

db = sqlite3.connect('db')
cursor = db.cursor()

tables = """
    CREATE TABLE IF NOT EXISTS main_table(
        user_id INTEGER PRIMARY KEY,
        user_name TEXT, 
        channel_id INTEGER
    )
"""
cursor.executescript(tables)


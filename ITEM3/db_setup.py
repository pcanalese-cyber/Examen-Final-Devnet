import sqlite3

DB_NAME = "usuarios.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);
""")

conn.commit()
conn.close()

print(f"Base de datos '{DB_NAME}' creada correctamente con tabla usuarios.")

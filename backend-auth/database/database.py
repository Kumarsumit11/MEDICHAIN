import sqlite3

DATABASE_NAME = "medisecure.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users table only
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        phone TEXT UNIQUE NOT NULL,
        emergency_contact TEXT NOT NULL,
        address TEXT NOT NULL,
        allergies TEXT,
        chronic_diseases TEXT,
        blood_type TEXT,
        date_of_birth TEXT,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully")
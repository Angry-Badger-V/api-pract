# seed nc_plus_one db
import json
import db.connection

def drop_users(cursor):
    cursor.execute(
        "DROP TABLE IF EXISTS users CASCADE;")

def create_users(cursor):
    cursor.execute("""
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        );
        """)

def read_users_data():
    pass

def bulk_insert_users():
    pass

def seed_users(cursor):
    # drop users if it exists
    # create users table
    # read user data
    # bulk insert user data
    drop_users(cursor)
    create_users(cursor)

def seed():
    conn = db.connection.get_connection()
    cursor = conn.cursor()
    seed_users(cursor)
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    seed()

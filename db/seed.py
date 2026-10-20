# seed nc_plus_one db
import json
import db.connection
from psycopg2.extras import execute_values
from src.seed.users import email_normalisation, name_normalisation, password_hashing

def read_data(filepath):
    with open(filepath, "r") as file:
        data = json.load(file)
    return data

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

def bulk_normalise_users(users):
    result = []
    for user in users:
        result.append({
            "name": name_normalisation(user),
            "email": email_normalisation(user),
            "password": password_hashing(user)
        })
    return result

def bulk_insert_users(cursor, users):
    user_values = []

    for user in users:
        user_values.append((
            user["email"],
            user["password"],
            user["name"]
        ))

    execute_values(
            cursor,
            """
            INSERT INTO users (email, password, name)
            VAKUES %s;
            """,
            user_values
    )

def seed_users(cursor):
    # drop users if it exists
    # create users table
    # read user data
    # bulk insert user data
    drop_users(cursor)
    create_users(cursor)
    user_data = read_data("data/users.json")
    bulk_normalise_users(user_data)
    bulk_insert_users(cursor, user_data)

def seed():
    conn = db.connection.get_connection()
    cursor = conn.cursor()
    seed_users(cursor)
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    seed()

# seed nc_plus_one db
import json
import db.connection
from psycopg2 import sql
from psycopg2.extras import execute_values
from src.seed.users import email_normalisation, name_normalisation, password_hashing

def read_data(filepath):
    with open(filepath, "r") as file:
        data = json.load(file)
    return data


def drop_table(cursor, table_name):
    query = sql.SQL(
        "DROP TABLE IF EXISTS {} CASCADE;"
    ).format(
        sql.Identifier(table_name)
    )
    cursor.execute(query)


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

def create_venues(cursor):
    cursor.execute("""
        CREATE TABLE venues (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            address TEXT,
            capacity INT
        );
        """)

def bulk_normalise_users(users):
    result = []
    for user in users:
        result.append({
            "name": name_normalisation(user)["name"],
            "email": email_normalisation(user)["email"],
            "password": password_hashing(user)["password"]
        })
    return result

def bulk_insert(cursor, table_name, data):
    if not data:
        return

    columns = list(data[0].keys())

    values = [
        tuple(row[column] for column in columns)
        for row in data
    ]

    query = sql.SQL("""
        INSERT INTO {} ({})
        VALUES %s
    """).format(
        sql.Identifier(table_name),
        sql.SQL(", ").join(
            sql.Identifier(column) for column in columns
        )
    )

    execute_values(cursor, query.as_string(cursor), values)
def seed_users(cursor):
    # drop users if it exists
    # create users table
    # read user data
    # bulk insert user data
    drop_table(cursor, "users")#drop_users(cursor)
    create_users(cursor)
    user_data = read_data("db/data/users.json")
    user_data = bulk_normalise_users(user_data)
    bulk_insert(cursor, "users", user_data)

def seed_values(cursor):
    # drop venues if it exists
    # create venues table
    # read venue data
    # bul insert venue data
    drop_table(cursor, "venues")
    create_venues(cursor)
    venue_data = read_data("db/data/venues.json")
    #venue_data = bulk_normalise_venues(venue_data)
    bulk_insert(cursor, "venues", venue_data)

def seed():
    conn = db.connection.get_connection()
    cursor = conn.cursor()
    seed_users(cursor)
    seed_values(cursor)
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    seed()

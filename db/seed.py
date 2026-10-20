# seed nc_plus_one db
import json

from _pytest.subtests import capturing_logs
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

def drop_tables(cursor):
    drop_table(cursor, "events")
    drop_table(cursor, "venues")
    drop_table(cursor, "users")

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

def create_events(cursor):
    cursor.execute("""
        CREATE TABLE events (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description VARCHAR(255),
            starts_at TIMESTAMP NOT NULL,
            ends_at TIMESTAMP NOT NULL, 
            organiser_id INT REFERENCES users(id),
            venue_id INT REFERENCES venues(id),
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)

def bulk_normalise_users(users):
    result = []
    for user in users:
        user = user.copy()

        name_normalisation(user)
        email_normalisation(user)
        password_hashing(user)        
        
        result.append(user)
    return result

def bulk_insert(cursor, table_name, data):
    if not data:
        return

    columns = list(data[0].keys())

    values = [
        tuple(row.get(column) for column in columns)
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
    #drop_table(cursor, "users")#drop_users(cursor)
    create_users(cursor)
    user_data = read_data("db/data/users.json")
    user_data = bulk_normalise_users(user_data)
    bulk_insert(cursor, "users", user_data)

def seed_venues(cursor):
    # drop venues if it exists
    # create venues table
    # read venue data
    # bul insert venue data
    #drop_table(cursor, "venues")
    create_venues(cursor)
    venue_data = read_data("db/data/venues.json")
    #venue_data = bulk_normalise_venues(venue_data)
    bulk_insert(cursor, "venues", venue_data)

def seed_events(cursor):
    #drop_table(cursor, "events")
    create_events(cursor)
    event_data = read_data("db/data/events.json")
    bulk_insert(cursor, "events", event_data)

def seed():
    conn = db.connection.get_connection()
    cursor = conn.cursor()
    drop_tables(cursor)
    seed_users(cursor)
    seed_venues(cursor)
    seed_events(cursor)
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    seed()

import psycopg2
import config


def connect():
    # create a connection to the database and return it
    conn = psycopg2.connect(
        host=config.host,
        port=config.port,
        database=config.database,
        user=config.user,
        password=config.password
    )
    return conn


# run this file to check that the connection works
if __name__ == "__main__":
    try:
        conn = connect()
        print("Connected to PostgreSQL!")
        conn.close()
    except Exception as error:
        print("Connection failed:", error)
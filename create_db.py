import mysql.connector
from mysql.connector import Error
from pathlib import Path

DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
}

SCHEMA_FILE = Path(__file__).with_name('schema.sql')


def create_database():
    print('Connecting to XAMPP MySQL...')
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        with SCHEMA_FILE.open('r', encoding='utf-8') as f:
            sql = f.read()
            for result in cursor.execute(sql, multi=True):
                pass

        connection.commit()
        print('Database created successfully.')
    except Error as e:
        print(f'Error: {e}')
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


if __name__ == '__main__':
    create_database()

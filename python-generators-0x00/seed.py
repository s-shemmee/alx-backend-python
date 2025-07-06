#!/usr/bin/python3
import mysql.connector
import csv
import uuid

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="yourpassword"
    )

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    cursor.close()

def connect_to_prodev():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="yourpassword",
        database="ALX_prodev"
    )

def create_table(connection):
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL
    );
    """
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()
    print("Table user_data created successfully")

def insert_data(connection, filename):
    cursor = connection.cursor()
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user_id = str(uuid.uuid4())
            cursor.execute(
                """
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
                """,
                (user_id, row["name"], row["email"], row["age"])
            )
    connection.commit()
    cursor.close()

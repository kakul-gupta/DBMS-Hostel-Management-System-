import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kakul@2006",   # change this
        database="hostel_db"
    )
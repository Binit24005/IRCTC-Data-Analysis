import os
import pandas as pd
import mysql.connector
from mysql.connector import Error

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, '..', 'data', 'cleaned_uts_data.csv')

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOUR_PASSWORD_HERE',  # Update with your MySQL password
}

def setup_and_insert():
    conn = None
    try:
        print("Connecting to MySQL...")
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS irctc_uts_db;")
        cursor.execute("USE irctc_uts_db;")
        cursor.execute("DROP TABLE IF EXISTS uts_bookings;")

        create_table_sql = """
        CREATE TABLE uts_bookings (
            Booking_ID INT PRIMARY KEY,
            Date DATE,
            Month INT,
            Week INT,
            Time TIME,
            Ticket_Type VARCHAR(50),
            Booking_Mode VARCHAR(50),
            From_Station VARCHAR(100),
            To_Station VARCHAR(100),
            Passengers INT,
            Total_Fare DECIMAL(10, 2),
            Payment_Type VARCHAR(50),
            Railway_Line VARCHAR(50),
            City VARCHAR(50),
            Day_Name VARCHAR(15),
            Is_Weekend TINYINT,
            Hour INT,
            Fare_Per_Passenger DECIMAL(10, 2)
        );
        """
        cursor.execute(create_table_sql)
        print("Table 'uts_bookings' created.")

        df = pd.read_csv(CSV_PATH)
        df = df.where(pd.notnull(df), None)

        insert_sql = """
        INSERT INTO uts_bookings (
            Booking_ID, Date, Month, Week, Time, Ticket_Type, Booking_Mode,
            From_Station, To_Station, Passengers, Total_Fare, Payment_Type,
            Railway_Line, City, Day_Name, Is_Weekend, Hour, Fare_Per_Passenger
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        records = [tuple(row) for row in df.itertuples(index=False, name=None)]
        total = len(records)
        chunk_size = 5000

        print(f"Uploading {total} records in batches...")
        for i in range(0, total, chunk_size):
            cursor.executemany(insert_sql, records[i:i + chunk_size])
            conn.commit()
            print(f"Uploaded {min(i + chunk_size, total)} / {total}")

        print("MySQL ingestion complete.")

    except Error as e:
        print(f"MySQL Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    setup_and_insert()
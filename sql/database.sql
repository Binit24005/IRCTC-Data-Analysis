CREATE DATABASE IF NOT EXISTS irctc_uts_db;
USE irctc_uts_db;

DROP TABLE IF EXISTS uts_bookings;

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
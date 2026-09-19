USE irctc_uts_db;

-- 1. Total Volume & Overall Revenue
SELECT 
    COUNT(*) AS total_bookings,
    SUM(Passengers) AS total_passengers,
    SUM(Total_Fare) AS total_revenue_inr,
    ROUND(AVG(Fare_Per_Passenger), 2) AS avg_fare_per_passenger
FROM uts_bookings;

-- 2. Peak Travel Hours
SELECT 
    Hour,
    COUNT(*) AS booking_count,
    SUM(Passengers) AS total_passengers
FROM uts_bookings
GROUP BY Hour
ORDER BY booking_count DESC;

-- 3. Top 10 Busiest Commuter Routes
SELECT 
    From_Station,
    To_Station,
    COUNT(*) AS route_trips,
    SUM(Total_Fare) AS route_revenue
FROM uts_bookings
GROUP BY From_Station, To_Station
ORDER BY route_trips DESC
LIMIT 10;

-- 4. Revenue and Traffic by Railway Line
SELECT 
    Railway_Line,
    COUNT(*) AS bookings,
    SUM(Passengers) AS passengers,
    SUM(Total_Fare) AS revenue,
    ROUND(AVG(Fare_Per_Passenger), 2) AS avg_fare
FROM uts_bookings
GROUP BY Railway_Line
ORDER BY bookings DESC;

-- 5. Booking Mode Adoption (Paper vs Paperless)
SELECT 
    Booking_Mode,
    Payment_Type,
    COUNT(*) AS total_transactions,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM uts_bookings), 2) AS pct_share
FROM uts_bookings
GROUP BY Booking_Mode, Payment_Type
ORDER BY total_transactions DESC;
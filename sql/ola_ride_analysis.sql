
USE Ola_Ride_Insights;
GO

/*
PROJECT: OLA RIDE INSIGHTS
SECTION: SQL BUSINESS ANALYSIS
TABLE: dbo.ola_bookings_staging
*/

-- Q1. Retrieve all successful bookings

SELECT *
FROM dbo.ola_bookings_staging
WHERE Booking_Status = 'Success';
GO


-- Q2. Find the average ride distance for each vehicle type

SELECT
    Vehicle_Type,
    ROUND(AVG(CAST(Ride_Distance AS FLOAT)), 2) AS Average_Ride_Distance
FROM dbo.ola_bookings_staging
WHERE Booking_Status = 'Success'
GROUP BY Vehicle_Type
ORDER BY Average_Ride_Distance DESC;
GO


-- Q3. Count the total number of rides cancelled by customers

SELECT
    COUNT(*) AS Total_Customer_Cancelled_Rides
FROM dbo.ola_bookings_staging
WHERE Booking_Status = 'Canceled by Customer';
GO


-- Q4. Top 5 customers by number of rides

SELECT TOP 5
    Customer_ID,
    COUNT(Booking_ID) AS Total_Rides
FROM dbo.ola_bookings_staging
GROUP BY Customer_ID
ORDER BY Total_Rides DESC;
GO


-- Q5. Driver cancellations due to personal or car-related issues

SELECT
    COUNT(*) AS Total_Driver_Cancellations
FROM dbo.ola_bookings_staging
WHERE Booking_Status = 'Canceled by Driver'
AND Canceled_Rides_by_Driver = 'Personal & Car related issue';
GO


-- Q6. Maximum and minimum driver ratings for Prime Sedan

SELECT
    Vehicle_Type,
    MAX(Driver_Ratings) AS Maximum_Driver_Rating,
    MIN(Driver_Ratings) AS Minimum_Driver_Rating
FROM dbo.ola_bookings_staging
WHERE Vehicle_Type = 'Prime Sedan'
AND Booking_Status = 'Success'
GROUP BY Vehicle_Type;
GO


-- Q7. Successful rides paid using UPI

SELECT
    COUNT(*) AS Total_UPI_Rides
FROM dbo.ola_bookings_staging
WHERE Payment_Method = 'UPI'
AND Booking_Status = 'Success';
GO


-- Q8. Average customer rating per vehicle type

SELECT
    Vehicle_Type,
    ROUND(AVG(Customer_Rating), 2) AS Average_Customer_Rating
FROM dbo.ola_bookings_staging
WHERE Booking_Status = 'Success'
GROUP BY Vehicle_Type
ORDER BY Average_Customer_Rating DESC;
GO


-- Q9. Total booking value of successful rides

SELECT
    SUM(Booking_Value) AS Total_Successful_Booking_Value
FROM dbo.ola_bookings_staging
WHERE Booking_Status = 'Success';
GO


-- Q10. Incomplete rides and their reasons

SELECT
    Incomplete_Rides_Reason,
    COUNT(*) AS Total_Incomplete_Rides
FROM dbo.ola_bookings_staging
WHERE Incomplete_Rides = 'Yes'
GROUP BY Incomplete_Rides_Reason
ORDER BY Total_Incomplete_Rides DESC;
GO



-- Additional business insights
-- Q11. Booking status distribution and percentages

SELECT
    Booking_Status,
    COUNT(*) AS Total_Bookings,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM dbo.ola_bookings_staging),
        2
    ) AS Booking_Percentage
FROM dbo.ola_bookings_staging
GROUP BY Booking_Status
ORDER BY Total_Bookings DESC;
GO


-- Q12. Revenue by vehicle type

SELECT
    Vehicle_Type,
    COUNT(*) AS Total_Successful_Rides,
    SUM(Booking_Value) AS Total_Revenue,
    ROUND(AVG(CAST(Booking_Value AS FLOAT)), 2) AS Average_Booking_Value
FROM dbo.ola_bookings_staging
WHERE Booking_Status = 'Success'
GROUP BY Vehicle_Type
ORDER BY Total_Revenue DESC;
GO


-- Q13. Hourly booking demand

SELECT
    Booking_Hour,
    COUNT(*) AS Total_Bookings
FROM dbo.ola_bookings_staging
GROUP BY Booking_Hour
ORDER BY Total_Bookings DESC;
GO



-- Q14. Top 10 pickup locations

SELECT TOP 10
    Pickup_Location,
    COUNT(*) AS Total_Bookings
FROM dbo.ola_bookings_staging
GROUP BY Pickup_Location
ORDER BY Total_Bookings DESC;
GO



-- Q15. Revenue by payment method

SELECT
    Payment_Method,
    COUNT(*) AS Total_Rides,
    SUM(Booking_Value) AS Total_Revenue
FROM dbo.ola_bookings_staging
WHERE Booking_Status = 'Success'
GROUP BY Payment_Method
ORDER BY Total_Revenue DESC;
GO


-- Q16. Average ride distance by time category

SELECT
    Ride_Time_Category,
    COUNT(*) AS Total_Successful_Rides,
    ROUND(AVG(CAST(Ride_Distance AS FLOAT)), 2) AS Average_Ride_Distance
FROM dbo.ola_bookings_staging
WHERE Booking_Status = 'Success'
GROUP BY Ride_Time_Category
ORDER BY Average_Ride_Distance DESC;
GO


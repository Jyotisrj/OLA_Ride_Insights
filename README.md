# 🚕 Ola Ride Insights

### Ride-Sharing & Mobility Analytics

## 📌 Project Overview

Ola Ride Insights is a data analytics and business intelligence project focused on analyzing ride-booking data from a ride-sharing platform.

The project explores booking trends, vehicle performance, customer behavior, cancellations, revenue, payment preferences, and customer and driver ratings.

It uses SQL Server, Python, Power BI, and Streamlit to transform raw ride-booking data into meaningful business insights and interactive visualizations.

## 🎯 Project Objectives

- Analyze ride-booking trends and booking status.
- Identify successful and unsuccessful bookings.
- Understand customer and driver cancellation patterns.
- Evaluate vehicle-type performance.
- Analyze revenue and payment preferences.
- Study customer and driver ratings.
- Develop interactive dashboards and a web application.
- Provide data-driven business recommendations.

## 🏢 Domain

Ride-Sharing & Mobility Analytics

## 🛠️ Technologies Used

- **Python:** Data cleaning, preprocessing, and exploratory data analysis.
- **Pandas & NumPy:** Data manipulation and analysis.
- **Matplotlib & Seaborn:** Data visualization.
- **SQL Server:** Database management and SQL analysis.
- **Power BI:** Interactive business intelligence dashboards.
- **Streamlit:** Interactive web application.
- **VS Code:** Development environment.

## 📂 Dataset Description

The project uses an Ola ride-booking dataset containing **103,024 booking records** from July 2024.

### Dataset Details

| Attribute | Description |
|---|---|
| Total Records | 103,024 |
| Time Period | July 1–31, 2024 |
| Unique Customers | 94,544 |
| Vehicle Types | 7 |
| Pickup Locations | 50 |
| Drop Locations | 50 |
| Original Columns | 20 |

### Important Dataset Columns

- `Date` and `Time` – Booking date and time.
- `Booking_ID` – Unique booking identifier.
- `Booking_Status` – Status of each booking.
- `Customer_ID` – Customer identifier.
- `Vehicle_Type` – Type of vehicle booked.
- `Pickup_Location` and `Drop_Location` – Ride locations.
- `Booking_Value` – Booking amount.
- `Payment_Method` – Payment method used.
- `Ride_Distance` – Distance travelled.
- `Driver_Ratings` – Driver rating.
- `Customer_Rating` – Customer rating.
- `Incomplete_Rides_Reason` – Reason for incomplete rides.

## ⚙️ Project Methodology

### 1. Data Understanding

- Loaded and explored the original Excel dataset.
- Examined dataset dimensions, column names, and data types.
- Analyzed missing values and duplicate records.
- Studied numerical and categorical variables.

### 2. Data Cleaning and Preprocessing

- Removed the unnecessary Vehicle Images column.
- Standardized column names.
- Converted Date and Time into appropriate formats.
- Created additional time-based features:
  - Booking Hour
  - Booking Day
  - Day Name
  - Booking Month
  - Ride Time Category
- Checked invalid ratings and negative values.
- Saved the cleaned dataset as a CSV file.

### 3. Exploratory Data Analysis (EDA)

- Analyzed booking status and success rate.
- Studied vehicle-wise booking distribution.
- Examined daily and hourly booking trends.
- Analyzed revenue and payment methods.
- Investigated customer and driver cancellation reasons.
- Evaluated customer and driver ratings.
- Examined incomplete rides and their reasons.

### 4. SQL Analysis

Used Microsoft SQL Server to answer 10 business questions related to:

- Successful bookings.
- Average ride distance by vehicle type.
- Customer cancellations.
- Top 5 customers by ride count.
- Driver cancellations.
- Prime Sedan driver ratings.
- UPI payments.
- Average customer ratings by vehicle type.
- Revenue from successful bookings.
- Incomplete rides and their reasons.

### 5. Power BI Dashboard

Developed five interactive dashboard pages:

1. Overall Dashboard
2. Vehicle Type Analysis
3. Revenue Analysis
4. Cancellation Analysis
5. Ratings Analysis

### 6. Streamlit Application

Developed a Streamlit application with nine sections:

1. Overall Dashboard
2. Vehicle Analysis
3. Revenue Analysis
4. Cancellation Analysis
5. Ratings Analysis
6. Booking Data
7. SQL Analysis
8. Business Insights
9. Power BI Dashboard

## 📊 Key Project Findings

The analysis of 103,024 Ola ride bookings revealed the following findings:

### 1. Booking Performance

- Total Bookings: **103,024**
- Successful Bookings: **63,967**
- Successful Booking Rate: **62.09%**
- Unsuccessful Bookings: **39,057**

### 2. Cancellation Analysis

- Customer Cancellations: **10,499**
- Driver Cancellations: **18,434**
- Driver Not Found: **10,124**
- Total Customer and Driver Cancellations: **28,933**

Driver cancellations were higher than customer cancellations.

### 3. Revenue Analysis

- Total Revenue from Successful Rides: **₹35,080,467**
- Average Successful Booking Value: **₹548.42**

### 4. Incomplete Rides

- Total Incomplete Rides: **3,926**
- Customer Demand: **1,601**
- Vehicle Breakdown: **1,591**
- Other Issues: **734**

### 5. Ratings Analysis

- Average Driver Rating: Approximately **4 out of 5**
- Average Customer Rating: Approximately **4 out of 5**

## 💡 Business Recommendations

Based on the analysis, the following recommendations can help improve ride-sharing operations:

1. **Improve Driver Availability:** Investigate driver cancellation patterns and improve driver allocation.
2. **Optimize Vehicle Allocation:** Use vehicle-wise booking trends to plan vehicle availability.
3. **Improve Customer Experience:** Analyze customer feedback and cancellation reasons to improve service quality.
4. **Improve Vehicle Reliability:** Monitor vehicle breakdowns and encourage regular maintenance.
5. **Optimize Peak-Hour Operations:** Use hourly booking trends to allocate drivers during high-demand periods.
6. **Monitor Revenue Performance:** Analyze payment preferences and booking values to support revenue planning.

## 📈 Project Outcomes

- Developed a complete data analytics workflow.
- Performed data cleaning and exploratory analysis using Python.
- Answered business questions using SQL Server.
- Created five Power BI dashboard pages.
- Built a nine-section Streamlit application.
- Generated business insights and recommendations from ride-booking data.

## 👩‍💻 Author

**Project:** Ola Ride Insights

**Domain:** Ride-Sharing & Mobility Analytics

**Tools:** Python, SQL Server, Power BI, Streamlit


## 🚀 Installation and Setup

Follow these steps to run the Ola Ride Insights project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/Jyotisrj/OLA_Ride_Insights.git
```

### 2. Navigate to the Project Folder

```bash
cd Ola_Ride_Insights
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

For Windows:

```bash
.venv\Scripts\activate
```

### 5. Install Required Libraries

```bash
pip install -r requirements.txt
```

### 6. Run the Streamlit Application

```bash
streamlit run app.py
```

The application will open in your default web browser.

### 7. Power BI Dashboard

The Power BI dashboard is available in the `power bi` folder.

Open `Ola_Ride_Insights_Dashboard.pbix` using Microsoft Power BI Desktop to explore the interactive report.

### 8. SQL Server Setup

The SQL Analysis section uses Microsoft SQL Server.

To run SQL queries, configure your SQL Server connection and ensure that the `ola_bookings_staging` table is available in your database.

## 📁 Project Structure

```text
Ola_Ride_Insights/
│
├── app.py
├── README.md
├── requirements.txt
│
├── data/
│   ├── ola_rides_raw.xlsx
│   └── ola_rides_cleaned.csv
│
├── notebooks/
│   ├── 02_Data_Cleaning.ipynb
│   └── 03_EDA.ipynb
│
├── eda_charts/
│
├── power bi/
│   ├── Ola_Ride_Insights_Dashboard.pbix
│   └── screenshots/
│
└── sql/
```


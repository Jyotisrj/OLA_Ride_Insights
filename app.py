
import streamlit as st
import pandas as pd
from pathlib import Path
try:
    import pyodbc
except ImportError:
    pyodbc = None

# --------------------------------
# 1. Page Configuration
# --------------------------------

st.set_page_config(
    page_title="Ola Ride Insights",
    page_icon="🚕",
    layout="wide"
)

# --------------------------------
# 2. Load Dataset
# --------------------------------

PROJECT_DIR = Path(__file__).resolve().parent
DATA_PATH = PROJECT_DIR / "data" / "ola_rides_cleaned.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df


try:
    df = load_data()

except FileNotFoundError:
    st.error("Dataset not found. Please check your data folder.")
    st.stop()

# --------------------------------
# SQL Server Connection
# --------------------------------

SQL_SERVER = r"DESKTOP-AK57STV\SQLEXPRESS"
SQL_DATABASE = "Ola_Ride_Insights"

def get_sql_connection():

    connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={SQL_SERVER};"
        f"DATABASE={SQL_DATABASE};"
        "Trusted_Connection=yes;"
    )

    return pyodbc.connect(connection_string)


# --------------------------------
# 3. Application Title
# --------------------------------

st.title("🚕 Ola Ride Insights")
st.subheader("Ride-Sharing & Mobility Analytics")
st.caption("Data Analysis Report | July 2024")

st.divider()


# --------------------------------
# 4. Sidebar Navigation
# --------------------------------

st.sidebar.title("OLA INSIGHTS")
st.sidebar.caption("Ride Analytics")

page = st.sidebar.radio(
    "Navigation",
    [
        "Overall Dashboard",
        "Vehicle Analysis",
        "Revenue Analysis",
        "Cancellation Analysis",
        "Ratings Analysis",
        "Booking Data",
        "SQL Analysis",
        "Business Insights",
        "Power BI Dashboard"
    ],
    key="ola_main_navigation"
)


# --------------------------------
# 5. Overall Dashboard
# --------------------------------

if page == "Overall Dashboard":

    st.header("Overall Performance")

    total_bookings = len(df)

    successful_bookings = (
        df["Booking_Status"] == "Success"
    ).sum()

    total_revenue = df.loc[
        df["Booking_Status"] == "Success",
        "Booking_Value"
    ].sum()

    success_rate = successful_bookings / total_bookings * 100

    cancelled_bookings = df["Booking_Status"].isin(
        ["Canceled by Customer", "Canceled by Driver"]
    ).sum()

    cancellation_rate = cancelled_bookings / total_bookings * 100

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Total Bookings", f"{total_bookings:,}")
    col2.metric("Successful Rides", f"{successful_bookings:,}")
    col3.metric("Total Revenue", f"₹{total_revenue:,.0f}")
    col4.metric("Success Rate", f"{success_rate:.2f}%")
    col5.metric("Cancellation Rate", f"{cancellation_rate:.2f}%")

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Booking Status Distribution")

        status_counts = df["Booking_Status"].value_counts()

        st.bar_chart(status_counts)

    with right:
        st.subheader("Daily Booking Trend")

        daily_bookings = (
            df.groupby("Date")
            .size()
            .sort_index()
        )

        st.line_chart(daily_bookings)

    st.divider()

    st.subheader("Dataset Preview")

    st.dataframe(df.head(10), use_container_width=True)

    st.caption(f"Total records: {len(df):,}")


# --------------------------------
# 6. Vehicle Analysis
# --------------------------------

elif page == "Vehicle Analysis":

    st.header("🚘 Vehicle Type Analysis")

    successful_df = df[df["Booking_Status"] == "Success"].copy()

    vehicle_bookings = (
        df.groupby("Vehicle_Type")
        .size()
        .sort_values(ascending=False)
    )

    vehicle_revenue = (
        successful_df.groupby("Vehicle_Type")["Booking_Value"]
        .sum()
        .sort_values(ascending=False)
    )

    avg_distance = (
        successful_df.groupby("Vehicle_Type")["Ride_Distance"]
        .mean()
        .round(2)
    )

    avg_rating = (
        successful_df.groupby("Vehicle_Type")["Customer_Rating"]
        .mean()
        .round(2)
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Vehicle Types", df["Vehicle_Type"].nunique())
    col2.metric("Total Vehicle Bookings", f"{len(df):,}")
    col3.metric(
        "Average Ride Distance",
        f"{successful_df['Ride_Distance'].mean():.2f} km"
    )

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Bookings by Vehicle Type")
        st.bar_chart(vehicle_bookings)

    with right:
        st.subheader("Revenue by Vehicle Type")
        st.bar_chart(vehicle_revenue)

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Average Ride Distance by Vehicle")
        st.bar_chart(avg_distance)

    with right:
        st.subheader("Average Customer Rating by Vehicle")
        st.bar_chart(avg_rating)

    st.divider()

    st.subheader("Vehicle Performance Summary")

    vehicle_summary = pd.DataFrame({
        "Total Bookings": vehicle_bookings,
        "Total Revenue": vehicle_revenue,
        "Average Ride Distance": avg_distance,
        "Average Customer Rating": avg_rating
    }).fillna(0)

    st.dataframe(vehicle_summary, use_container_width=True)


# --------------------------------
# 7. Revenue Analysis
# --------------------------------

elif page == "Revenue Analysis":

    st.header("💰 Revenue Analysis")

    successful_df = df[df["Booking_Status"] == "Success"].copy()

    total_revenue = successful_df["Booking_Value"].sum()

    avg_booking_value = successful_df["Booking_Value"].mean()

    total_successful = len(successful_df)

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
    col2.metric("Average Booking Value", f"₹{avg_booking_value:,.2f}")
    col3.metric("Successful Bookings", f"{total_successful:,}")

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Revenue by Payment Method")

        payment_revenue = (
            successful_df.groupby("Payment_Method")["Booking_Value"]
            .sum()
            .sort_values(ascending=False)
        )

        st.bar_chart(payment_revenue)

    with right:
        st.subheader("Daily Revenue Trend")

        daily_revenue = (
            successful_df.groupby("Date")["Booking_Value"]
            .sum()
            .sort_index()
        )

        st.line_chart(daily_revenue)

    st.divider()

    st.subheader("Top 5 Customers by Booking Value")

    top_customers = (
        successful_df.groupby("Customer_ID")["Booking_Value"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )

    top_customers.columns = ["Customer ID", "Total Booking Value"]

    st.bar_chart(
        top_customers.set_index("Customer ID")
    )

    st.dataframe(top_customers, use_container_width=True)

    st.divider()

    st.subheader("Revenue by Vehicle Type")

    revenue_vehicle = (
        successful_df.groupby("Vehicle_Type")["Booking_Value"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(revenue_vehicle)


# --------------------------------
# 8. Cancellation Analysis
# --------------------------------

elif page == "Cancellation Analysis":

    st.header("❌ Cancellation Analysis")

    customer_cancelled = (
        df["Booking_Status"] == "Canceled by Customer"
    ).sum()

    driver_cancelled = (
        df["Booking_Status"] == "Canceled by Driver"
    ).sum()

    incomplete_rides = (
        df["Incomplete_Rides"].astype(str).str.strip().str.lower() == "yes"
    ).sum()

    total_cancelled = customer_cancelled + driver_cancelled

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Customer Cancellations", f"{customer_cancelled:,}")
    col2.metric("Driver Cancellations", f"{driver_cancelled:,}")
    col3.metric("Total Cancellations", f"{total_cancelled:,}")
    col4.metric("Incomplete Rides", f"{incomplete_rides:,}")

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Customer Cancellation Reasons")

        customer_reasons = (
            df["Canceled_Rides_by_Customer"]
            .dropna()
            .value_counts()
        )

        st.bar_chart(customer_reasons)

    with right:
        st.subheader("Driver Cancellation Reasons")

        driver_reasons = (
            df["Canceled_Rides_by_Driver"]
            .dropna()
            .value_counts()
        )

        st.bar_chart(driver_reasons)

    st.divider()

    st.subheader("Incomplete Ride Reasons")

    incomplete_reasons = (
        df["Incomplete_Rides_Reason"]
        .dropna()
        .value_counts()
    )

    st.bar_chart(incomplete_reasons)

    st.divider()

    st.subheader("Booking Status Summary")

    st.bar_chart(df["Booking_Status"].value_counts())


# --------------------------------
# 9. Ratings Analysis
# --------------------------------

elif page == "Ratings Analysis":

    st.header("⭐ Ratings Analysis")

    successful_df = df[df["Booking_Status"] == "Success"].copy()

    avg_driver_rating = successful_df["Driver_Ratings"].mean()

    avg_customer_rating = successful_df["Customer_Rating"].mean()

    rated_rides = successful_df["Driver_Ratings"].notna().sum()

    col1, col2, col3 = st.columns(3)

    col1.metric("Average Driver Rating", f"{avg_driver_rating:.2f} / 5")
    col2.metric("Average Customer Rating", f"{avg_customer_rating:.2f} / 5")
    col3.metric("Total Rated Rides", f"{rated_rides:,}")

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Driver Rating Distribution")

        driver_distribution = (
            successful_df["Driver_Ratings"]
            .dropna()
            .value_counts()
            .sort_index()
        )

        st.bar_chart(driver_distribution)

    with right:
        st.subheader("Customer Rating Distribution")

        customer_distribution = (
            successful_df["Customer_Rating"]
            .dropna()
            .value_counts()
            .sort_index()
        )

        st.bar_chart(customer_distribution)

    st.divider()

    st.subheader("Ratings by Vehicle Type")

    vehicle_ratings = (
        successful_df.groupby("Vehicle_Type")
        [["Driver_Ratings", "Customer_Rating"]]
        .mean()
        .round(2)
    )

    st.bar_chart(vehicle_ratings)

    st.dataframe(vehicle_ratings, use_container_width=True)

    st.divider()

     
    st.subheader("Driver Rating vs Customer Rating")

    rating_comparison = successful_df[
        ["Driver_Ratings", "Customer_Rating"]
    ].dropna().copy()

    # Count the number of rides for each rating
    driver_counts = (
        rating_comparison["Driver_Ratings"]
        .round()
        .astype(int)
        .value_counts()
    )

    customer_counts = (
        rating_comparison["Customer_Rating"]
        .round()
        .astype(int)
        .value_counts()
    )

    # Combine both rating counts
    rating_chart_data = pd.DataFrame({
        "Driver Rating": driver_counts,
        "Customer Rating": customer_counts
    }).fillna(0)

    rating_chart_data.index.name = "Rating"

    rating_chart_data = rating_chart_data.sort_index()

    # Display clustered column chart
    st.bar_chart(
        rating_chart_data,
        x_label="Rating",
        y_label="Number of Rides",
        color=["#2878B5", "#F39C35"]
    )

    st.caption(
        "Comparison of driver and customer ratings by rating category."
    )



# --------------------------------
# 10. Booking Data
# --------------------------------

elif page == "Booking Data":

    st.header("📋 Booking Data Explorer")

    st.write("Explore and filter Ola booking records.")

    filtered_df = df.copy()

    # Date Filter

    st.subheader("Filters")

    valid_dates = filtered_df["Date"].dropna()

    if not valid_dates.empty:

        date_col1, date_col2 = st.columns(2)

        with date_col1:
            start_date = st.date_input(
                "Start Date",
                value=valid_dates.min().date(),
                key="booking_start_date"
            )

        with date_col2:
            end_date = st.date_input(
                "End Date",
                value=valid_dates.max().date(),
                key="booking_end_date"
            )

        if start_date > end_date:
            st.warning("Start date cannot be after end date.")
            st.stop()

        filtered_df = filtered_df[
            (filtered_df["Date"].dt.date >= start_date) &
            (filtered_df["Date"].dt.date <= end_date)
        ]

    # Vehicle Filter

    selected_vehicles = st.multiselect(
        "Select Vehicle Type",
        options=sorted(df["Vehicle_Type"].dropna().unique()),
        default=sorted(df["Vehicle_Type"].dropna().unique()),
        key="booking_vehicle_filter"
    )

    filtered_df = filtered_df[
        filtered_df["Vehicle_Type"].isin(selected_vehicles)
    ]

    # Booking Status Filter

    selected_status = st.multiselect(
        "Select Booking Status",
        options=sorted(df["Booking_Status"].dropna().unique()),
        default=sorted(df["Booking_Status"].dropna().unique()),
        key="booking_status_filter"
    )

    filtered_df = filtered_df[
        filtered_df["Booking_Status"].isin(selected_status)
    ]

    # Search Booking ID

    search_booking = st.text_input(
        "Search Booking ID",
        key="booking_search"
    )

    if search_booking:
        filtered_df = filtered_df[
            filtered_df["Booking_ID"].astype(str)
            .str.contains(search_booking, case=False, na=False)
        ]

    st.divider()

    st.subheader("Filtered Booking Records")

    col1, col2 = st.columns(2)

    col1.metric("Filtered Records", f"{len(filtered_df):,}")
    col2.metric("Total Dataset Records", f"{len(df):,}")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=450
    )

    # CSV Download

    csv_data = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=csv_data,
        file_name="ola_filtered_bookings.csv",
        mime="text/csv",
        key="download_filtered_bookings"
    )

    st.caption("Use the filters above to explore specific booking records.")


# --------------------------------
# 11. SQL Analysis
# --------------------------------

elif page == "SQL Analysis":

    st.header("🗄️ SQL Analysis")
    st.write("Explore results from the 10 SQL business questions.")

    queries = {

        "1. Retrieve all successful bookings": """
            SELECT *
            FROM dbo.ola_bookings_staging
            WHERE Booking_Status = 'Success';
        """,

        "2. Average ride distance by vehicle type": """
            SELECT
                Vehicle_Type,
                AVG(CAST(Ride_Distance AS FLOAT)) AS Average_Ride_Distance
            FROM dbo.ola_bookings_staging
            WHERE Booking_Status = 'Success'
            GROUP BY Vehicle_Type
            ORDER BY Average_Ride_Distance DESC;
        """,

        "3. Total customer-cancelled rides": """
            SELECT COUNT(*) AS Total_Customer_Cancellations
            FROM dbo.ola_bookings_staging
            WHERE Booking_Status = 'Canceled by Customer';
        """,

        "4. Top 5 customers by number of rides": """
            SELECT TOP 5
                Customer_ID,
                COUNT(*) AS Total_Rides
            FROM dbo.ola_bookings_staging
            GROUP BY Customer_ID
            ORDER BY Total_Rides DESC;
        """,

        "5. Driver cancellations due to personal/car issues": """
            SELECT COUNT(*) AS Total_Cancellations
            FROM dbo.ola_bookings_staging
            WHERE Canceled_Rides_by_Driver =
                  'Personal & Car related issue';
        """,

        "6. Maximum and minimum Prime Sedan driver ratings": """
            SELECT
                MAX(Driver_Ratings) AS Maximum_Driver_Rating,
                MIN(Driver_Ratings) AS Minimum_Driver_Rating
            FROM dbo.ola_bookings_staging
            WHERE Vehicle_Type = 'Prime Sedan';
        """,

        "7. All rides paid using UPI": """
            SELECT *
            FROM dbo.ola_bookings_staging
            WHERE Payment_Method = 'UPI';
        """,

        "8. Average customer rating by vehicle type": """
            SELECT
                Vehicle_Type,
                AVG(CAST(Customer_Rating AS FLOAT))
                    AS Average_Customer_Rating
            FROM dbo.ola_bookings_staging
            GROUP BY Vehicle_Type
            ORDER BY Average_Customer_Rating DESC;
        """,

        "9. Total booking value of successful rides": """
            SELECT
                SUM(Booking_Value) AS Total_Successful_Booking_Value
            FROM dbo.ola_bookings_staging
            WHERE Booking_Status = 'Success';
        """,

        "10. Incomplete rides with their reasons": """
            SELECT
                Booking_ID,
                Vehicle_Type,
                Incomplete_Rides,
                Incomplete_Rides_Reason
            FROM dbo.ola_bookings_staging
            WHERE Incomplete_Rides = 'Yes';
        """
    }

    selected_query = st.selectbox(
        "Select SQL Business Question",
        list(queries.keys()),
        key="sql_query_selection"
    )

    st.subheader(selected_query)

    st.code(queries[selected_query], language="sql")

    if st.button("Run SQL Query", key="run_sql_query"):

        try:
            with st.spinner("Executing SQL query..."):

                connection = get_sql_connection()

                try:
                    result = pd.read_sql_query(
                        queries[selected_query],
                        connection
                    )
                finally:
                    connection.close()

            st.success("Query executed successfully!")

            st.metric("Rows Returned", f"{len(result):,}")

            st.dataframe(
                result,
                use_container_width=True
            )

            # Download query result

            csv_data = result.to_csv(index=False).encode("utf-8")

            st.download_button(
                "Download Query Result",
                data=csv_data,
                file_name="ola_sql_query_result.csv",
                mime="text/csv",
                key="download_sql_result"
            )

        except Exception as e:
            st.error(f"SQL execution failed: {e}")

        
    if pyodbc is None:
        st.warning("SQL Server connection is not available.")

        st.info(
            "The SQL Analysis feature requires a connection to "
            "the project's SQL Server database. This connection "
            "is available in the local development environment "
            "but has not been configured for cloud deployment."
        )

        st.stop()




# --------------------------------
# 12. Business Insights
# --------------------------------

elif page == "Business Insights":

    st.header("💡 Business Insights")
    st.write(
        "Key findings and recommendations based on Ola ride booking data."
    )

    st.divider()

    # 1. Booking Performance

    st.subheader("1. Booking Performance")

    total_bookings = len(df)

    successful_bookings = (
        df["Booking_Status"] == "Success"
    ).sum()

    success_rate = (
        successful_bookings / total_bookings * 100
    )

    unsuccessful_bookings = total_bookings - successful_bookings

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Bookings", f"{total_bookings:,}")
    col2.metric("Successful Bookings", f"{successful_bookings:,}")
    col3.metric("Success Rate", f"{success_rate:.2f}%")

    st.info(
        f"Out of {total_bookings:,} bookings, "
        f"{successful_bookings:,} were successful. "
        f"{unsuccessful_bookings:,} bookings were unsuccessful."
    )

    st.divider()

    # 2. Cancellation Analysis

    st.subheader("2. Cancellation Analysis")

    customer_cancelled = (
        df["Booking_Status"] == "Canceled by Customer"
    ).sum()

    driver_cancelled = (
        df["Booking_Status"] == "Canceled by Driver"
    ).sum()

    cancellation_data = pd.Series({
        "Customer Cancellations": customer_cancelled,
        "Driver Cancellations": driver_cancelled
    })

    st.bar_chart(cancellation_data)

    if driver_cancelled > customer_cancelled:
        st.warning(
            f"Driver cancellations ({driver_cancelled:,}) "
            f"are higher than customer cancellations "
            f"({customer_cancelled:,}). "
            "Ola should investigate driver-side cancellation patterns."
        )
    else:
        st.info(
            "Customer cancellations are higher than driver cancellations. "
            "Ola should investigate customer cancellation patterns."
        )

    # 3. Revenue Analysis

    st.divider()

    st.subheader("3. Revenue Insights")

    successful_df = df[
        df["Booking_Status"] == "Success"
    ].copy()

    total_revenue = successful_df["Booking_Value"].sum()

    average_booking_value = (
        successful_df["Booking_Value"].mean()
    )

    col1, col2 = st.columns(2)

    col1.metric("Total Successful Ride Revenue", f"₹{total_revenue:,.0f}")
    col2.metric(
        "Average Booking Value",
        f"₹{average_booking_value:,.2f}"
    )

    payment_revenue = (
        successful_df.groupby("Payment_Method")["Booking_Value"]
        .sum()
        .sort_values(ascending=False)
    )

    st.write("Revenue generated by payment method")
    st.bar_chart(payment_revenue)

    if not payment_revenue.empty:
        top_payment = payment_revenue.idxmax()

        st.success(
            f"{top_payment} generated the highest revenue "
            f"(₹{payment_revenue.max():,.0f})."
        )

    # 4. Vehicle Performance

    st.divider()

    st.subheader("4. Vehicle Performance")

    vehicle_bookings = (
        df.groupby("Vehicle_Type")
        .size()
        .sort_values(ascending=False)
    )

    st.write("Bookings by vehicle type")
    st.bar_chart(vehicle_bookings)

    if not vehicle_bookings.empty:
        top_vehicle = vehicle_bookings.idxmax()

        st.success(
            f"{top_vehicle} recorded the highest number of bookings "
            f"({vehicle_bookings.max():,})."
        )

    # 5. Customer and Driver Ratings

    st.divider()

    st.subheader("5. Customer and Driver Satisfaction")

    avg_driver_rating = successful_df["Driver_Ratings"].mean()

    avg_customer_rating = successful_df["Customer_Rating"].mean()

    col1, col2 = st.columns(2)

    col1.metric(
        "Average Driver Rating",
        f"{avg_driver_rating:.2f}/5"
    )

    col2.metric(
        "Average Customer Rating",
        f"{avg_customer_rating:.2f}/5"
    )

    if avg_driver_rating < 4 or avg_customer_rating < 4:
        st.warning(
            "At least one average rating is below 4. "
            "Ola can investigate customer feedback and service quality."
        )
    else:
        st.success(
            "Both average ratings are at least 4 out of 5, "
            "indicating positive average feedback."
        )

    # 6. Peak Demand Analysis

    st.divider()

    st.subheader("6. Peak Demand Analysis")

    if "Booking_Hour" in df.columns:

        hourly_bookings = (
            df.groupby("Booking_Hour")
            .size()
            .sort_values(ascending=False)
        )

        st.bar_chart(hourly_bookings.sort_index())

        peak_hour = hourly_bookings.idxmax()
        peak_bookings = hourly_bookings.max()

        st.info(
            f"The highest booking volume occurred at "
            f"{int(peak_hour):02d}:00, with "
            f"{peak_bookings:,} bookings."
        )

    # 7. Business Recommendations

    st.divider()

    st.subheader("7. Business Recommendations")

    recommendations = [
        (
            "Improve Driver Availability",
            "Investigate driver cancellation patterns and improve "
            "driver allocation during high-demand periods."
        ),
        (
            "Optimize Vehicle Allocation",
            "Use vehicle-wise booking trends to allocate suitable "
            "vehicles according to customer demand."
        ),
        (
            "Improve Customer Experience",
            "Analyze customer feedback and ratings to identify "
            "areas where ride service quality can improve."
        ),
        (
            "Improve Revenue Strategy",
            "Monitor payment preferences and booking value patterns "
            "to support better revenue planning."
        ),
        (
            "Manage Peak Demand",
            "Use hourly booking trends to plan driver availability "
            "during busy periods."
        )
    ]

    for title, description in recommendations:
        with st.expander(title):
            st.write(description)

    st.divider()

    st.caption(
        "Note: These recommendations are based on observed patterns "
        "in the July 2024 dataset. They are analytical suggestions, "
        "not proof of cause-and-effect relationships."
    )



# --------------------------------
# Power BI Dashboard
# --------------------------------

elif page == "Power BI Dashboard":

    st.header("📊 Power BI Dashboard")

    st.write(
        "Explore the five analytical views of the Ola Ride Insights project."
    )

    st.divider()

    # Screenshot folder
    SCREENSHOT_DIR = (
        PROJECT_DIR / "power bi" / "screenshots"
    )

    dashboard_images = {
        "Overall Dashboard": "overall_dashboard.png",
        "Vehicle Type Analysis": "vehicle_analysis.png",
        "Revenue Analysis": "revenue_analysis.png",
        "Cancellation Analysis": "cancellation_analysis.png",
        "Ratings Analysis": "ratings_analysis.png"
    }

    # Select dashboard page
    selected_dashboard = st.selectbox(
        "Select Dashboard Page",
        list(dashboard_images.keys()),
        key="powerbi_dashboard_selection"
    )

    image_path = (
        SCREENSHOT_DIR / dashboard_images[selected_dashboard]
    )

    if image_path.exists():

        st.subheader(selected_dashboard)

        st.image(
            str(image_path),
            use_container_width=True
        )

    else:

        st.error(
            f"Screenshot not found: {image_path.name}"
        )

    st.divider()

    st.subheader("All Dashboard Pages")

    for dashboard_name, image_name in dashboard_images.items():

        image_path = SCREENSHOT_DIR / image_name

        with st.expander(dashboard_name):

            if image_path.exists():

                st.image(
                    str(image_path),
                    use_container_width=True
                )

            else:

                st.warning(
                    f"Please add {image_name} to the screenshots folder."
                )

    st.divider()

    st.info(
        "The interactive Power BI report is available locally as "
        "Ola_Ride_Insights_Dashboard.pbix. "
        "Open it using Power BI Desktop to explore the interactive visuals."
    )



# --------------------------------
# 11. Footer
# --------------------------------

st.sidebar.divider()
st.sidebar.caption("Ola Ride Insights | July 2024")
st.sidebar.caption("Data Analytics Project")

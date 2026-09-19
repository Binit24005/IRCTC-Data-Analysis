# 🚆 IRCTC UTS Ticketing & Passenger Flow Analysis

A data analytics and interactive dashboard project built to analyze **Unreserved Ticketing System (UTS) booking data** and identify passenger-flow patterns, peak travel hours, busy routes, railway-line performance, fare trends, and booking-mode adoption.

The project combines **Python, Pandas, NumPy, MySQL, SQL, Plotly, and Streamlit** to transform raw railway ticketing data into meaningful analytical insights and an interactive dashboard.

> **Note:** This is an independent academic/portfolio analytics project based on a UTS ticketing dataset. It is not an official IRCTC or Indian Railways application.

---

## 📊 Project Highlights

| Metric             |          Value |
| ------------------ | -------------: |
| Cleaned Bookings   |     **89,959** |
| Total Fare Revenue | **₹3,375,885** |
| Unique Routes      |         **90** |
| Stations           |         **18** |
| Railway Lines      |          **4** |
| Booking Modes      |          **2** |
| Hour Range         |       **0–23** |

### Railway Lines

The cleaned dataset contains four railway-line categories:

* Central
* Harbour
* Pune
* Western

### Booking Modes

The dataset contains two booking modes:

* Paper
* Paperless

---

## 🎯 Project Objectives

The main objectives of this project are to:

* Analyze passenger booking patterns.
* Identify peak travel and booking hours.
* Find the busiest commuter routes.
* Compare railway-line booking activity.
* Analyze fare revenue across railway lines.
* Examine Paper vs Paperless booking adoption.
* Calculate passenger and fare-related metrics.
* Provide interactive filtering through a Streamlit dashboard.
* Use SQL to perform structured analytical queries.
* Convert raw ticketing data into portfolio-ready business insights.

---

## 🗂️ Dataset

The project works with UTS ticketing data containing booking-level information.

### Raw Dataset

```text
data/Uts_Data.csv
```

The raw dataset contains approximately **718,661 rows**.

### Cleaned Dataset

```text
data/cleaned_uts_data.csv
```

After cleaning and removing repeated `Booking_ID` transactions, the working dataset contains:

```text
89,959 bookings
```

The Streamlit dashboard uses the cleaned dataset.

---

## 🧹 Data Cleaning

The data-cleaning pipeline is implemented in:

```text
src/data_cleaning.py
```

The process includes:

1. Loading the raw CSV dataset.
2. Removing repeated transactions using `Booking_ID`.
3. Converting dates into proper date format.
4. Creating `Day_Name`.
5. Creating the `Is_Weekend` indicator.
6. Extracting booking/travel hour from the time field.
7. Converting passenger counts into numeric values.
8. Validating and converting total fare values.
9. Calculating fare per passenger.
10. Removing unnecessary whitespace from text fields.
11. Standardizing text values.
12. Exporting the cleaned dataset.

### Derived Fields

The cleaning process produces useful analytical fields such as:

```text
Day_Name
Is_Weekend
Hour
Fare_Per_Passenger
```

---

## 📈 Data Analysis

The project performs exploratory and descriptive analysis using Python and SQL.

### 1. Peak Travel Hours

The project analyzes booking volume across the **24-hour period from 0–23** to identify periods with higher booking activity.

### 2. Busiest Routes

Routes are created using:

```text
From_Station → To_Station
```

The project identifies the top commuter routes based on booking volume and also calculates route revenue.

### 3. Railway-Line Analysis

The project compares:

* Booking volume
* Passenger volume
* Total fare revenue
* Average fare per passenger

across the four railway-line categories.

### 4. Booking Mode Analysis

The dataset is analyzed by:

```text
Paper
Paperless
```

The SQL analysis also calculates the percentage share of each booking-mode/payment combination.

### 5. Revenue Analysis

Total fare revenue is calculated from the `Total_Fare` field and analyzed at different levels, including railway line and route.

---

## 🗄️ MySQL & SQL Analysis

The project includes a MySQL database:

```text
irctc_uts_db
```

The main table is:

```text
uts_bookings
```

Database schema:

```text
sql/database.sql
```

Analytical queries:

```text
sql/analysis.sql
```

### SQL Analysis Includes

* Total bookings
* Total passengers
* Total revenue
* Average fare per passenger
* Peak travel hours
* Top 10 commuter routes
* Railway-line performance
* Booking-mode adoption

Example:

```sql
SELECT
    Railway_Line,
    COUNT(*) AS bookings,
    SUM(Passengers) AS passengers,
    SUM(Total_Fare) AS revenue,
    ROUND(AVG(Fare_Per_Passenger), 2) AS avg_fare
FROM uts_bookings
GROUP BY Railway_Line
ORDER BY bookings DESC;
```

---

# 🚆 Interactive Streamlit Dashboard

The project includes an interactive dashboard built using **Streamlit**.

Main application:

```text
app.py
```

### Dashboard Features

* Dark railway-control-room inspired interface
* Interactive railway-line filtering
* Booking-mode filtering
* Travel-hour filtering
* Dynamic KPI cards
* Total bookings
* Total fare revenue
* Unique routes
* Number of stations
* Peak-hour insights
* Busiest-route insights
* Booking-mode insights
* Railway-line revenue analysis
* Route-level analytics
* Interactive Plotly charts
* Filtered dataset download
* Dataset preview

### Dashboard Filters

Users can filter the dataset by:

```text
Railway Line
Booking Mode
Travel Hour
```

The dashboard recalculates the displayed KPIs and analytical results based on the selected filters.

---

## 📊 Dashboard Visualizations

The dashboard provides visual analysis for:

### Peak Travel Hours

Displays booking activity throughout the day.

### Top Busiest Routes

Displays the highest-volume station-to-station routes.

### Booking Mode Distribution

Shows the distribution between:

```text
Paper
Paperless
```

### Railway-Line Revenue

Compares total fare revenue across railway-line categories.

### Route Analytics

Allows users to select an individual route and inspect:

* Total bookings
* Revenue
* Average fare
* Top booking mode
* Hourly booking activity

---

## 🛠️ Technologies Used

### Programming & Data Analysis

* Python
* Pandas
* NumPy

### Database

* MySQL
* SQL

### Visualization

* Plotly
* Matplotlib
* Seaborn

### Dashboard

* Streamlit

### Development

* VS Code
* Git
* GitHub

---

## 📁 Project Structure

```text
IRCTC-Data-Analysis/
│
├── data/
│   ├── Uts_Data.csv
│   └── cleaned_uts_data.csv
│
├── notebooks/
│   └── analysis.ipynb
│
├── sql/
│   ├── database.sql
│   └── analysis.sql
│
├── src/
│   ├── data_cleaning.py
│   ├── data_analysis.py
│   └── database.py
│
├── visualizations/
│
├── app.py
├── README.md
└── requirements.txt
```

---

# ⚙️ Installation & Setup

## 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate into the project:

```bash
cd IRCTC-Data-Analysis
```

---

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

---

## 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## 4. Run the Data Cleaning Pipeline

From the project root:

```powershell
python src\data_cleaning.py
```

This processes:

```text
data/Uts_Data.csv
```

and generates:

```text
data/cleaned_uts_data.csv
```

---

# 📊 Run the Dashboard

From the project root:

```powershell
streamlit run app.py
```

The Streamlit application will open in your browser.

---

# 🗄️ MySQL Setup

Make sure MySQL is installed and running.

Open MySQL Workbench or the MySQL command-line client.

Run:

```sql
SOURCE sql/database.sql;
```

Then load the cleaned CSV data into:

```text
irctc_uts_db
```

table:

```text
uts_bookings
```

After loading the data, run the analytical queries from:

```text
sql/analysis.sql
```

---

# 🔍 Key Analytical Questions

This project focuses on questions such as:

### Passenger Flow

* Which hours have the highest booking activity?
* How does passenger volume vary throughout the day?
* Which routes have the highest booking volume?

### Railway-Line Performance

* Which railway-line categories have the highest booking activity?
* How does fare revenue vary across railway lines?
* What is the average fare per passenger?

### Booking Behavior

* What proportion of transactions are Paper vs Paperless?
* How does booking-mode usage vary across the dataset?

### Route Performance

* Which station pairs have the most bookings?
* Which routes generate higher fare revenue?
* How does hourly activity vary for a selected route?

---

# 💡 Business & Analytical Insights

The dashboard is designed to help explore:

* Peak passenger-demand periods
* High-volume commuter routes
* Railway-line activity
* Fare and revenue patterns
* Paperless booking adoption
* Route-level passenger flow
* Time-based booking behavior

These observations are generated dynamically from the dataset rather than being hard-coded into the dashboard.

---

# 📌 Data Integrity

The dashboard and analytical scripts use the cleaned dataset:

```text
data/cleaned_uts_data.csv
```

The current verified dataset contains:

```text
89,959 bookings
18 stations
90 unique routes
4 railway lines
2 booking modes
Hour values from 0–23
```

The dashboard calculates its KPIs dynamically from the dataset.

---

# 🚧 Limitations

This project is an independent data-analysis project and has several limitations:

* The dataset represents a specific UTS ticketing dataset rather than the complete Indian railway network.
* The railway-line categories in the dataset should not be interpreted as complete national railway divisions.
* The project does not represent live IRCTC booking information.
* The dashboard does not connect to official IRCTC systems or APIs.
* Results depend on the quality and coverage of the supplied dataset.
* Revenue figures represent the `Total_Fare` values present in the dataset.

---

# 🚀 Future Enhancements

Possible future improvements include:

* Deploying the Streamlit dashboard online.
* Adding advanced passenger-flow visualizations.
* Adding station-to-station network analysis based on the dataset.
* Adding date-range filtering.
* Adding weekday/weekend comparisons.
* Adding monthly and weekly trend analysis.
* Adding more interactive Plotly visualizations.
* Adding predictive passenger-demand analysis.
* Adding machine-learning-based demand forecasting.
* Improving dashboard animation and micro-interactions.
* Adding automated data-refresh pipelines.
* Integrating additional railway datasets where legally and technically appropriate.

---

# 🎓 Academic & Portfolio Purpose

This project demonstrates practical experience with:

```text
Data Cleaning
        ↓
Exploratory Data Analysis
        ↓
Feature Engineering
        ↓
SQL Database Design
        ↓
SQL Analytics
        ↓
Data Visualization
        ↓
Interactive Dashboard
        ↓
Business Insights
```

It is designed as a portfolio project demonstrating practical application of Python, SQL, data analysis, visualization, and dashboard development.

---

# 👨‍💻 Author

**Binit Singh**

B.Tech Computer Science Engineering
Galgotias University

### Skills Demonstrated

* Python
* Pandas
* NumPy
* SQL
* MySQL
* Data Analysis
* Data Visualization
* Plotly
* Streamlit
* Git & GitHub

---

## ⭐ Project Status

**Status: Completed — Dashboard Ready for Deployment**

The current local Streamlit dashboard has been tested against the cleaned dataset and its major KPI, filtering, insights, route analytics, and download logic have been verified.

---

## 📜 License

This project is intended for educational, academic, and portfolio purposes.

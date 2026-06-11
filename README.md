# Rajasthan Air Quality and Livability Tracker 🌍

A Python-based ETL pipeline and interactive Streamlit dashboard tracking real-time Air Quality Index (AQI) and PM2.5 levels across major cities in Rajasthan.

## 🚀 Features

Live API Extraction: Fetches real-time environmental data using the WAQI API.

Automated Data Cleaning: Uses pandas and numpy to handle missing sensor data, normalize timestamps, and enforce strict data types.

Local Database: Stores historical data in a lightweight SQLite database for fast querying.

Interactive Dashboard: Built with Streamlit, featuring dynamic scatter plots, historical trend bar charts, and metric cards.

Forecasting Engine: Implements a Statistical Simple Moving Average (SMA) model to predict short-term air quality trends.

## 🛠️ Tech Stack

Language: Python 3.11

Data Pipeline: requests, pandas, numpy

Database: SQLite3

Frontend UI: streamlit

## ⚙️ Installation & Setup

### 1. Clone the repository and navigate to the folder:

git clone [https://github.com/Ajay-K-0304/rajasthan-air-quality-tracker](https://github.com/Ajay-K-0304/rajasthan-air-quality-tracker)
cd rajasthan-aqi-tracker


### 2. Create and activate a virtual environment:

## Windows
python -m venv .venv
.venv\Scripts\activate

## Mac/Linux
python3 -m venv .venv
source .venv/bin/activate


### 3. Install the required dependencies:

pip install requests pandas numpy streamlit


### 4. Add your API Key:

Open etl.py and replace YOUR_TOKEN_HERE with your free token from aqicn.org.

## 🏃‍♂️ Running the Application

### Step 1: Extract and Load Data
Run the ETL script to fetch live data from the internet, clean it, and store it in your local database (aqi_data.db).

python etl.py


(Tip: Run this command a few times throughout the day to build up a history of data for your charts!)

### Step 2: Launch the Dashboard
Start the Streamlit server to view the interactive web interface.

streamlit run app.py


(If the command is not found, use python -m streamlit run app.py)

# 👤 Author

**Name: Ajay Kumar Kumawat**

**Roll No: 23ESKIT014**

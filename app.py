import streamlit as st
import pandas as pd
import sqlite3
from predict import getNextDayPrediction
from etl import fetchAndStoreData
# Set the title and layout of the web page
st.set_page_config(page_title="Rajasthan AQI Tracker", layout="wide")

def load_data():
    #Connects to the SQLite database and loads the data into a Pandas DataFrame
    try:
        conn = sqlite3.connect("aqi_data.db")
        df = pd.read_sql_query("SELECT * FROM readings", conn)
        conn.close()
        return df
    except sqlite3.OperationalError:
        return pd.DataFrame()

# Load the data
df = load_data()

# Sidebar Navigation
st.sidebar.title("🧭 Navigation")

st.sidebar.markdown("### 🔄 Data Controls")
if st.sidebar.button("Fetch Latest Data", use_container_width=True):
    with st.spinner("Fetching real-time data from API..."):
        fetchAndStoreData() # This runs your ETL script!
    st.sidebar.success("Database Updated Successfully!")
    st.rerun() # This instantly refreshes the page to show the new data

st.sidebar.divider()

viewmode = st.sidebar.radio("Go to", ["Dashboard", "Raw Data View"])

if df.empty:
    st.warning("⚠️ No data found in the database! Please open your terminal and run `python etl.py` first to fetch data.")
elif viewmode == "Raw Data View":
    # ==========================================
    # RAW DATA VIEW
    # ==========================================
    st.title("Raw Data Database")
    st.markdown("View all historical records saved in the local SQLite database.")
    
    #Add filters for the raw data table
    st.sidebar.header("Data Filters")
    filterCity = st.sidebar.selectbox("Filter by City", ["All"] + list(df['city'].unique()))
    
    if filterCity != "All":
        filteredDf = df[df['city'] == filterCity]
    else:
        filteredDf = df
        
    st.dataframe(filteredDf, use_container_width=True)

else:
    # DASHBOARD VIEW
    st.title("Rajasthan Air Quality Dashboard")
    st.markdown("A live tracker for Air Quality Index (AQI) and PM2.5 levels.")
    
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed')
    latestAllCities = df.sort_values('timestamp').groupby('city').tail(1)

    #Quick Insights
    st.subheader("Quick Insights")
    
    # Calculate answers dynamically
    highestAqi = latestAllCities.loc[latestAllCities['aqi'].idxmax()]
    highestPm25 = latestAllCities.loc[latestAllCities['pm25'].idxmax()]
    healthiest = latestAllCities.loc[latestAllCities['aqi'].idxmin()]
    
    # Calculate highest risk city using the prediction module
    worstFutureCity = "None"
    maxPredictedAqi = -1
    for city in df['city'].unique():
        pred = getNextDayPrediction(df[df['city'] == city])
        if pred['predicted_aqi'] > maxPredictedAqi:
            maxPredictedAqi = pred['predicted_aqi']
            worstFutureCity = city

    # Display Insight Blocks
    c1, c2, c3, c4 = st.columns(4)
    c1.error(f"**Highest AQI Now:**\n\n{highestAqi['city']} ({int(highestAqi['aqi'])})")
    c2.warning(f"**Max PM 2.5 Level:**\n\n{highestAqi['city']} ({float(highestAqi['pm25'])})")
    c3.info(f"**Highest AQI (Predicted):**\n\n{worstFutureCity} ({maxPredictedAqi})")
    c4.success(f"**Healthiest City:**\n\n{healthiest['city']} ({int(healthiest['aqi'])})")

    st.divider()

    #Scatter Plot
    st.subheader("🌐 AQI vs PM 2.5 Correlation")
    st.scatter_chart(latestAllCities, x='pm25', y='aqi', color='city' , x_label='PM2.5(μ g/m³)' , y_label="AQI")

    st.divider()
    #Deep Dive
    st.sidebar.header("Dashboard Controls")
    cityList = df['city'].unique()
    selectedCity = st.sidebar.selectbox("Select a City to Deep Dive", cityList)

    cityDf = df[df['city'] == selectedCity]
    latestRecord = cityDf.iloc[-1]

    st.subheader(f"Deep Dive: {selectedCity}")
    st.markdown(f"**Station:** {latestRecord['station']} | **Last Updated:** {latestRecord['timestamp']}")

    #Current Metrics & Prediction
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Current AQI", value=int(latestRecord['aqi']))
    col2.metric(label="PM 2.5 Level", value=float(latestRecord['pm25']))
    
    #Calculate Prediction instantly for the block
    predictions = getNextDayPrediction(cityDf)
    aqiDelta = int(predictions['predicted_aqi'] - latestRecord['aqi'])
    col3.metric(
        label="Predicted Next AQI", 
        value=predictions['predicted_aqi'],
        delta=f"{aqiDelta} points",
        delta_color="inverse" 
    )

    st.write("") 
    # Add some spacing
    
    #Separate Historical Graphs
    st.markdown("#### Historical Trends")
    
    # AQI Graph
    st.markdown(f"**AQI Timeline for {selectedCity}**")
    aqiChartData = cityDf.set_index('timestamp')['aqi']
    st.bar_chart(aqiChartData, use_container_width=True)
    
    # PM 2.5 Graph
    st.markdown(f"**PM 2.5 Timeline for {selectedCity}**")
    pm25_chart_data = cityDf.set_index('timestamp')['pm25']
    st.bar_chart(pm25_chart_data, use_container_width=True)
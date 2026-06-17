import requests
import sqlite3
import pandas as pd
import numpy as np
import os
from dotenv import  load_dotenv

#Using env variables for safely storing api key and using it here
load_dotenv()
apiKey=os.getenv("myKey")

apiToken = apiKey

#We are tracking these cities only , but more can be added
cities = ["Jaipur", "Jodhpur", "Udaipur", "Kota", "Delhi"]
dbName = "aqi_data.db"

def initDb():
    #Create db if not present
    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            city TEXT,
            station TEXT,
            aqi INTEGER,
            pm25 REAL
        )
    ''')
    conn.commit()
    return conn

def fetchAndStoreData():
    print("Starting ETL Pipeline\n")

    rawData = []

    #Extract
    for city in cities:
        url = f"https://api.waqi.info/feed/{city}/?token={apiToken}"
        try:
            response = requests.get(url,timeout=10)
            data = response.json()

            if data.get("status") == "ok":
                cityData = data["data"]

                # Instead of cleaning here, we just grab the raw data into a dictionary
                row = {
                    "timestamp": cityData.get("time", {}).get("iso"),
                    "city": city,
                    "station": cityData.get("city", {}).get("name"),
                    "aqi": cityData.get("aqi"),
                    "pm25": cityData.get("iaqi", {}).get("pm25", {}).get("v")
                }
                rawData.append(row)
                print(f"Downloaded raw data for {city.upper()}")
            else:
                print(f"Failed to get data for {city}.")
        except Exception as e:
            print(f"Network error while fetching {city}: {e}")

    if not rawData:
        print("No data collected. Exiting.")
        return
    
    #Transforming data
    print("\nCleaning data...")
    
    #Load the raw dictionaries into a Pandas DataFrame
    df = pd.DataFrame(rawData)

    #We use numpy to replace '-' or empty strings with actual NaN values.
    df['aqi'] = df['aqi'].replace('-', np.nan)
    
    #Pandas Operation: Force columns to be strict numeric types
    df['aqi'] = pd.to_numeric(df['aqi'], errors='coerce')
    df['pm25'] = pd.to_numeric(df['pm25'], errors='coerce')

    #Fill any NaN/missing values with 0 so our charts don't crash
    df['aqi'] = df['aqi'].fillna(0).astype(int)
    df['pm25'] = df['pm25'].fillna(0.0)

    #Standardize city and station names (uppercase and strip spaces)
    df['city'] = df['city'].str.upper().str.strip()
    df['station'] = df['station'].str.strip()

    #Convert messy API timestamps into clean SQL formats
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')

    print("\nPreview of Cleaned DataFrame:")
    print(df.head())

    # ==========================================
    # 3. LOAD (Using Pandas to SQL)
    # ==========================================
    print("\nSaving to SQLite...")
    conn = initDb()
    
    # 'append' adds the new DataFrame rows perfectly matching our SQLite columns.
    df.to_sql("readings", conn, if_exists="append", index=False)
    
    conn.close()
    print("🎉 ETL process complete! Data safely stored.")

if __name__ == "__main__":
    fetchAndStoreData()
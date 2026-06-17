import requests

# 1. Paste your WAQI API token here
API_TOKEN = "cc6a4e20a34fd67ff7b87625cdfa32446254f4a4"

# 2. The cities we want to track
CITIES = ["Jaipur", "Jodhpur", "Udaipur", "Kota", "Delhi"]

def fetch_aqi_data():
    print("🌍 Starting AQI Data Extraction...\n")

    for city in CITIES:
        # 3. Build the specific URL for each city
        url = f"https://api.waqi.info/feed/{city}/?token={API_TOKEN}"

        try:
            # 4. Make the GET request to the API
            response = requests.get(url, timeout=10)
            data = response.json() # Convert the response to a Python Dictionary

            # 5. The API returns {"status": "ok", "data": {...}} if successful
            if data.get("status") == "ok":
                city_data = data["data"]

                # 6. Extract the exact pieces of information we need
                aqi = city_data.get("aqi")
                station_name = city_data.get("city", {}).get("name", "Unknown Station")
                timestamp = city_data.get("time", {}).get("iso", "Unknown Time")

                # The API stores specific pollutants inside the 'iaqi' dictionary.
                # We use .get() so if PM2.5 is missing, it defaults to 0.0 instead of crashing.
                iaqi = city_data.get("iaqi", {})
                pm25 = iaqi.get("pm25", {}).get("v", 0.0)

                # 7. Print the results to the terminal
                print(f"✅ Data found for {city.upper()}:")
                print(f"   ➤ Station: {station_name}")
                print(f"   ➤ Time:    {timestamp}")
                print(f"   ➤ AQI:     {aqi}")
                print(f"   ➤ PM2.5:   {pm25}\n")

            else:
                print(f"❌ Failed to get data for {city}. API said: {data.get('data')}\n")

        except Exception as e:
            # If your internet is down or the API crashes, this stops your whole app from dying.
            print(f"⚠️ Network error while fetching {city}: {e}\n")

if __name__ == "__main__":
    fetch_aqi_data()
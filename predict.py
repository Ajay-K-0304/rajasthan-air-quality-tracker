import pandas as pd

def getNextDayPrediction(city_df, window=3):
    #Calculates the Simple Moving Average (SMA) to predict the next reading.
    #It takes the average of the most recent data points (default last 3).
    if city_df.empty:
        return {"predicted_aqi": 0, "predicted_pm25": 0}

    # Ensure data is sorted by timestamp so we are getting the latest records
    sortedDf = city_df.sort_values(by='timestamp')

    # If we have fewer rows than the window, use whatever number of rows we have
    actualWindow = min(len(sortedDf), window)

    # Grab the most recent 'n' records
    recentData = sortedDf.tail(actualWindow)

    # Calculate the average (SMA)
    predAqi = recentData['aqi'].mean()
    predPM25 = recentData['pm25'].mean()

    # Return as a clean dictionary
    return {
        "predicted_aqi": int(round(predAqi)),
        "predicted_pm25": round(predPM25, 2)
    }
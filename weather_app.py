import streamlit as st
import requests

# Title
st.title("🌤️ Weather Forecast App")

# Input from user
city = st.text_input("Enter City Name", "New York")

# ✅ Your working OpenWeatherMap API key
API_KEY = "619338abb069f1e139d446a5b257b1a3"

def get_weather(city_name, api_key):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    return response.json()

if st.button("Get Weather"):
    if city:
        data = get_weather(city, API_KEY)

        # Show raw data for debugging
        # st.write("Debug Info:", data)

        if data.get("cod") == 200:
            st.success(f"Weather in {city}")
            st.metric("Temperature", f"{data['main']['temp']} °C")
            st.metric("Feels Like", f"{data['main']['feels_like']} °C")
            st.metric("Humidity", f"{data['main']['humidity']} %")
            st.metric("Wind Speed", f"{data['wind']['speed']} m/s")
            st.write(f"Weather Description: {data['weather'][0]['description'].title()}")
        else:
            st.error(f"Error: {data.get('message', 'Unknown error')}")

import streamlit as st
import pandas as pd
import requests
import os
import streamlit as st
import os

API_KEY = os.getenv("WEATHER_API_KEY") or st.secrets.get("WEATHER_API_KEY")


# Load the world cities CSV
cities_df = pd.read_csv("worldcities.csv")

st.set_page_config(page_title="Weather-Based Clothing Recommender")
st.title("🌤️ Weather-Based Clothing Recommender")

# Dropdown to select country
countries = cities_df['country'].unique()
selected_country = st.selectbox("Select a Country", sorted(countries))

# Filter cities by selected country
filtered_cities = cities_df[cities_df['country'] == selected_country]
city_names = filtered_cities['city'].unique()
selected_city = st.selectbox("Select a City", sorted(city_names))

# Button to fetch weather
if st.button("Get Recommendation"):
    if selected_city:
        country_code = filtered_cities[filtered_cities['city'] == selected_city]['iso2'].values[0]

        if API_KEY:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={selected_city},{country_code}&appid={API_KEY}&units=metric"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                temp = data['main']['temp']
                weather = data['weather'][0]['description'].capitalize()

                st.markdown(f"""
                    <div style="background-color:#f0f8ff;padding:20px;border-radius:15px;box-shadow:0 4px 8px rgba(0,0,0,0.2);">
                        <h3 style="color:#333;">🌤️ Weather in {selected_city}</h3>
                        <p style="font-size:22px;margin:0;"><strong>🌡️ Temperature:</strong> {temp}°C</p>
                        <p style="font-size:18px;"><strong>Condition:</strong> {weather}</p>
                    </div>
                """, unsafe_allow_html=True)

                # Clothing recommendation
                if temp > 30:
                    recommendation = "🩳 It's hot! Wear light cotton clothes. Stay hydrated 💧"
                elif 20 <= temp <= 30:
                    recommendation = "👕 Pleasant weather. Wear comfortable clothes."
                elif 10 <= temp < 20:
                    recommendation = "🧥 It's cool. Carry a jacket."
                else:
                    recommendation = "🧣 Brrr! It's cold. Wear warm clothes."

                st.markdown(f"""
                    <div style="background-color:#e6ffe6;padding:15px;margin-top:15px;border-left:5px solid #00cc44;border-radius:10px;">
                        <strong>{recommendation}</strong>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.error("❌ Could not fetch weather data. Try a different location.")
        else:
            st.error("⚠️ API key not found. Please make sure it's set correctly in the .env file.")

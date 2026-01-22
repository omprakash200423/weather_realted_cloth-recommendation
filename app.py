import streamlit as st
import requests
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Weather-Based Clothing Recommender",
    page_icon="🌤️",
    layout="centered"
)

# ---------------- CSS (DARK RESULT CARDS) ----------------
st.markdown(
    """
    <style>
    body {
        background-color: #0f172a;
    }
    .weather-card {
        background-color: #111827;
        color: white;
        padding: 20px;
        border-radius: 14px;
        margin-top: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
        font-size: 18px;
    }
    .recommend-card {
        background-color: #064e3b;
        color: #d1fae5;
        padding: 18px;
        border-radius: 14px;
        margin-top: 15px;
        font-size: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- API KEY ----------------
API_KEY = st.secrets["WEATHER_API_KEY"]

# ---------------- TITLE ----------------
st.title("🌤️ Weather-Based Clothing Recommender")

# ---------------- LOAD CITY DATA ----------------
df = pd.read_csv("worldcities.csv")

countries = sorted(df["country"].unique())
country = st.selectbox("Select a Country", countries)

cities = sorted(df[df["country"] == country]["city"].unique())
city = st.selectbox("Select a City", cities)

# ---------------- WEATHER FETCH ----------------
def get_weather(city):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )
    response = requests.get(url)
    return response.json()

# ---------------- CLOTHING LOGIC ----------------
def clothing_recommendation(temp):
    if temp < 10:
        return "🧥 Very cold weather. Wear jacket, sweater, and warm clothes."
    elif temp < 20:
        return "🧥 Cool weather. Light jacket or hoodie recommended."
    elif temp < 30:
        return "👕 Pleasant weather. Wear comfortable clothes."
    else:
        return "🩳 Hot weather. Wear light cotton clothes."

# ---------------- BUTTON ----------------
if st.button("Get Recommendation"):
    data = get_weather(city)

    if data.get("cod") != 200:
        st.error("❌ Could not fetch weather data.")
    else:
        temp = data["main"]["temp"]
        condition = data["weather"][0]["description"].title()
        recommendation = clothing_recommendation(temp)

        # -------- WEATHER CARD --------
        st.markdown(
            f"""
            <div class="weather-card">
                🌤️ <b>Weather in {city}</b><br><br>
                🌡️ Temperature: <b>{temp}°C</b><br>
                ☁️ Condition: <b>{condition}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        # -------- RECOMMENDATION CARD --------
        st.markdown(
            f"""
            <div class="recommend-card">
                {recommendation}
            </div>
            """,
            unsafe_allow_html=True
        )

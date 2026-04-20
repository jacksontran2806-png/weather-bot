import streamlit as st
import plotly.graph_objects as go
from weather import get_weather

# Page config
st.set_page_config(
    page_title="Weather Dashboard",
    page_icon="🌤️",
    layout="wide"
)

st.title("🌤️ Real-Time Weather Dashboard")

# Cities to track
cities = ["Ho Chi Minh City", "Sydney", "London", "New York", "Tokyo"]

# Fetch weather for all cities
weather_data = []
for city in cities:
    data = get_weather(city)
    if data:
        weather_data.append({
            "City": data["name"],
            "Temperature": data["main"]["temp"],
            "Feels Like": data["main"]["feels_like"],
            "Condition": data["weather"][0]["description"].title(),
            "Humidity": data["main"]["humidity"],
            "Wind Speed": data["wind"]["speed"]
        })

# Display current weather cards
st.subheader("Current Weather")
cols = st.columns(len(weather_data))

for idx, (col, city_data) in enumerate(zip(cols, weather_data)):
    with col:
        # Weather emoji based on condition
        condition = city_data["Condition"].lower()
        if "rain" in condition:
            emoji = "🌧️"
        elif "cloud" in condition:
            emoji = "☁️"
        elif "clear" in condition:
            emoji = "☀️"
        elif "snow" in condition:
            emoji = "❄️"
        else:
            emoji = "🌤️"
        
        st.metric(
            label=f"{emoji} {city_data['City']}",
            value=f"{city_data['Temperature']}°C",
            delta=f"Feels like {city_data['Feels Like']}°C"
        )
        st.caption(city_data["Condition"])

# Comparison table
st.subheader("📊 Weather Comparison")
st.dataframe(weather_data, use_container_width=True)

# Temperature bar chart
st.subheader("🌡️ Temperature Comparison")
fig = go.Figure(data=[
    go.Bar(
        x=[d["City"] for d in weather_data],
        y=[d["Temperature"] for d in weather_data],
        marker_color='lightblue',
        text=[f"{d['Temperature']}°C" for d in weather_data],
        textposition='auto',
    )
])
fig.update_layout(
    yaxis_title="Temperature (°C)",
    showlegend=False,
    height=400
)
st.plotly_chart(fig, use_container_width=True)

# Humidity comparison
st.subheader("💧 Humidity Levels")
fig2 = go.Figure(data=[
    go.Bar(
        x=[d["City"] for d in weather_data],
        y=[d["Humidity"] for d in weather_data],
        marker_color='steelblue',
        text=[f"{d['Humidity']}%" for d in weather_data],
        textposition='auto',
    )
])
fig2.update_layout(
    yaxis_title="Humidity (%)",
    showlegend=False,
    height=400
)
st.plotly_chart(fig2, use_container_width=True)

# Auto-refresh
st.caption("🔄 Dashboard auto-refreshes every 5 minutes")
import streamlit as st
import streamlit.components.v1 as components
from weather import get_weather
from datetime import datetime
import json

# Page config
st.set_page_config(
    page_title="WEATHER TERMINAL",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit default elements
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Get weather data function
def fetch_weather_data(cities):
    weather_data = []
    for city in cities:
        data = get_weather(city)
        if data:
            weather_data.append({
                "city": data["name"],
                "temp": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "condition": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind": data["wind"]["speed"],
                "pressure": data["main"]["pressure"],
                "icon": data["weather"][0]["icon"]
            })
    return weather_data

# Default cities
default_cities = ["Ho Chi Minh City", "Sydney", "London", "New York", "Tokyo"]

# Session state for search
if 'search_city' not in st.session_state:
    st.session_state.search_city = ""

# Render custom HTML dashboard
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Azeret+Mono:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: #000000;
            color: #00ff41;
            font-family: 'Azeret Mono', monospace;
            overflow-x: hidden;
            position: relative;
        }

        /* Animated background grid */
        .grid-background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                linear-gradient(rgba(0, 255, 65, 0.1) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 255, 65, 0.1) 1px, transparent 1px);
            background-size: 50px 50px;
            animation: gridMove 20s linear infinite;
            pointer-events: none;
            z-index: 0;
        }

        @keyframes gridMove {
            0% { transform: translate(0, 0); }
            100% { transform: translate(50px, 50px); }
        }

        .container {
            position: relative;
            z-index: 1;
            max-width: 1800px;
            margin: 0 auto;
            padding: 40px 20px;
        }

        /* Header */
        .terminal-header {
            border: 3px solid #00ff41;
            padding: 30px;
            margin-bottom: 40px;
            background: rgba(0, 0, 0, 0.8);
            box-shadow: 0 0 30px rgba(0, 255, 65, 0.3), inset 0 0 30px rgba(0, 255, 65, 0.1);
            position: relative;
            overflow: hidden;
        }

        .terminal-header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(0, 255, 65, 0.1), transparent);
            animation: scan 3s linear infinite;
        }

        @keyframes scan {
            0% { transform: translateY(-100%) translateX(-100%); }
            100% { transform: translateY(100%) translateX(100%); }
        }

        h1 {
            font-family: 'Orbitron', sans-serif;
            font-size: 4rem;
            font-weight: 900;
            letter-spacing: 8px;
            text-shadow: 0 0 20px #00ff41, 0 0 40px #00ff41;
            margin-bottom: 15px;
            position: relative;
            z-index: 1;
        }

        .status-bar {
            display: flex;
            gap: 30px;
            font-size: 0.9rem;
            margin-top: 15px;
            position: relative;
            z-index: 1;
        }

        .status-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background: #00ff41;
            border-radius: 50%;
            animation: pulse 2s ease-in-out infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; box-shadow: 0 0 10px #00ff41; }
            50% { opacity: 0.5; box-shadow: 0 0 5px #00ff41; }
        }

        /* Search input */
        .search-section {
            margin-bottom: 50px;
        }

        .search-label {
            font-size: 1.2rem;
            margin-bottom: 15px;
            letter-spacing: 2px;
            color: #00ff41;
            text-shadow: 0 0 10px #00ff41;
        }

        #citySearch {
            width: 100%;
            padding: 20px 25px;
            font-family: 'Azeret Mono', monospace;
            font-size: 1.3rem;
            background: rgba(0, 0, 0, 0.9);
            border: 3px solid #00ff41;
            color: #00ff41;
            outline: none;
            transition: all 0.3s;
            letter-spacing: 2px;
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.2);
        }

        #citySearch:focus {
            border-color: #00ffff;
            box-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
            color: #00ffff;
        }

        #citySearch::placeholder {
            color: rgba(0, 255, 65, 0.5);
        }

        /* Weather cards grid */
        .weather-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-bottom: 50px;
        }

        .weather-card {
            background: rgba(0, 0, 0, 0.9);
            border: 2px solid #00ff41;
            padding: 30px;
            position: relative;
            overflow: hidden;
            transition: all 0.3s;
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.2);
        }

        .weather-card:hover {
            transform: translateY(-5px);
            border-color: #00ffff;
            box-shadow: 0 0 40px rgba(0, 255, 255, 0.4);
        }

        .weather-card::after {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0, 255, 65, 0.2), transparent);
            transition: left 0.5s;
        }

        .weather-card:hover::after {
            left: 100%;
        }

        .city-name {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 20px;
            letter-spacing: 3px;
            text-shadow: 0 0 15px #00ff41;
        }

        .temp-display {
            font-size: 4rem;
            font-weight: 900;
            font-family: 'Orbitron', sans-serif;
            margin: 20px 0;
            text-shadow: 0 0 30px #00ff41;
            line-height: 1;
        }

        .condition {
            font-size: 1.1rem;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: #00ffff;
        }

        .data-row {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-top: 1px solid rgba(0, 255, 65, 0.3);
            font-size: 0.95rem;
        }

        .data-label {
            opacity: 0.7;
        }

        .data-value {
            font-weight: 600;
        }

        /* Analysis section */
        .analysis-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
            margin-top: 50px;
        }

        .analysis-card {
            background: rgba(0, 0, 0, 0.9);
            border: 2px solid #00ff41;
            padding: 25px;
            text-align: center;
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.2);
        }

        .analysis-title {
            font-size: 0.9rem;
            letter-spacing: 2px;
            margin-bottom: 15px;
            color: #00ffff;
        }

        .analysis-value {
            font-size: 2rem;
            font-weight: 700;
            font-family: 'Orbitron', sans-serif;
            margin: 10px 0;
            text-shadow: 0 0 20px #00ff41;
        }

        .analysis-location {
            font-size: 1.1rem;
            opacity: 0.8;
        }

        /* Footer */
        .terminal-footer {
            margin-top: 50px;
            padding: 20px;
            text-align: center;
            border-top: 2px solid #00ff41;
            font-size: 0.85rem;
            opacity: 0.7;
        }

        /* Loading animation */
        .loading {
            display: none;
            text-align: center;
            font-size: 1.5rem;
            padding: 50px;
            letter-spacing: 3px;
            animation: blink 1s infinite;
        }

        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }

        .error {
            background: rgba(255, 0, 0, 0.2);
            border: 2px solid #ff0000;
            color: #ff0000;
            padding: 20px;
            margin: 20px 0;
            text-align: center;
            font-size: 1.2rem;
            letter-spacing: 2px;
        }
    </style>
</head>
<body>
    <div class="grid-background"></div>
    
    <div class="container">
        <div class="terminal-header">
            <h1>⚡ WEATHER.TERMINAL</h1>
            <div class="status-bar">
                <div class="status-item">
                    <div class="status-dot"></div>
                    <span>SYSTEM: ONLINE</span>
                </div>
                <div class="status-item">
                    <div class="status-dot"></div>
                    <span>API: ACTIVE</span>
                </div>
                <div class="status-item">
                    <div class="status-dot"></div>
                    <span id="currentTime">--:--:--</span>
                </div>
            </div>
        </div>

        <div class="search-section">
            <div class="search-label">&gt; ENTER_TARGET_LOCATION:</div>
            <input type="text" id="citySearch" placeholder="TYPE CITY NAME... (e.g., TOKYO, PARIS, MUMBAI)" />
        </div>

        <div class="loading" id="loading">LOADING DATA...</div>
        <div id="error"></div>
        <div class="weather-grid" id="weatherGrid"></div>
        
        <div class="analysis-grid" id="analysisGrid"></div>

        <div class="terminal-footer">
            ⚡ WEATHER.TERMINAL v2.0 | AUTO-REFRESH: ENABLED | DATA_SOURCE: OPENWEATHERMAP_API
        </div>
    </div>

    <script>
        // Update clock
        function updateClock() {
            const now = new Date();
            const timeString = now.toLocaleTimeString('en-US', { hour12: false });
            document.getElementById('currentTime').textContent = timeString;
        }
        setInterval(updateClock, 1000);
        updateClock();

        // Communicate with Streamlit
        let defaultCities = """ + json.dumps(default_cities) + """;
        
        function fetchWeather(city) {
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: city
            }, '*');
        }

        // Search functionality
        const searchInput = document.getElementById('citySearch');
        let searchTimeout;

        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            const city = e.target.value.trim();
            
            if (city) {
                searchTimeout = setTimeout(() => {
                    fetchWeather(city);
                }, 800);
            } else {
                fetchWeather('');
            }
        });

        // Render weather data
        function renderWeather(data) {
            const grid = document.getElementById('weatherGrid');
            const analysisGrid = document.getElementById('analysisGrid');
            const errorDiv = document.getElementById('error');
            
            if (!data || data.length === 0) {
                errorDiv.innerHTML = '<div class="error">❌ ERROR: LOCATION_NOT_FOUND. CHECK_COORDINATES_AND_RETRY.</div>';
                grid.innerHTML = '';
                analysisGrid.innerHTML = '';
                return;
            }

            errorDiv.innerHTML = '';
            
            // Render cards
            grid.innerHTML = data.map(city => `
                <div class="weather-card">
                    <div class="city-name">${city.city.toUpperCase()}</div>
                    <div class="temp-display">${city.temp}°C</div>
                    <div class="condition">${city.condition.toUpperCase()}</div>
                    <div class="data-row">
                        <span class="data-label">FEELS_LIKE:</span>
                        <span class="data-value">${city.feels_like}°C</span>
                    </div>
                    <div class="data-row">
                        <span class="data-label">HUMIDITY:</span>
                        <span class="data-value">${city.humidity}%</span>
                    </div>
                    <div class="data-row">
                        <span class="data-label">WIND_SPEED:</span>
                        <span class="data-value">${city.wind} m/s</span>
                    </div>
                    <div class="data-row">
                        <span class="data-label">PRESSURE:</span>
                        <span class="data-value">${city.pressure} hPa</span>
                    </div>
                </div>
            `).join('');

            // Analysis
            const hottest = data.reduce((a, b) => a.temp > b.temp ? a : b);
            const coldest = data.reduce((a, b) => a.temp < b.temp ? a : b);
            const mostHumid = data.reduce((a, b) => a.humidity > b.humidity ? a : b);

            analysisGrid.innerHTML = `
                <div class="analysis-card">
                    <div class="analysis-title">🔥 HOTTEST_ZONE</div>
                    <div class="analysis-value">${hottest.temp}°C</div>
                    <div class="analysis-location">${hottest.city.toUpperCase()}</div>
                </div>
                <div class="analysis-card">
                    <div class="analysis-title">❄️ COLDEST_ZONE</div>
                    <div class="analysis-value">${coldest.temp}°C</div>
                    <div class="analysis-location">${coldest.city.toUpperCase()}</div>
                </div>
                <div class="analysis-card">
                    <div class="analysis-title">💧 MAX_HUMIDITY</div>
                    <div class="analysis-value">${mostHumid.humidity}%</div>
                    <div class="analysis-location">${mostHumid.city.toUpperCase()}</div>
                </div>
            `;
        }

        // Initial render placeholder
        renderWeather(""" + json.dumps(fetch_weather_data(default_cities)) + """);
    </script>
</body>
</html>
"""

# Render the component
components.html(html_code, height=1400, scrolling=True)

# Handle city search from component
city_search = st.text_input("City Search (Hidden)", key="city_search_hidden", label_visibility="collapsed")

if city_search:
    cities_to_fetch = [city_search]
else:
    cities_to_fetch = default_cities

# This runs on every interaction but component caches the HTML
weather_json = json.dumps(fetch_weather_data(cities_to_fetch))
import streamlit as st
import streamlit.components.v1 as components
from weather import get_weather
from historical import get_historical_weather
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="WeatherDepths",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── HELPERS ───────────────────────────────────────────────────────────────────

def condition_icon(desc):
    d = desc.lower()
    if "clear" in d:                        return "☀️"
    if "few cloud" in d or "partly" in d:   return "⛅"
    if "scatter" in d:                      return "🌤️"
    if "broken" in d or "overcast" in d:    return "☁️"
    if "drizzle" in d or "light rain" in d: return "🌦️"
    if "rain" in d or "shower" in d:        return "🌧️"
    if "thunder" in d or "storm" in d:      return "⛈️"
    if "snow" in d or "sleet" in d:         return "❄️"
    if "mist" in d or "fog" in d or "haze" in d: return "🌫️"
    return "🌤️"

def fetch_weather_data(cities):
    result = []
    for city in cities:
        data = get_weather(city)
        if data:
            result.append({
                "city":       data["name"],
                "temp":       data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "condition":  data["weather"][0]["description"],
                "humidity":   data["main"]["humidity"],
                "wind":       data["wind"]["speed"],
                "pressure":   data["main"]["pressure"],
            })
    return result

# ── STREAMLIT GLOBAL CSS ──────────────────────────────────────────────────────

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Inter:wght@400;500&display=swap" rel="stylesheet">
<style>
    #MainMenu, footer, header { visibility: hidden; }

    .stApp, .main { background: #0d1b2a !important; }
    .block-container {
        background: #0d1b2a !important;
        padding-top: 1.5rem !important;
        padding-bottom: 4rem !important;
        max-width: 1400px !important;
    }

    /* Search input */
    .stTextInput > label {
        font-family: 'Inter', sans-serif !important;
        color: rgba(168,218,220,0.65) !important;
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        letter-spacing: 1.8px !important;
        text-transform: uppercase !important;
    }
    .stTextInput > div > div > input {
        background: rgba(22,39,58,0.85) !important;
        border: 1px solid rgba(45,139,139,0.35) !important;
        border-radius: 10px !important;
        color: #f1faee !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        padding: 12px 16px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.25) !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
        letter-spacing: normal !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: rgba(45,139,139,0.75) !important;
        box-shadow: 0 0 0 3px rgba(45,139,139,0.12) !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: rgba(168,218,220,0.3) !important;
    }

    /* Selectbox */
    [data-testid="stSelectbox"] > label {
        font-family: 'Inter', sans-serif !important;
        color: rgba(168,218,220,0.65) !important;
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        letter-spacing: 1.8px !important;
        text-transform: uppercase !important;
    }
    [data-testid="stSelectbox"] > div > div {
        background: rgba(22,39,58,0.85) !important;
        border: 1px solid rgba(45,139,139,0.35) !important;
        border-radius: 10px !important;
        color: #f1faee !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Section headers in Streamlit land */
    .section-hdr {
        border-left: 3px solid #2d8b8b;
        padding: 12px 18px;
        margin: 8px 0 20px 0;
        background: rgba(22,39,58,0.5);
        border-radius: 0 8px 8px 0;
    }
    .section-hdr h3 {
        font-family: 'Poppins', sans-serif;
        font-size: 1.1rem; font-weight: 600;
        color: #f1faee; margin: 0 0 2px 0;
    }
    .section-hdr p {
        font-family: 'Inter', sans-serif;
        font-size: 0.72rem; color: rgba(168,218,220,0.5);
        margin: 0; letter-spacing: 0.3px;
    }
    .err-notice {
        background: rgba(220,53,69,0.08);
        border: 1px solid rgba(220,53,69,0.3);
        border-radius: 10px; padding: 12px 16px;
        color: #e57373; font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# ── INPUTS ────────────────────────────────────────────────────────────────────

default_cities = ["Ho Chi Minh City", "Sydney", "London", "New York", "Tokyo"]

city_input = st.text_input(
    "Search location",
    placeholder="Enter a city — Paris, Mumbai, Dubai...",
    key="city_search",
)

cities_to_display = [city_input.strip()] if city_input.strip() else default_cities
weather_data = fetch_weather_data(cities_to_display)

# ── BUILD WEATHER CARDS ───────────────────────────────────────────────────────

def build_card(city):
    icon = condition_icon(city["condition"])
    return f"""
    <div class="card">
        <div class="card-glow"></div>
        <div class="card-top-bar"></div>
        <span class="card-watermark">{icon}</span>
        <div class="card-header">
            <div class="city-name">{city["city"]}</div>
            <span class="badge">{icon} {city["condition"].title()}</span>
        </div>
        <div class="temp-row">
            <span class="temp">{city["temp"]}</span><span class="temp-unit">°C</span>
        </div>
        <div class="divider"></div>
        <div class="metric"><span class="lbl">🌡 Feels like</span><span class="val">{city["feels_like"]}°C</span></div>
        <div class="metric"><span class="lbl">💧 Humidity</span><span class="val">{city["humidity"]}%</span></div>
        <div class="metric"><span class="lbl">💨 Wind</span><span class="val">{city["wind"]} m/s</span></div>
        <div class="metric"><span class="lbl">📊 Pressure</span><span class="val">{city["pressure"]} hPa</span></div>
    </div>"""

cards_html = "".join(build_card(c) for c in weather_data) if weather_data else ""

analysis_html = ""
if weather_data:
    hottest = max(weather_data, key=lambda x: x["temp"])
    coldest = min(weather_data, key=lambda x: x["temp"])
    humid   = max(weather_data, key=lambda x: x["humidity"])
    windiest = max(weather_data, key=lambda x: x["wind"])
    analysis_html = f"""
    <div class="overview-section">
        <p class="overview-label">Global Overview</p>
        <div class="overview-grid">
            <div class="overview-card">
                <div class="ov-icon">🔥</div>
                <div class="ov-body">
                    <div class="ov-val">{hottest["temp"]}°C</div>
                    <div class="ov-city">{hottest["city"]}</div>
                    <div class="ov-tag">Hottest</div>
                </div>
            </div>
            <div class="overview-card">
                <div class="ov-icon">❄️</div>
                <div class="ov-body">
                    <div class="ov-val">{coldest["temp"]}°C</div>
                    <div class="ov-city">{coldest["city"]}</div>
                    <div class="ov-tag">Coldest</div>
                </div>
            </div>
            <div class="overview-card">
                <div class="ov-icon">💧</div>
                <div class="ov-body">
                    <div class="ov-val">{humid["humidity"]}%</div>
                    <div class="ov-city">{humid["city"]}</div>
                    <div class="ov-tag">Most Humid</div>
                </div>
            </div>
            <div class="overview-card">
                <div class="ov-icon">💨</div>
                <div class="ov-body">
                    <div class="ov-val">{windiest["wind"]} m/s</div>
                    <div class="ov-city">{windiest["city"]}</div>
                    <div class="ov-tag">Windiest</div>
                </div>
            </div>
        </div>
    </div>"""

n = len(weather_data)
error_html = """<div class="error-notice">⚠️ Location not found — please check the city name.</div>""" if not weather_data else ""

# ── MAIN HTML ─────────────────────────────────────────────────────────────────

html_code = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Inter:wght@400;500&display=swap" rel="stylesheet">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}

body {{
    background: #0d1b2a;
    color: #f1faee;
    font-family: 'Inter', sans-serif;
    padding: 28px 28px 20px;
    min-height: 100vh;
}}

/* Ambient mesh background */
.mesh {{
    position: fixed; inset:0; z-index:0; pointer-events:none;
    background:
        radial-gradient(ellipse 65% 55% at 12% 8%,  rgba(45,139,139,0.10) 0%, transparent 60%),
        radial-gradient(ellipse 45% 65% at 88% 92%, rgba(29,62,101,0.20)  0%, transparent 58%),
        radial-gradient(ellipse 35% 35% at 55% 38%, rgba(45,139,139,0.05) 0%, transparent 50%);
}}

.wrap {{ position:relative; z-index:1; max-width:1560px; margin:0 auto; }}

/* ── HEADER ── */
.hdr {{
    display:flex; justify-content:space-between; align-items:center;
    flex-wrap:wrap; gap:16px;
    padding-bottom:28px;
    border-bottom:1px solid rgba(45,139,139,0.14);
    margin-bottom:32px;
}}

.brand {{ display:flex; align-items:center; gap:14px; }}

.brand-logo {{
    width:48px; height:48px;
    background: linear-gradient(145deg, #2d8b8b 0%, #a8dadc 100%);
    border-radius:14px;
    display:flex; align-items:center; justify-content:center;
    font-size:1.5rem;
    box-shadow: 0 4px 22px rgba(45,139,139,0.32);
    flex-shrink:0;
}}

.brand-title {{
    font-family:'Poppins',sans-serif;
    font-size:1.55rem; font-weight:700; color:#f1faee; letter-spacing:0.2px;
}}

.brand-sub {{
    font-size:0.73rem; color:rgba(168,218,220,0.55); margin-top:2px;
}}

.pills {{ display:flex; gap:9px; flex-wrap:wrap; align-items:center; }}

.pill {{
    display:flex; align-items:center; gap:7px;
    background:rgba(45,139,139,0.08);
    border:1px solid rgba(45,139,139,0.18);
    border-radius:99px; padding:5px 13px;
    font-size:0.73rem; color:#a8dadc; white-space:nowrap;
}}

.dot {{
    width:6px; height:6px; border-radius:50%; background:#2d8b8b; flex-shrink:0;
    animation: breathe 2.6s ease-in-out infinite;
}}

@keyframes breathe {{
    0%,100% {{ opacity:1; box-shadow:0 0 0 0 rgba(45,139,139,0.45); }}
    50%      {{ opacity:0.6; box-shadow:0 0 0 5px rgba(45,139,139,0); }}
}}

/* ── SECTION LABEL ── */
.sec-lbl {{
    font-size:0.68rem; font-weight:600;
    letter-spacing:2.2px; color:#2d8b8b;
    text-transform:uppercase; margin-bottom:14px;
}}

/* ── WEATHER CARDS ── */
.grid {{
    display:grid;
    grid-template-columns: repeat(auto-fill, minmax(265px, 1fr));
    gap:16px; margin-bottom:36px;
}}

.card {{
    background: rgba(22,39,58,0.68);
    border: 1px solid rgba(45,139,139,0.14);
    border-radius:18px; padding:22px;
    position:relative; overflow:hidden;
    backdrop-filter:blur(8px);
    transition: transform 0.24s ease, box-shadow 0.24s ease, border-color 0.24s ease;
    cursor:default;
}}

.card-top-bar {{
    position:absolute; top:0; left:0; right:0; height:2px;
    background: linear-gradient(90deg, #2d8b8b, rgba(168,218,220,0.4), transparent);
    opacity:0; transition:opacity 0.24s;
}}

.card-glow {{
    position:absolute; inset:-1px;
    border-radius:18px;
    box-shadow: inset 0 0 0 1px rgba(168,218,220,0);
    transition: box-shadow 0.24s;
    pointer-events:none;
}}

.card:hover {{ transform:translateY(-5px); border-color:rgba(168,218,220,0.28); box-shadow:0 14px 44px rgba(0,0,0,0.45), 0 0 0 1px rgba(45,139,139,0.10); }}
.card:hover .card-top-bar {{ opacity:1; }}

.card-watermark {{
    position:absolute; right:14px; top:12px;
    font-size:3.8rem; opacity:0.055; line-height:1; user-select:none; pointer-events:none;
}}

.card-header {{ display:flex; justify-content:space-between; align-items:flex-start; gap:8px; margin-bottom:14px; }}

.city-name {{
    font-family:'Poppins',sans-serif;
    font-size:1.05rem; font-weight:600; color:#f1faee; line-height:1.3;
}}

.badge {{
    font-size:0.65rem; font-weight:500; color:#a8dadc;
    background:rgba(45,139,139,0.12); border:1px solid rgba(45,139,139,0.22);
    border-radius:99px; padding:3px 9px; white-space:nowrap; flex-shrink:0;
    text-transform:capitalize;
}}

.temp-row {{ margin:2px 0 14px; line-height:1; }}

.temp {{
    font-family:'Poppins',sans-serif;
    font-size:3rem; font-weight:700; color:#f1faee;
}}

.temp-unit {{ font-size:1.25rem; font-weight:400; color:rgba(168,218,220,0.7); }}

.divider {{
    height:1px;
    background: linear-gradient(90deg, rgba(45,139,139,0.28), rgba(45,139,139,0.05), transparent);
    margin:12px 0;
}}

.metric {{ display:flex; justify-content:space-between; align-items:center; padding:5px 0; }}

.lbl {{ font-size:0.74rem; color:rgba(241,250,238,0.38); display:flex; align-items:center; gap:5px; }}

.val {{ font-size:0.82rem; font-weight:500; color:#f1faee; }}

/* ── OVERVIEW STATS ── */
.overview-section {{ margin-bottom:36px; }}

.overview-label {{
    font-size:0.68rem; font-weight:600;
    letter-spacing:2.2px; color:#2d8b8b;
    text-transform:uppercase; margin-bottom:14px;
}}

.overview-grid {{
    display:grid;
    grid-template-columns: repeat(auto-fill, minmax(185px,1fr));
    gap:13px;
}}

.overview-card {{
    background:rgba(22,39,58,0.68);
    border:1px solid rgba(45,139,139,0.13);
    border-radius:14px; padding:16px 18px;
    display:flex; align-items:center; gap:14px;
    transition: border-color 0.22s, box-shadow 0.22s;
}}

.overview-card:hover {{
    border-color:rgba(45,139,139,0.32);
    box-shadow:0 4px 20px rgba(0,0,0,0.3);
}}

.ov-icon {{ font-size:1.7rem; line-height:1; flex-shrink:0; }}

.ov-val {{
    font-family:'Poppins',sans-serif;
    font-size:1.5rem; font-weight:700; color:#f1faee; line-height:1;
}}

.ov-city {{ font-size:0.75rem; color:rgba(168,218,220,0.65); margin:3px 0 2px; }}

.ov-tag {{
    font-size:0.62rem; font-weight:600;
    letter-spacing:1.2px; color:#2d8b8b;
    text-transform:uppercase;
}}

/* ── FOOTER ── */
.footer {{
    border-top:1px solid rgba(45,139,139,0.12);
    padding:20px 0; margin-top:8px;
    display:flex; justify-content:space-between;
    align-items:center; flex-wrap:wrap; gap:8px;
}}

.footer-l {{ font-size:0.73rem; color:rgba(241,250,238,0.28); }}
.footer-r {{ font-size:0.73rem; color:rgba(45,139,139,0.55); }}

.error-notice {{
    background:rgba(220,53,69,0.07);
    border:1px solid rgba(220,53,69,0.28);
    border-radius:12px; padding:14px 18px;
    color:#e57373; font-size:0.85rem; margin-bottom:18px;
}}
</style>
</head>
<body>
<div class="mesh"></div>
<div class="wrap">

    <div class="hdr">
        <div class="brand">
            <div class="brand-logo">🌊</div>
            <div>
                <div class="brand-title">WeatherDepths</div>
                <div class="brand-sub">Global Weather Intelligence</div>
            </div>
        </div>
        <div class="pills">
            <div class="pill"><div class="dot"></div>System Online</div>
            <div class="pill"><div class="dot"></div>API Active</div>
            <div class="pill" id="timePill">--:--:--</div>
        </div>
    </div>

    {error_html}

    <p class="sec-lbl">Live Conditions &mdash; {n} location{"s" if n != 1 else ""}</p>
    <div class="grid">{cards_html}</div>

    {analysis_html}

    <div class="footer">
        <span class="footer-l">WeatherDepths &nbsp;&middot;&nbsp; Powered by OpenWeatherMap</span>
        <span class="footer-r" id="footerTime"></span>
    </div>

</div>
<script>
function tick() {{
    const now = new Date();
    const t = now.toLocaleTimeString('en-US', {{hour12:false}});
    const d = now.toLocaleDateString('en-US', {{month:'short', day:'numeric', year:'numeric'}});
    const p = document.getElementById('timePill');
    if (p) p.textContent = t;
    const f = document.getElementById('footerTime');
    if (f) f.textContent = 'Updated ' + d + ' ' + t;
}}
setInterval(tick, 1000);
tick();
</script>
</body>
</html>"""

components.html(html_code, height=1080, scrolling=True)

# ── HISTORICAL ANALYSIS ───────────────────────────────────────────────────────

st.markdown("""
<style>
    .section-hdr {{
        border-left: 3px solid #2d8b8b;
        padding: 12px 18px;
        margin: 12px 0 22px 0;
        background: rgba(22,39,58,0.45);
        border-radius: 0 10px 10px 0;
    }}
    .section-hdr h3 {{
        font-family: 'Poppins', sans-serif;
        font-size: 1.05rem; font-weight: 600; color: #f1faee; margin: 0 0 3px 0;
    }}
    .section-hdr p {{
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem; color: rgba(168,218,220,0.45); margin: 0;
    }}
    .err-notice {{
        background: rgba(220,53,69,0.07);
        border: 1px solid rgba(220,53,69,0.28);
        border-radius: 10px; padding: 12px 16px;
        color: #e57373; font-family: 'Inter', sans-serif; font-size: 0.85rem;
    }}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="section-hdr">
    <h3>Historical Data Analysis</h3>
    <p>Source: Open-Meteo ERA5 archive &nbsp;·&nbsp; ~5-day processing delay</p>
</div>
""", unsafe_allow_html=True)

TIME_OPTIONS = {
    "7D": ("Last 7 days",    7),
    "1M": ("Last 30 days",  30),
    "6M": ("Last 6 months", 180),
    "1Y": ("Last year",     365),
}

selected_key = st.selectbox(
    "Time range",
    options=list(TIME_OPTIONS.keys()),
    format_func=lambda k: TIME_OPTIONS[k][0],
    key="hist_range",
)
hist_days = TIME_OPTIONS[selected_key][1]
hist_city = city_input.strip() if city_input.strip() else "Ho Chi Minh City"


@st.cache_data(ttl=3600)
def cached_historical(city, days):
    return get_historical_weather(city, days)


with st.spinner(f"Loading historical data for {hist_city}..."):
    hist_data = cached_historical(hist_city, hist_days)

if not hist_data:
    st.markdown(
        '<div class="err-notice">⚠️ Could not load historical data — verify the city name or check your connection.</div>',
        unsafe_allow_html=True,
    )
else:
    df = pd.DataFrame({
        "date":          pd.to_datetime(hist_data["dates"]),
        "temp_max":      hist_data["temp_max"],
        "temp_min":      hist_data["temp_min"],
        "temp_mean":     hist_data["temp_mean"],
        "precipitation": hist_data["precipitation"],
        "wind_max":      hist_data["wind_max"],
    })

    # Ocean Depths chart theme
    def _style(fig, title):
        fig.update_layout(
            plot_bgcolor="#0b1825",
            paper_bgcolor="#0f1e2e",
            font=dict(family="Inter, sans-serif", color="#f1faee"),
            title=dict(
                text=title,
                font=dict(size=12, color="rgba(168,218,220,0.75)", family="Poppins, sans-serif"),
                x=0.01,
            ),
            xaxis=dict(
                gridcolor="rgba(45,139,139,0.10)", color="rgba(241,250,238,0.4)",
                showline=True, linecolor="rgba(45,139,139,0.22)",
                tickfont=dict(size=10, color="rgba(241,250,238,0.45)"),
                zeroline=False,
            ),
            yaxis=dict(
                gridcolor="rgba(45,139,139,0.10)", color="rgba(241,250,238,0.4)",
                showline=True, linecolor="rgba(45,139,139,0.22)",
                tickfont=dict(size=10, color="rgba(241,250,238,0.45)"),
                zeroline=False,
            ),
            legend=dict(
                bgcolor="rgba(11,24,37,0.85)", bordercolor="rgba(45,139,139,0.25)",
                borderwidth=1, font=dict(color="rgba(241,250,238,0.65)"),
                orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
            ),
            margin=dict(l=8, r=8, t=56, b=8),
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor="rgba(11,24,37,0.96)", bordercolor="rgba(45,139,139,0.45)",
                font=dict(color="#f1faee", family="Inter, sans-serif", size=11),
            ),
        )
        return fig

    # Chart 1 — Temperature trend
    fig_temp = _style(go.Figure(), f"Temperature Trend — {hist_data['city']} (°C)")
    fig_temp.add_trace(go.Scatter(
        x=df["date"], y=df["temp_max"], name="Max",
        mode="lines", line=dict(color="#f4845f", width=2),
        hovertemplate="%{y:.1f}°C",
    ))
    fig_temp.add_trace(go.Scatter(
        x=df["date"], y=df["temp_min"], name="Min",
        mode="lines", line=dict(color="#a8dadc", width=2),
        fill="tonexty", fillcolor="rgba(45,139,139,0.08)",
        hovertemplate="%{y:.1f}°C",
    ))
    fig_temp.add_trace(go.Scatter(
        x=df["date"], y=df["temp_mean"], name="Mean",
        mode="lines", line=dict(color="#2d8b8b", width=2.5, dash="dot"),
        hovertemplate="%{y:.1f}°C",
    ))
    st.plotly_chart(fig_temp, use_container_width=True)

    col1, col2 = st.columns(2)

    # Chart 2 — Precipitation
    with col1:
        fig_rain = _style(go.Figure(), "Daily Precipitation (mm)")
        fig_rain.add_trace(go.Bar(
            x=df["date"], y=df["precipitation"], name="Rain",
            marker_color="rgba(45,139,139,0.6)",
            marker_line=dict(color="#2d8b8b", width=1),
            hovertemplate="%{y:.1f} mm",
        ))
        st.plotly_chart(fig_rain, use_container_width=True)

    # Chart 3 — Wind speed
    with col2:
        fig_wind = _style(go.Figure(), "Max Wind Speed (km/h)")
        fig_wind.add_trace(go.Scatter(
            x=df["date"], y=df["wind_max"], name="Wind Max",
            mode="lines", line=dict(color="#7ec8e3", width=2),
            fill="tozeroy", fillcolor="rgba(126,200,227,0.07)",
            hovertemplate="%{y:.1f} km/h",
        ))
        st.plotly_chart(fig_wind, use_container_width=True)

    # Chart 4 — Monthly averages (30+ day ranges only)
    if hist_days >= 30:
        df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()
        monthly = df.groupby("month").agg(
            avg_max=("temp_max", "mean"),
            avg_mean=("temp_mean", "mean"),
            avg_min=("temp_min", "mean"),
        ).reset_index()

        fig_monthly = _style(go.Figure(), "Monthly Temperature Averages (°C)")
        for col_key, label, color in [
            ("avg_max",  "Avg Max",  "rgba(244,132,95,0.72)"),
            ("avg_mean", "Avg Mean", "rgba(45,139,139,0.72)"),
            ("avg_min",  "Avg Min",  "rgba(168,218,220,0.72)"),
        ]:
            fig_monthly.add_trace(go.Bar(
                x=monthly["month"], y=monthly[col_key],
                name=label, marker_color=color,
                hovertemplate="%{y:.1f}°C",
            ))
        fig_monthly.update_layout(barmode="group")
        st.plotly_chart(fig_monthly, use_container_width=True)

# WeatherDepths

A real-time weather intelligence dashboard built with Streamlit. Monitor live conditions across multiple cities, explore historical climate trends with interactive charts, and receive automated daily email reports.

![Ocean Depths Theme](https://img.shields.io/badge/theme-Ocean%20Depths-2d8b8b?style=flat-square)
![Python](https://img.shields.io/badge/python-3.11+-1a2332?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/streamlit-1.56-a8dadc?style=flat-square)

---

## Features

**Live Dashboard**
- Real-time weather for up to 5 cities simultaneously (or search any city)
- Temperature, humidity, wind speed, pressure, and feels-like data
- Global overview cards — hottest, coldest, most humid, windiest

**Historical Analysis**
- Selectable time ranges: 7 days, 30 days, 6 months, 1 year
- Temperature trend chart (daily max / min / mean with shaded range)
- Daily precipitation bar chart
- Max wind speed area chart
- Monthly temperature averages (30+ day ranges)
- Powered by the free Open-Meteo ERA5 archive — no extra API key needed

**Email Notifications**
- Formatted daily weather reports via Gmail SMTP
- Automated scheduling via GitHub Actions (runs 8:00 AM Vietnam time)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Dashboard UI | Streamlit + Plotly + custom HTML/CSS |
| Current weather | OpenWeatherMap API |
| Historical data | Open-Meteo ERA5 archive (free, no key) |
| Email delivery | Gmail SMTP |
| Automation | GitHub Actions |
| Environment config | python-dotenv |

---

## Getting Started

### 1. Clone and set up

```bash
git clone https://github.com/jacksontran2806-png/weather-bot.git
cd weather-bot
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```
OPENWEATHER_API_KEY=your_openweathermap_api_key
EMAIL_PASSWORD=your_gmail_app_password
```

Get a free OpenWeatherMap API key at [openweathermap.org](https://openweathermap.org/api).
For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833) (not your account password).

### 3. Run the dashboard

```bash
streamlit run dashboard.py
```

Opens at `http://localhost:8501`. Type any city in the search box or browse the default five.

### 4. Run the email notifier manually

```bash
python main.py "Ho Chi Minh City"
python main.py London
python main.py Tokyo
```

---

## Project Structure

```
weather-bot/
├── dashboard.py      # Streamlit dashboard (main UI)
├── historical.py     # Open-Meteo historical data fetching
├── weather.py        # OpenWeatherMap API client
├── main.py           # CLI email report runner
├── notifier.py       # Gmail SMTP helper
├── config.py         # Loads .env variables
├── requirements.txt
└── .github/
    └── workflows/
        └── daily-weather.yml   # GitHub Actions cron job
```

---

## Automated Scheduling

The email bot runs daily at 8:00 AM Vietnam time via GitHub Actions.

To trigger it manually:
1. Go to the **Actions** tab on GitHub
2. Select **Daily Weather Report**
3. Click **Run workflow**

---

## Author

**Jackson Tran** — Aspiring Cloud & AI Engineer, Vietnam → Australia

[GitHub](https://github.com/jacksontran2806-png)

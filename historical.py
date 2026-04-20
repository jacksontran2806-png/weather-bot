import requests
from datetime import datetime, timedelta


def get_coordinates(city):
    try:
        resp = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "language": "en", "format": "json"},
            timeout=10,
        )
        resp.raise_for_status()
        results = resp.json().get("results", [])
        if not results:
            return None
        r = results[0]
        return {"lat": r["latitude"], "lon": r["longitude"], "name": r["name"]}
    except Exception:
        return None


def get_historical_weather(city, days=7):
    coords = get_coordinates(city)
    if not coords:
        return None

    end_date = datetime.now() - timedelta(days=5)
    start_date = end_date - timedelta(days=days - 1)

    try:
        resp = requests.get(
            "https://archive-api.open-meteo.com/v1/archive",
            params={
                "latitude": coords["lat"],
                "longitude": coords["lon"],
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "daily": "temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum,windspeed_10m_max",
                "timezone": "UTC",
            },
            timeout=15,
        )
        resp.raise_for_status()
        daily = resp.json().get("daily", {})
        return {
            "city": coords["name"],
            "dates": daily.get("time", []),
            "temp_max": daily.get("temperature_2m_max", []),
            "temp_min": daily.get("temperature_2m_min", []),
            "temp_mean": daily.get("temperature_2m_mean", []),
            "precipitation": daily.get("precipitation_sum", []),
            "wind_max": daily.get("windspeed_10m_max", []),
        }
    except Exception:
        return None

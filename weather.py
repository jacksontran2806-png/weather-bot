import requests
from config import OPENWEATHER_API_KEY

def get_weather(city):
    """Fetch current weather for a city"""
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            print(f"Error: City '{city}' not found")
        elif response.status_code == 401:
            print("Error: Invalid API key")
        else:
            print(f"Error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return None

if __name__ == "__main__":
    import sys
    
    # Get city from command line, or default to HCMC
    if len(sys.argv) > 1:
        city = " ".join(sys.argv[1:])  # Handles "New York" as two args
    else:
        city = "Ho Chi Minh City"
    
    print(f"Fetching weather for {city}...\n")
    
    data = get_weather(city)
    
    if data:
        city_name = data["name"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        
        print(f"Weather in {city_name}:")
        print(f"Temperature: {temp}°C (feels like {feels_like}°C)")
        print(f"Conditions: {description}")
        print(f"Humidity: {humidity}%")
    else:
        print("Could not fetch weather data")
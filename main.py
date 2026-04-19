from weather import get_weather
from notifier import send_email
import sys

def format_weather_report(data):
    """Format weather data into a readable email"""
    city = data["name"]
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    description = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    
    report = f"""
Weather Report for {city}
{'=' * 40}

Temperature: {temp}°C (feels like {feels_like}°C)
Conditions: {description.capitalize()}
Humidity: {humidity}%
Wind Speed: {wind_speed} m/s

Have a great day!
"""
    return report

def main():
    # Get city from command line or use default
    if len(sys.argv) > 1:
        city = " ".join(sys.argv[1:])
    else:
        city = "Ho Chi Minh City"
    
    print(f"Fetching weather for {city}...")
    
    # Fetch weather
    data = get_weather(city)
    
    if not data:
        print("Failed to fetch weather. No email sent.")
        return
    
    # Format report
    report = format_weather_report(data)
    print("\n" + report)
    
    # Send email
    send_email(
        subject=f"Weather Report: {data['name']}",
        body=report,
        to_email="YOUR_GMAIL@gmail.com"  # ← Replace with your email
    )

if __name__ == "__main__":
    main()
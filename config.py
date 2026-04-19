import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Validate that keys exist
if not OPENWEATHER_API_KEY:
    raise ValueError("OPENWEATHER_API_KEY not found in .env file")
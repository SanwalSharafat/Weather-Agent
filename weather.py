import requests, os
from dotenv import load_dotenv
load_dotenv ()
API_KEY = os.getenv("API_KEY")

# -----------------------------------------------------
# WEATHER TOOL FUNCTION
# -----------------------------------------------------
def get_current_weather(location: str) -> dict:
    """Returns the current weather for a specific location using the OpenWeatherMap API."""
    url = "http://api.openweathermap.org/data/2.5/weather"

    if not API_KEY:
        return {"error": "Weather API key not found. Please set API_KEY in .env."}

    try:
        params = {
            "q": location,
            "appid": API_KEY,
            "units": "metric"
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        return {
            "location": data["name"],
            "temperature_celsius": data["main"]["temp"],
            "conditions": data["weather"][0]["description"].capitalize(),
            "humidity_percent": data["main"]["humidity"],
        }

    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": f"City '{location}' not found. (Status 404)"}
        return {"error": f"HTTP error occurred: {e}"}

    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {e}"}

    except KeyError as e:
        return {"error": f"Error parsing weather data: Missing key {e}. Response: {data}"}

from datetime import datetime, timezone
import requests
from fastapi import HTTPException
from core.config import WeatherConfig
from typing import Optional

# ---------------------------------------------------------------- Reuseable functions ----------------------------------------------------------------

def convert_temp(value: float, unit: str) -> float:
    if not isinstance(value, (int, float)) or unit not in ["celsius", "fahrenheit", "kelvin"]:
        return "N/A"
    elif unit == "celsius":
        result = value - 273.15
        return round(result, 2)
    elif unit == "fahrenheit":
        result = (value - 273.15) * 9/5 + 32
        return round(result, 2)
    elif unit == "kelvin":
        return round(value, 2)
    
def convert_wind_speed(value: float) -> dict:
    if not isinstance(value, (int, float)):
        return "N/A"
    result = {
        "metric": {
            "km/h": round(value * 3.6, 2),
            "m/s": round(value, 2),
        },
        "imperial":{
            "mp/h": round(value * 2.237, 2),
            "f/s": round(value * 3.281, 2)
        },
        "knots": round(value * 1.944)
    }
    return result

def convert_to_date(value: int, shift: int) -> str:
    if not isinstance(value, int) or not isinstance(shift, int):
        return "N/A"
    timestamp = value + shift
    dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def get_weather_data(city: str, lang: Optional[str] = "en") -> requests.Response:
    response: requests.Response = requests.get(url=WeatherConfig.WEATHER_API_URL, params={"q": city, "lang": lang})
    if response.status_code == 404:
        raise HTTPException(detail={"error": f"{city} was not found"}, status_code=404)
    if response.status_code == 200:
        return response.json()
    

# ---------------------------------------------------------------- Functions for the API ------------------------------------------------------------

def get_general_weather(city: str, lang: str) -> dict:
    res_json = get_weather_data(city, lang)
    weather = {
        "city": res_json["name"],
        "coord":{
            "lon":res_json["coord"]["lon"],
            "lat":res_json["coord"]["lat"]
        },
        "description":res_json["weather"][0]["description"],
        "temperature":{
            "celsius":{
                "temp":convert_temp(res_json["main"]["temp"], "celsius"),
                "feels_like":convert_temp(res_json["main"]["feels_like"], "celsius"),
                "daily_min":convert_temp(res_json["main"]["temp_min"], "celsius"),
                "daily_max":convert_temp(res_json["main"]["temp_max"], "celsius"),
            },
            "fahrenheit":{
                "temp":convert_temp(res_json["main"]["temp"], "fahrenheit"),
                "feels_like":convert_temp(res_json["main"]["feels_like"], "fahrenheit"),
                "daily_min":convert_temp(res_json["main"]["temp_min"], "fahrenheit"),
                "daily_max":convert_temp(res_json["main"]["temp_max"], "fahrenheit"),
            },
            "kelvin":{
                "temp":convert_temp(res_json["main"]["temp"], "kelvin"),
                "feels_like":convert_temp(res_json["main"]["feels_like"], "kelvin"),
                "daily_min":convert_temp(res_json["main"]["temp_min"], "kelvin"),
                "daily_max":convert_temp(res_json["main"]["temp_max"], "kelvin"),
            }
        },
        "pressure":res_json["main"]["pressure"],
        "humidity":res_json["main"]["humidity"],
        "wind":{
            "direction": res_json["wind"]["deg"],
            "speed": convert_wind_speed(res_json["wind"]["speed"])
        },
        "cloud_percentage": res_json["clouds"]["all"],
        "sunrise": convert_to_date(res_json["sys"]["sunrise"], res_json["timezone"]),
        "sunset": convert_to_date(res_json["sys"]["sunset"], res_json["timezone"])
    }
    return weather

def get_current_temp(city: str, unit: str) -> dict[str, float]:
    response = requests.get(f"{WeatherConfig.WEATHER_API_URL}&q={city}")
    if response.status_code == 404:
        raise HTTPException(detail={"error": f"{city} was not found"}, status_code=404)
    if response.status_code == 200:
        res_json = response.json()
        return {"current temperature":convert_temp(res_json["main"]["temp"], unit)}
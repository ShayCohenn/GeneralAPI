import requests
import datetime
from constants import WEATHER_API_URL

# ---------------------------------------------------------------- Reuseable functions ----------------------------------------------------------------

def convert_temp(value: float, unit: str) -> float:
    if not isinstance(value, (int, float)):
        return "Error: an error occurred"
    if unit not in ["celsius", "fahrenheit", "kelvin"]:
        return "Error: Unit must be celsius, fahrenheit or kelvin"
    elif unit == "celsius":
        result = value - 273.15
        return round(result, 2)
    elif unit == "fahrenheit":
        result = (value - 273.15) * 9/5 + 32
        return round(result, 2)
    elif unit == "kelvin":
        return round(value, 2)
    
def convert_wind_speed(value: float) -> float:
    if not isinstance(value, (int, float)):
        return "Error: an error occurred"
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

def convert_to_date(value: int, shift: int):
    if not isinstance(value, int) or not isinstance(shift, int):
        return "Error: an error occurred"
    timestamp = value + shift
    dt = datetime.datetime.utcfromtimestamp(timestamp)
    return dt.strftime("%Y-%m-%d %H:%M:%S")

# ---------------------------------------------------------------- Functions for the API ------------------------------------------------------------

def get_general_weather(city: str, lang: str):
    response = requests.get(f"{WEATHER_API_URL}&q={city}&lang={lang}")
    if response.status_code == 200:
        res_json = response.json()
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
    elif response.status_code == 404:
        return "404"
    else:
        return None

def get_current_temp(city: str, unit: str):
    response = requests.get(f"{WEATHER_API_URL}&q={city}")
    if response.status_code == 200:
        res_json = response.json()
        return {"current temperature":convert_temp(res_json["main"]["temp"], unit)}
    elif response.status_code == 404:
        return "404"
    else:
        raise None
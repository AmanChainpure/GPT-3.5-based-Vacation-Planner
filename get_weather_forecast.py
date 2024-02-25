import requests
from dotenv import load_dotenv
import os

load_dotenv()
weather_api_key = 'ab9c60a2fe5747d0805104048231205'


def weather_forecast(location):
    weather_url = f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={location}"

    try:
        response = requests.get(weather_url)
        data = response.json()

        if response.status_code == 200:
            # Extract relevant weather information from the response
            temperature = data["current"]["temp_c"]
            humidity = data["current"]["humidity"]
            wind_speed = data["current"]["wind_kph"]
            condition = data["current"]["condition"]["text"]

            # Print the weather information
            print("Location:", location)
            print("Temperature (°C):", temperature)
            print("Humidity (%):", humidity)
            print("Wind Speed (kph):", wind_speed)
            print("Condition:", condition)

            result = f'Weather in {location} is {condition}, temperature is {temperature} °C, humidity is {humidity} % and wind speed will be {wind_speed} kph'
            return result


        else:
            return "Error occurred while fetching weather data."

    except requests.exceptions.RequestException as e:
        print("Error occurred:", e)
        return None


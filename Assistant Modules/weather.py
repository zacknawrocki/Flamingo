import requests
import json



class Weather:
    def __init__(self, city=None, unit=None, api_key=None):
        self.city = city
        self.unit = unit
        self.api_key = api_key

    def set_city(self, city):
        # Get city code from http://bulk.openweathermap.org/sample/
        # or use the search bar at https://openweathermap.org/
        self.city = city

    def set_unit(self, unit):
        # unit = "imperial" or "metric"
        self.unit = unit

    def set_api_key(self, api_key):
        # create an api key at https://openweathermap.org/api
        self.api_key = api_key

    def get_current_weather_response(self):
        weather_url = "https://api.openweathermap.org/data/2.5/weather?"

        try:
            weather_url = weather_url + "id=" + self.city + "&appid=" + self.api_key + "&units=" + self.unit
        except:
            weather_response = "In order to get the weather, you must first set up your weather settings. "
            weather_response += "You can do this by visiting [insert link] on your local network."
            return weather_response

        response = requests.get(weather_url)

        if response.status_code == 200:
            data = response.json()

            weather = data['main']
            temperature, feels_like = weather['temp'], weather['feels_like']
            humidity, pressure = weather['humidity'], weather['pressure']
            location = data['name']
            report = data['weather'][0]['description']

            weather_response = f"It is {temperature} degrees in {location} "
            weather_response += f"and feels like {feels_like} degrees, with {report}, "
            weather_response += f"a humidity of {humidity}, and a pressure of {pressure}."

            return weather_response

        else:
            return "Sorry, I am unable to get weather at this time."

    def get_daily_forecast(self):
        pass

    def get_weekly_forecast(self):
        pass



w = Weather()
current_weather = w.get_current_weather_response()

print(current_weather)


#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import requests

OPENWEATHER_API_KEY = '2b2733ed41dea074206cea549f53e0a6'


def time_until_playable(court_data):

    
    court_surface_area = court_data['surface_area']
    drainage_rate = court_data['drainage_rate']

    # Get weather data for Copenhagen
    weather_data = get_weather_data()
    rain_intensity = calculate_rain_intensity(weather_data)
    humidity = calculate_humidity(weather_data)
    pressure = calculate_pressure(weather_data)
    temperature = calculate_temperature(weather_data)
    sunlight = calculate_sunlight(weather_data)
    wind = calculate_wind(weather_data)
    
    # Calculate the time it will take for the court to drain
    water_volume = rain_intensity * court_surface_area
    drainage_time = water_volume / drainage_rate
    
    # Adjust the drainage time based on other weather parameters
    if humidity > 75:
        drainage_time *= 1.2
    if pressure < 990:
        drainage_time *= 1.1
    if temperature < 10:
        drainage_time *= 1.3
    if sunlight < 3:
        drainage_time *= 1.2
    if wind < 5:
        drainage_time*= 1.3
    
    return drainage_time   

court_data = {
    'surface_area': 679.353656,  # in square meters
    'drainage_rate': 5,    # in liters per minute per square meter
    'court_slope': 1.00   # in gradient that the court slopes
}

def get_weather_data():
    url = 'https://api.openweathermap.org/data/2.5/weather?q=Copenhagen&appid=' + '2b2733ed41dea074206cea549f53e0a6'

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

weather_data = get_weather_data()    
    
if weather_data is not None:
    # Do something with the weather data
    print(weather_data)
else:
    print("Failed to fetch weather data.")
    
    
def calculate_pressure(weather_data):
    if weather_data is None:
        # Return a default value if we couldn't retrieve weather data
        return 1013.25
    
    # Get the pressure from the weather data (in hPa)
    if 'main' in weather_data:
        if 'pressure' in weather_data['main']:
            pressure = weather_data['main']['pressure']
    
    return pressure

def calculate_rain_intensity(weather_data):
    if weather_data is None:
        # Return a default value if we couldn't retrieve weather data
        return 0
    
    # Get the rain intensity from the weather data (in millimeters per hour)
    rain_intensity = 0
    if 'rain' in weather_data:
        if '1h' in weather_data['rain']:
            rain_intensity = weather_data['rain']['1h']
    
    # Convert the rain intensity to liters per minute per square meter
    return (rain_intensity / 1000) * 60

def calculate_humidity(weather_data):
    if weather_data is None:
        # Return a default value if we couldn't retrieve weather data
        return 0
    
    # Get the humidity from the weather data (as a percentage)
    humidity = 0
    if 'main' in weather_data:
        if 'humidity' in weather_data['main']:
            humidity = weather_data['main']['humidity']
    
    return humidity

def calculate_pressure(weather_data):
    if weather_data is None:
        # Return a default value if we couldn't retrieve weather data
        return 1013.25
    
    # Get the pressure from the weather data (in hPa)
    pressure = 0
    if 'main' in weather_data:
        if 'pressure' in weather_data['main']:
            pressure = weather_data['main']['pressure']
    
    return pressure

def calculate_temperature(weather_data):
    if weather_data is None:
        # Return a default value if we couldn't retrieve weather data
        return 15.0

    temperature = 15.0
    if 'main' in weather_data:
        if 'temp' in weather_data['main']:
            temperature = weather_data['main']['temp'] - 273.15

    return temperature
    
def calculate_wind(weather_data):
    if weather_data is None:
        return 0

    wind_speed = 0
    if 'wind' in weather_data:
        if 'speed' in weather_data['wind']:
            wind_speed = weather_data['wind']['speed']

    return wind_speed

def calculate_sunlight(weather_data):
    # Implement your logic here to calculate sunlight based on the weather data.
    # For this example, I'll return a default value of 5.
    return 5


drainage_time = time_until_playable(court_data)
print(f" - The tennis court will be playable in {drainage_time} minutes.")

#Determine how much rain is gonna make the courts not-playable. What is the least amount of rain that makes the court unplayable
    #Conditions that affect the drainage of the courts, which are not already in the program:
    #Shadows from trees and buildings, which will make the courts dry slower.
    #Questions: Which condition affect the draiange of the courts the most? Of course amount of rainfall, is the most important. If it is always raining
    #the courts can never get dry. Set boundaries, the calculation of how the courts are getting drained is not to be affected by human intervention.
    #How big of an impact does the sun have? How big of an impact does the temperature have? 
    #How much water have the courts recieved doing a longer period of time? How much water does the fundament below the tenniscourt contain?
    #How can you determine humidity, amount of water below the tenniscourt surface? Through a lot of weatherdata from the previous months?
    #This program should combine rasterdata and standard calculations to make a better estimate of the drainage
    #Reduce time spent in-field at tenniscourts to determine whether a court is wet or not, time-demanding, but fun though. 
    #Future ideas. Use weatherdata to calcuate when a tenniscourt will be playable tomorrow or not. Estimates so tennistrainers can plan their training accordingly.
    #Make an automation that make apicalls every 5 min when the courts are playable. And start making API calls every one minute and 26 seconds when the courts needs to dry.
    #Calculate the amount of water used in a regular watering off the court(when players water the court before playing) and add that to amount of water in the fundament. Get data from bookingsystem, and get an average of how often people is watering the court. Or get that data through a raspberry pi. 
    #


# In[ ]:





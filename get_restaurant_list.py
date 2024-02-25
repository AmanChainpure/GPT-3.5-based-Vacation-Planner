import requests
import os
from dotenv import load_dotenv

load_dotenv()
travel_advisor_api = 'd173665876msh828d2a003ee46f9p10f44djsn7b169a931475'


def get_cordinates(location):
    geocoding_url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json"
    response = requests.get(geocoding_url)
    data = response.json()
    if not data:
        print("Location not found.")
        return

    # Extract latitude and longitude from the geocoding response
    latitude = data[0]['lat']
    longitude = data[0]['lon']
    return latitude, longitude


def get_restaurants(location):
    lat, long = get_cordinates(location)
    print(lat, long)
    print(location)
    url = "https://travel-advisor.p.rapidapi.com/restaurants/list-by-latlng"
    querystring = {"latitude": lat, "longitude": long, "limit": "30", "currency": "INR", "distance": "2",
                   "open_now": "false", "lunit": "km", "lang": "en_US"}

    headers = {
        "X-RapidAPI-Key": travel_advisor_api,
        "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring, )
    data_gathered = response.json()['data']

    result = []
    if data_gathered:
        for i in data_gathered[:10]:
            if 'name' in i.keys() and 'address' in i.keys() and 'cuisine' in i.keys():
                result.append({'Name': i['name'],
                               'Address': i['address'],
                               'Cuisines': ','.join([j['name'] for j in i['cuisine']])})

        return result


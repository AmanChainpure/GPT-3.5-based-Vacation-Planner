from dotenv import load_dotenv
import os
import requests

load_dotenv()
trip_advisor_api_key = 'e4215e8ac9msh11edeed3de833dbp1db5e7jsnd45641ee14cc'


def search_hotels(location, checkin_date, checkout_date):
    # Geocode the location using OpenStreetMap Nominatim API
    geocoding_url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json"
    response = requests.get(geocoding_url)
    data = response.json()
    if not data:
        print("Location not found.")
        return

    # Extract latitude and longitude from the geocoding response
    latitude = data[0]['lat']
    longitude = data[0]['lon']

    print('Latitude:', latitude)
    print('Longitude', longitude)

    # Search for hotels using TripAdvisor API
    checkin = checkin_date
    checkout = checkout_date
    url = "https://tripadvisor16.p.rapidapi.com/api/v1/hotels/searchHotelsByLocation"

    querystring = {"latitude": latitude, "longitude": longitude, "checkIn": checkin, "checkOut": checkout,
                   "pageNumber": "1", "currencyCode": "INR"}

    headers = {
        "X-RapidAPI-Key": trip_advisor_api_key,
        "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()

    result = []

    if data:
        for i in response.json()['data']['data']:
            hotel_name = i['title']
            hotel_location = i['secondaryInfo']
            price = i['priceForDisplay']

            result.append({'Hotel Name': hotel_name, 'Location': hotel_location, 'Per Night Fare': price})
        # print('Hotel data:\n',result)
        return result
    else:
        return "No hotels found."

# Proper

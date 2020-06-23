#
# Simple Sun (Set) and (Rise)
# Sunset and Sunrise data based on the City
#
# Copyright (c) KvinTanaka. (MIT License)
# https://www.kvintanaka.com
#

import sys
import requests
from dateutil.parser import isoparse
from dateutil.tz import tzlocal


# --- Simple Sun Set And Rise - Main ---


def get_timedata(geodata):
    """Retrieve Sunset and Sunrise Time based on a coordinates.
    Geocode data is taken from sunrise-sunset.org.
    Author: KvinTanaka"""

    api = "https://api.sunrise-sunset.org/json?lat=" + geodata['latitude'] + "&lng=" + geodata[
        'longitude'] + "&date=today&formatted=1"
    response = requests.get(api)
    result = response.json()

    sunset_time = isoparse(result['results']['sunset'])  # Convert ISO 8601 format to Python Datetime
    sunrise_time = isoparse(result['results']['sunrise'])  # Convert ISO 8601 format to Python Datetime
    #Note: Timezone data from sunrise-sunset.org API is currently UTC only (+00:00)

    return {'sunset': sunset_time.astimezone(tzlocal()), 'sunrise': sunrise_time.astimezone(tzlocal())}

def get_coordinates(city):
    """Retrieve Coordinates data (Longitude and Latitude) of a city.
    Geocode data is taken from OpenStreetMap.org.
    Author: KvinTanaka"""

    api = "https://nominatim.openstreetmap.org/search?city=" + city + "&format=json"
    response = requests.get(api)
    result = response.json()

    if len(result) == 0:
        raise Exception('Location not found')
    else:
        lon = result[0]['lon']
        lat = result[0]['lat']
        country = result[0]['display_name'].split(', ')[-1]

    return {'longitude': lon, 'latitude': lat, 'country': country}


def main():
    """Start point"""

    if len(sys.argv) >= 2:
        city = ' '.join(sys.argv[1:])

        geodata = get_coordinates(city)
        timedata = get_timedata(geodata)

        print('Result for ' + city + ' [' + geodata['country'] + ']:')
        print('Sunrise: ' + timedata['sunrise'].strftime("%H:%M:%S"))
        print('Sunset: ' + timedata['sunset'].strftime("%H:%M:%S"))
    else:
        print("Invalid Argument: Please input a city name")


if __name__ == "__main__":
    main()

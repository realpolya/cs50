import os

import googlemaps
from cs50 import SQL
from geocoding import geocode, reverse_geocode

gmaps = googlemaps.Client(key='AIzaSyCVaQ94dl2C-c2z83rAKSmmEfU5Mg4e1p8')

# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
geo = geocode_result[0]
geo1 = geo.get('geometry')
geo2 = geo1.get('location')
lat = geo2.get('lat')
lng = geo2.get('lng')

print (lat, lng)

import csv
import datetime
import pytz
import requests
import urllib
import uuid
import re
import json

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code




def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/home")
        return f(*args, **kwargs)

    return decorated_function





# looks up the location – todo: this can be written so much better
# looks up the location
def lookup(address):
    """Connect to NYC Zola and LA Zimas (and other locations later too)"""

    #getting a more concise address
    orientation = ["South", "North", "East", "West", "S", "N", "W", "E"]
    broken_address = address.split()

    # address with sides of the world removed
    def sides(broken_address):
        nosides = []
        for word in broken_address:
            if word not in orientation:
                nosides.append(word)
        return(nosides)

    sideless = sides(broken_address)
    sideless_str = " ".join(sideless)

    # address with "th" removed
    thless = re.sub(r'(\d)th', r'\1', address)

    # address with both sides and "th" removed
    thlessSplit = thless.split()
    all_less = sides(thlessSplit)
    all_less_str = " ".join(all_less)

    # first try: NYC – Zola website
    nyc_url = "https://search-api-production.herokuapp.com/search?helpers[]=geosearch-v2&helpers[]=bbl&helpers[]=neighborhood&helpers[]=zoning-district&helpers[]=zoning-map-amendment&helpers[]=special-purpose-district&helpers[]=commercial-overlay&q=" + address

    response = requests.get(nyc_url)

    # need to control for cities within NY state better
    # to make sure that the address is indeed within NYC

    # checking if the address is in New York
    # if theere is an empty list, not in NYC
    if response.json() == []:
        print("This address is not in NYC")
    # checking if the address without orientation and "th" is in NYC
    elif all_less_str.upper() in response.text.upper() and "NY" in address:
        print("Address is found in NYC")
        print ("String without 'th' and sides matched")
        return {"authority":"New York City"}
    # checking if the address without "th" is in NYC
    elif thless.upper() in response.text.upper() and "NY" in address:
        print("Address is found in NYC")
        print ("String without 'th' matched")
        return {"authority":"New York City"}
    # checking if the address without the sides is in NYC
    elif sideless_str.upper() in response.text.upper() and "NY" in address:
        print("Address is found in NYC")
        print ("String without sides matched")
        return {"authority":"New York City"}
    # checking if the first 3 words of the original address is in NYC
    elif broken_address[0].upper() in response.text.upper() and broken_address[1].upper() in response.text.upper() and broken_address[2].upper() in response.text.upper() and "NY" in address:
        print("Address is found in NYC")
        print ("Normal strings matched")
        return {"authority":"New York City"}
    # if all failed, not in NYC
    else:
        print("Address NOT found in NYC")

    # second try: LA – Zimas
    if sideless[0].isdigit():
        number = sideless[0]

        street = sideless[1]

        la_url = f"https://zimas.lacity.org/ajaxSearchResults.aspx?search=address&HouseNumber={number}&StreetName={street}"
        response = requests.get(la_url)

        if "Images/warning_icon.png" in response.text:
            print("Address NOT found in LA")
        elif "Los Angeles" in address:
            print("Address found in Zimas LA")
            print(response.text)
            return {"authority":"The City of Los Angeles"}
        else:
            print("Address NOT found in LA")
    else:
        return {"authority":"None"}
    return {"authority":"None"}



# looks up the bbl of NYC location
def bbl_heroku(address):

    #getting a more concise address
    orientation = ["South", "North", "East", "West", "S", "N", "W", "E"]
    broken_address = address.split()

    # address with sides of the world removed
    def sides(broken_address):
        nosides = []
        for word in broken_address:
            if word not in orientation:
                nosides.append(word)
        return(nosides)

    sideless = sides(broken_address)
    sideless_str = " ".join(sideless)

    # address with "th" removed
    thless = re.sub(r'(\d)th', r'\1', address)

    # address with both sides and "th" removed
    thlessSplit = thless.split()
    all_less = sides(thlessSplit)
    all_less_str = " ".join(all_less)

    # get bbl from heroku
    nyc_url = "https://search-api-production.herokuapp.com/search?helpers[]=geosearch-v2&helpers[]=bbl&helpers[]=neighborhood&helpers[]=zoning-district&helpers[]=zoning-map-amendment&helpers[]=special-purpose-district&helpers[]=commercial-overlay&q=" + address

    response = requests.get(nyc_url)

    # checking if the address is in New York
    # if theere is an empty list, not in NYC
    if response.json() == []:
        print("This address is not in NYC")

    # converting JSON to list of dictionaries
    heroku_dict = json.loads(response.text)
    bbl = heroku_dict[0]["bbl"]

    return(bbl)

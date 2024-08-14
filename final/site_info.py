import requests
import re
from bs4 import BeautifulSoup
import json

from flask import redirect, render_template, request, session
from helpers import bbl_heroku


#this function allows user to look up parcel specs from ZIMAS
# LA City
def zimas_info(address):

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

    if sideless[0].isdigit():
        number = sideless[0]

    street = sideless[1]

    ajax_url = f"https://zimas.lacity.org/ajaxSearchResults.aspx?search=address&HouseNumber={number}&StreetName={street}"

    ajaxresponse = requests.get(ajax_url)

    match = re.search(r"ZimasData\.navigateDataToPin\('([^']*)', '([^']*)'\)", ajaxresponse.text)
    if match:
        first_string = match.group(1)
        second_string = match.group(2)

    pin = first_string
    reformat = second_string

    # now query ZIMAS and its HTML
    result_url = f"https://zimas.lacity.org/map.aspx?pin={pin}&ajax=yes&address={reformat}"

    response = requests.get(result_url)
    noback = response.text
    noslash = noback.replace("\\", "")
    soup = BeautifulSoup(noslash, 'html.parser')

    # trying to find these specs
    try:
        areacalc = soup.find('a', {'onclick':"getToolTip('areacalc.htm');"}).parent.find_next_sibling('td').text
    except AttributeError:
        areacalc = "NA"

    try:
        parcel = soup.find('a', {'onclick':"getToolTip('apn.htm');"}).parent.find_next_sibling('td').text
    except AttributeError:
        parcel = "NA"

    try:
        zoning = soup.find('a', {'onclick':"getToolTip('zoning.htm');"}).parent.find_next_sibling('td').text
    except AttributeError:
        zoning = "NA"

    try:
        year = soup.find('td', string=lambda x: x and "Year Built" in x).find_next_sibling('td').text
    except AttributeError:
        year = "NA"

    # now work with assessor's portal to extract width and length of the lot
    assessor_url = f"https://portal.assessor.lacounty.gov/api/parceldetail?ain={parcel}"

    # obtaining the response from assessor's portal
    assessresponse = requests.get(assessor_url)

    # checking if the parcel exists
    if assessresponse.text == '{"Parcel":null}':
        print("Parcel has been deleted or does not exist")
        land_width = "NA"
        land_depth = "NA"
    else:
        # parsing the HTML to find width and depth
        assessor = assessresponse.text

        # converting JSON to dictionary
        ass_dict = json.loads(assessor)

        # dissecting the new dictionary to find width and depth
        try:
            land_width = ass_dict['Parcel']['LandWidth']
        except KeyError:
            land_width = "NA"

        try:
            land_depth = ass_dict['Parcel']['LandDepth']
        except KeyError:
            land_depth = "NA"


    #create a dictionary sitespecs
    sitespecs = {
        'Area':areacalc,
        'Parcel':parcel,
        'Zoning':zoning,
        'Year':year,
        'Width':land_width,
        'Depth':land_depth,
        'Address':reformat
    }

    return(sitespecs)



# NY City
def zola_info(address):

    bbl = bbl_heroku(address)

    # insert bbl into the link
    zolaurl = f"https://planninglabs.carto.com/api/v2/sql?q=SELECT%20address,bbl,bldgarea,lot,lotarea,lotdepth,lotfront,yearbuilt,zonedist1,zonedist2,zonedist3,zonedist4,LOWER(zonemap)%20AS%20zonemap,%20%20%20%20/*%20id:1011710062%20*/%20%20%20%20st_x(st_centroid(the_geom))%20as%20lon,%20st_y(st_centroid(the_geom))%20as%20lat,%20%20%20%20the_geom,%20bbl%20AS%20id%20FROM%20dcp_mappluto%20WHERE%20bbl={bbl}&format=json"

    zola_response = requests.get(zolaurl)

    zola_dict = json.loads(zola_response.text)

    # obtaining specs from the zola query
    try:
        areacalc = zola_dict["rows"][0]["lotarea"]
    except KeyError:
        areacalc = "NA"

    try:
        zoning = zola_dict["rows"][0]["zonedist1"]
    except KeyError:
        zoning = "NA"

    try:
        year = zola_dict["rows"][0]["yearbuilt"]
    except KeyError:
        year = "NA"

    try:
        land_width = zola_dict["rows"][0]["lotfront"]
    except KeyError:
        land_width = "NA"

    try:
        land_depth = zola_dict["rows"][0]["lotdepth"]
    except KeyError:
        land_depth = "NA"

     #create a dictionary sitespecs
    sitespecs = {
        'Area':areacalc,
        'Parcel':bbl,
        'Zoning':zoning,
        'Year':year,
        'Width':land_width,
        'Depth':land_depth,
        'Address':address
    }

    return(sitespecs)


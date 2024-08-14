# this file is for testing ZIMAS in LA

import requests
import re
from bs4 import BeautifulSoup
from flask import Flask, request
import json

app = Flask(__name__)

# first reformat the address
# address = "5200 Wilshire Boulevard, Los Angeles, CA, USA"
# address = "325 West Adams Boulevard, Los Angeles, CA, USA"
# address = "888 South Hope Street, Los Angeles, CA, USA"
# address = "523 Gayley Avenue, Los Angeles, CA, USA"
# address = "631 Hauser Boulevard, Los Angeles, CA, USA"
# address = "600 Ridgeley Drive, Los Angeles, CA, USA"
address = "333 South Grand Avenue, Los Angeles, CA, USA"

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

#now query ZIMAS
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


print(areacalc)
print(parcel)
print(zoning)
print(year)

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

    print(land_width)
    print(land_depth)





# MISCELLANEOUS
# the search query on zimas leads to a javascript command that includes the full address and the map pin

# version with backslashes:
# <tr\>
#   <td class=\"DataCellsLeft\"\>
#       <a style='cursor: pointer;' onclick=\"getToolTip('areacalc.htm');\"\>Lot/Parcel Area (Calculated)&nbsp;</a\>
#   </td\>
#   <td class=\"DataCellsRight\" \>141,429.7 (sq ft)</td\>
# </tr\>

# version without backslashes
# <tr>
#   <td class="DataCellsLeft">
#       <a style='cursor: pointer;' onclick="getToolTip('areacalc.htm');">Lot/Parcel Area (Calculated)&nbsp;</a>
#   </td>
#   <td class="DataCellsRight" >141,429.7 (sq ft)</td>
# </tr>





# from assessor's map
# <dt uib-tooltip="The lot's width and depth.  For properties that are not square or rectangular, this is often a rough average of the width and depth.">Land W' x D':</dt>
# <dd class="ng-binding">355 x 165</dd>

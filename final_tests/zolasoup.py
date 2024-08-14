# this file is for testing Zola in NYC
import requests
import re
import json

# every address has a bbl number, it is then included in the url of zola page

# address = "101 West End Avenue, New York, NY, USA"
address = "250 West 19th Street, New York, NY, USA"
# address = "145 W 116th St, Los Angeles, CA, USA"
# address = "145 West 116th Street, Chicago, IL, USA"

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


bbl = bbl_heroku(address)

# insert bbl into the link
zolaurl = f"https://planninglabs.carto.com/api/v2/sql?q=SELECT%20address,bbl,bldgarea,lot,lotarea,lotdepth,lotfront,yearbuilt,zonedist1,zonedist2,zonedist3,zonedist4,LOWER(zonemap)%20AS%20zonemap,%20%20%20%20/*%20id:1011710062%20*/%20%20%20%20st_x(st_centroid(the_geom))%20as%20lon,%20st_y(st_centroid(the_geom))%20as%20lat,%20%20%20%20the_geom,%20bbl%20AS%20id%20FROM%20dcp_mappluto%20WHERE%20bbl={bbl}&format=json"

zola_response = requests.get(zolaurl)

zola_dict = json.loads(zola_response.text)

# obtaining specs from the zola query
try:
    area = zola_dict["rows"][0]["lotarea"]
except KeyError:
    area = "NA"

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

print(area)
print(bbl)
print(zoning)
print(year)
print(land_width)
print(land_depth)

# MISCELLANEOUS
# 1011710062 becomes 1/1171/62
# Manhattan (Borough 1) | Block 1171 | Lot 62

# in HTML parser section class="lot-details"
# div class="data-grid"
# Lot Area
# Year Built
# Parcel is BBL (Borough-Block-Lot)

# <div class="data-grid">
#      <label class="data-label">
#       Lot Area
#      </label>
#      <span class="datum">
#          27,437 sq ft
#      </span>
#    </div>

# Zoning
#   <a target="_blank" href="https://www1.nyc.gov/site/planning/zoning/districts-tools/c4.page" class="button" rel="noopener noreferrer">
#   C4-7
#       </a>

# insert bbl number into the following url
# bbl_url = "https://zola.planning.nyc.gov/l/lot/1/1171/62?search=true#17.15/40.775145/-73.988423"




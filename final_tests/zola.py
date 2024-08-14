import requests

# for NY
# address = "101 WEST END AVENUE, 10023"

# for LA
address = { "number" : "5200",
           "street" : "Wilshire" }

def lookup(address):
    """Look up the address and extract information"""

    # nyc_url = "https://search-api-production.herokuapp.com/search?helpers[]=geosearch-v2&helpers[]=bbl&helpers[]=neighborhood&helpers[]=zoning-district&helpers[]=zoning-map-amendment&helpers[]=special-purpose-district&helpers[]=commercial-overlay&q=" + address
    la_url = f"https://zimas.lacity.org/ajaxSearchResults.aspx?search=address&HouseNumber={address['number']}&StreetName={address['street']}"

    # for NYC
    #response = requests.get(nyc_url)
    #if response.json() == []:
    #    print(response.status_code)
    #    print(response.text)
    #    print("Invalid address")
    #else:
    #   print("Address is found")

    # for LA
    response = requests.get(la_url)

    if "Images/warning_icon.png" in response.text:
        print("Address NOT found")
    else:
        print("Address found!")

lookup(address)

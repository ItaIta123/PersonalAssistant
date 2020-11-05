import requests
from urllib.parse import urlencode  # a cool tool for making urls
import googlemaps
# import prettyprint
import pprint
from bs4 import BeautifulSoup
import keys

api_key = "Google API key"


def extract_lat_lng(address_or_postalcode='current', data_type='json', reverse=False, latlng=(0, 0)):
    """
    :param address_or_postalcode: address to geocode
    :param data_type:
    :param reverse: from geocode to address
    :param latlng: geocode lat and lng
    :return: the geolocation: (lat,lng)
    """
    # in the reverse case (geocode to address)
    if reverse is True:
        lat = latlng[0]
        lng = latlng[1]
        url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={api_key}'
        # print(url)
        r = requests.get(url)
        address = r.json()['results'][1]['formatted_address']
        # print(address)
        return address

    else:
        # in a case where current_location isn't specified; get the device's geocoding:
        if address_or_postalcode == 'current':
            geo_coding_website_html = requests.get('https://tools.keycdn.com/geo')
            # CHeck for page's availability
            if geo_coding_website_html.status_code not in range(200, 299):
                print("Error 404 Page could not be found")
                return "Error 404 Page could not be found"
            else:
                # parse the geocoding
                src = geo_coding_website_html.content
                soup = BeautifulSoup(src, 'lxml')
                # get the specific geocod html value
                try:
                    geocode = soup.findAll("dd", class_="col-8 text-monospace")[4].string
                    # print(geocode) OUTPUT = 32.2696 (lat) / 34.8876 (long)
                except:
                    print("Error parsing the geocode from the website. Google.py line 37")
                else:
                    # getting only the numbers
                    geocode = geocode.split()
                    lat = geocode[0]
                    lng = geocode[3]
                    current_location = float(lat), float(lng)
                    # print(current_location)
                    # OUTPUT = ('32.2696', '34.8876')
                    return current_location

        # There is a value for the address_postal code location
        else:
            end_point = f'https://maps.googleapis.com/maps/api/geocode/{data_type}'
            params = {'address': address_or_postalcode, 'key': api_key}
            url_params = urlencode(params)
            # print(url_params)
            url = f'{end_point}?{url_params}'
            # print(url)
            r = requests.get(url)
            # Check for page availability
            if r.status_code not in range(200, 299):
                return {}
            latlng = {}
            try:
                # Try to copy the location dict to latlng
                latlng = r.json()['results'][0]['geometry']['location']
            except:
                print("error loading the location from the json data")
            else:
                # If the 'try' statement worked latlng = {"lat" : 37.42165019999999, "lng" : -122.0856843 }
                return latlng.get('lat'), latlng.get('lng')


def distance(current_location='current', target_location=None):
    """
    :param current_location: can be specified or not. If not: getting the device's current location
    :param target_location:
    :return: Time and Seconds
    """
    if current_location == 'current':
        geocode_current_location = extract_lat_lng('current')
        current_location = extract_lat_lng(reverse=True, latlng=geocode_current_location)
        # Base url
        end_point = "https://maps.googleapis.com/maps/api/distancematrix/json?"
        params = {'origins': current_location, 'destinations': target_location, 'key': api_key}
        url_params = urlencode(params)
        final_url = f'{end_point}{url_params}'
        # print(final_url)

        # get response
        r = requests.get(final_url)
        # print(r)

        # return time as text and as seconds
        # print(r.json())
        try:
            time = r.json()['rows'][0]['elements'][0]['duration']['text']
            seconds = r.json()['rows'][0]['elements'][0]['duration']['value']
        except:
            print("Don't be silly, pick something else")
            return "Don't be silly, pick something else"
        else:
            # print/return the total travel time
            return time
            # print("Time" , time)
            # print("seconds", seconds)

    else:
        # Base url
        end_point = "https://maps.googleapis.com/maps/api/distancematrix/json?"
        params = {'origins': current_location, 'destinations': target_location, 'key': api_key}
        url_params = urlencode(params)
        final_url = f'{end_point}{url_params}'
        # print(final_url)

        # get response
        r = requests.get(final_url)
        # print(r)

        # return time as text and as seconds
        # print(r.json())
        try:
            time = r.json()['rows'][0]['elements'][0]['duration']['text']
            seconds = r.json()['rows'][0]['elements'][0]['duration']['value']
        except:
            print("Don't be silly, pick something else")
            return "Don't be silly, pick something else"
        else:
            # print/return the total travel time
            return time
            # print("Time" , time)
            # print("seconds", seconds)


def places_details(place_name='current', results_type=None):
    """
    :param place_name: The place you want to look for POI around
    :param results_type: https://developers.google.com/places/web-service/supported_types
    :return: Name of the POI, address , ETA (estimated time arrival)
    """
    # Define Client Object - the way to react with Google's maps api:
    gmaps = googlemaps.Client(key=api_key)  # Takes care the Required key= parameter in the .places_nearby()

    # Define Search:
    places_result = gmaps.places_nearby(location=extract_lat_lng(place_name), radius=5000, open_now=False,
                                        type=results_type)
    # print(places_result['results'])
    for place in places_result['results']:
        POI_name = place['name']
        place_address = place['vicinity']
        ETA = distance('current', place_address)
        if POI_name == place_address:
            pass
        else:
            print(f'Name: {POI_name} | Address: {place_address} | ETA: {ETA}')


if __name__ == "__main__":
    places_details("New York", 'coffee')

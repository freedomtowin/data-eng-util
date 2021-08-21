import urllib
s=requests.Session()
#reverse geoencoding
link="https://api.mapbox.com/geocoding/v5/mapbox.places/{LAT},{LONG}.json?access_token=INSERT_TOKEN"
response = s.get(url=link)
s.close()

s=requests.Session()
#geoencoding
link="https://api.mapbox.com/geocoding/v5/mapbox.places/{ADDRESS ZIP},{CITY},{STATE}?access_token=INSERT_TOKEN"
response = s.get(url=link)
s.close()

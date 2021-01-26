import spotipy
import json
import requests
from random import randrange
from spotipy.oauth2 import SpotifyOAuth

"""
Firebase

Code to retrieve data from Firebase database API 
"""

# api-endpoint
urlPrefix = 'https://DATABASENAME-default-rtdb.REGION.firebasedatabase.app/quotes/'
# get random int between first quote id to last for endpoint
quoteIdInt = randrange(1, 5) # small range for testing purposes
quoteStr = str(quoteIdInt)
urlQuoteSuffix = '/quote.json'
urlAuthorSuffix = '/author.json'
urlCitySuffix = '/city.json'

quoteUrl = urlPrefix + quoteStr + urlQuoteSuffix
authorUrl = urlPrefix + quoteStr + urlAuthorSuffix
cityUrl = urlPrefix + quoteStr + urlCitySuffix

# get requests
quote = requests.get(url=quoteUrl)
author = requests.get(url=authorUrl)
city = requests.get(url=cityUrl)

quoteData = quote.json()
authorData = author.json()
cityData = city.json()
# print quote
print('"' + quoteData + '"' + ' ~' + authorData + ' (' + cityData + ')')

"""
Spotipy

Spotipy code to retrieve currently playing song.
"""
# spotipy instance with auth info
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="CLIENT_ID",
                                               client_secret="CLIENT_SECRET",
                                               redirect_uri="RDR_URI",
                                               scope="user-read-currently-playing"))

# spotipy currently playing function
current_song = sp.currently_playing()

# getting currently playing song on user account
try:
    body = json.loads(json.dumps(current_song))
    artists = ""
    for a in body["item"]["artists"]:
        if artists != "":
            artists += ", "
        artists += a["name"]
    print({
        'Song:': body["item"]["name"],
        'Artist: ': artists
    })
except:
    print("Nothing is being played at the minute")

"""
WeatherAPI

Code to retrieve weather info for city
"""

# api-endpoint
weatherAPIEndpoint = 'http://api.weatherapi.com/v1/current.json?key=API_KEY&q=Dublin'

# sending get request and saving the response as response object
dublinCityWeather = requests.get(url=weatherAPIEndpoint)

# extracting data in json format
data = json.loads(json.dumps(dublinCityWeather.json()))

city = data['location']['name']
country = data['location']['country']
currentWeatherDegrees = str(data['current']['temp_c'])
currentWeatherInWords = data['current']['condition']['text']
currentWeatherIcon = data['current']['condition']['icon']

print(currentWeatherIcon + currentWeatherDegrees +
      'C - ' + currentWeatherInWords + ' - ' + city + ', ' + country)

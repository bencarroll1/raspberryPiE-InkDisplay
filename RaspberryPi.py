#!/usr/bin/env python

import argparse
import inkyphat
from PIL import Image, ImageFont, ImageDraw
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from font_intuitive import Intuitive
from inky.auto import auto
import random
import requests
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

try:
    inky_display = auto(ask_user=True, verbose=True)
except TypeError:
    raise TypeError("You need to update the Inky library to >= v1.1.0")

# inky_display.set_rotation(180)
try:
    inky_display.set_border(inky_display.YELLOW)
except NotImplementedError:
    pass

# Figure out scaling for display size
scale_size = 1.0
padding = 0

if inky_display.resolution == (400, 300):
    scale_size = 2.20
    padding = 15

if inky_display.resolution == (600, 448):
    scale_size = 2.20
    padding = 30

# Create a new canvas to draw on
img = Image.new("P", inky_display.resolution)
draw = ImageDraw.Draw(img)

# Load the fonts
intuitive_font = ImageFont.truetype(Intuitive, int(22 * scale_size))
hanken_medium_font_20 = ImageFont.truetype(
    HankenGroteskMedium, int(20 * scale_size))
hanken_medium_font = ImageFont.truetype(
    HankenGroteskMedium, int(22 * scale_size))

# Grab the name to be displayed

"""
Firebase

Code to retrieve data from Firebase database API
"""

# Reference: code written by Adam Bowie, as seen here: https://www.adambowie.com/blog/2019/09/news-twitter-feeds-and-inky-what-e-ink-display/


def reflow_quote(quote, width, font):
    words = quote.split(" ")
    reflowed = ' '
    line_length = 0

    for i in range(len(words)):
        word = words[i] + " "
        word_length = font.getsize(word)[0]
        line_length += word_length

        if line_length < width:
            reflowed += word
        else:
            line_length = word_length
            reflowed = reflowed[:-1] + "\n " + word

    return reflowed


# api-endpoint
urlPrefix = 'https://DATABASENAME-default-rtdb.REGION.firebasedatabase.app/quotes/'
# get random int between first quote id to last for endpoint
quoteStr = str(random.randint(1, 21))
print(quoteStr)
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

quoteData = str(quote.json())
authorData = str(author.json())
cityData = str(city.json())

# print quote
print('"' + quoteData + '"' + ' ~' + authorData + ' ('+cityData+')')
quote = '"' + quoteData + '"'
author = '~' + authorData

quoter = reflow_quote(quote, inky_display.WIDTH, font=intuitive_font)

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
        'Artist:': artists
    })
    song, artist = str(body["item"]["name"]), str(artists)

    nowPlaying = song + ' - ' + artist
    print(nowPlaying)

except:
    print("Nothing is being played at the minute")
    nowPlaying = 'Nothing Playing'

"""
WeatherAPI

Code to retrieve weather info for city
"""

# API endpoint
weatherAPIEndpoint = 'http://api.weatherapi.com/v1/current.json?key=API_KEY&q=CITY'

# sending get request and saving the response as response object
dublinCityWeather = requests.get(url=weatherAPIEndpoint)

# extracting data in json format
data = json.loads(json.dumps(dublinCityWeather.json()))

city = data['location']['name']
country = data['location']['country']
currentWeatherDegrees = str(data['current']['temp_c'])
currentWeatherInWords = data['current']['condition']['text']

print(currentWeatherDegrees +
      'C - ' + currentWeatherInWords + ' - ' + city + ', ' + country)

weather = currentWeatherDegrees + 'C - ' + city + ', ' + country

# Top and bottom y-coordinates for the white strip
y_top = int(inky_display.height * (5.0 / 10.0))
y_bottom = y_top + int(inky_display.height * (5.0 / 10.0))

# Draw the red, white, and red strips
for y in range(0, y_top):
    for x in range(0, inky_display.width):
        img.putpixel((x, y), inky_display.BLACK if inky_display.colour ==
                     "black" else inky_display.WHITE)

for y in range(y_top, y_bottom):
    for x in range(0, inky_display.width):
        img.putpixel((x, y), inky_display.WHITE)

for y in range(y_bottom, inky_display.height):
    for x in range(0, inky_display.width):
        img.putpixel((x, y), inky_display.BLACK if inky_display.colour ==
                     "black" else inky_display.WHITE)

# Calculate the positioning and draw the quote text
quote_w, quote_h = intuitive_font.getsize(str(quoter))
quote_x = int((inky_display.width - quote_w) / 2)
quote_y = 0 + padding
draw.text((0, quote_y), quoter,
          inky_display.BLACK, font=intuitive_font)

# Calculate the positioning and draw the weather text
author_w, author_h = intuitive_font.getsize(author)
author_x = int((inky_display.width - author_w) / 2)
author_y = quote_h + padding + 20
draw.text((author_x, author_y), author,
          inky_display.YELLOW, font=intuitive_font)

# Calculate the positioning and draw the quote text
spotify_w, spotify_h = hanken_medium_font.getsize(str(nowPlaying))
spotify_x = int((inky_display.width - spotify_w) / 2)
spotify_y = author_h + padding + 50
draw.text((spotify_x, spotify_y), str(nowPlaying),
          inky_display.BLACK, font=hanken_medium_font)

# Calculate the positioning and draw the quote author text
weather_w, weather_h = hanken_medium_font_20.getsize(str(weather))
weather_x = int((inky_display.width - weather_w) / 2)
weather_y = int(y_top + ((y_bottom - y_top - weather_h) / 2) + 20)
draw.text((weather_x, weather_y), weather,
          inky_display.BLACK, font=hanken_medium_font_20)

# Display the completed name badge
inky_display.set_image(img)
inky_display.show()

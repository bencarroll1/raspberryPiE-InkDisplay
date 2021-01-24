# Raspberry Pi Inky pHAT Peripheral Display - Quote, Currently Playing Spotify Song and Local Weather

## Overview
A project that uses a Raspberry Pi (Zero WH) to display information on to a Pimoroni Inky pHAT screen display.

## Aims
This project aims to display a quote retrieved from an Firebase Realtime Database API endpoint. I set up the database as a means to store quotes, the name of the person who said it, and the city they're from.

The projects also aims to display the name of the song and corresponding artist the user is currently listening to on Spotify.

Finally, the project aims to display information about the weather in the user's city including the temperature in Celcius, a text-based description of the weather, and the city and country it corresponds to.

## Motivation
I started this project as a means to try out using Raspberry Pi for the first time. I was curious to see how the Pi's work, as well as how it functions with the Inky pHAT display attached. To find out, I ended up creating this project that makes a few HTTP GET requests to various API's and displays the retrieved information out on the display, and as a result functions as a peripheral display for a desk.
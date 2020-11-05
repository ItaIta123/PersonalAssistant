# PersonalAssistant
A personal assistant built in Python that is able to send an email, show the weather, show POI near to your location or anywhere else on earth, ETA to a specific location, Read Wikipedia pages, and more...


Set-Up instructions: (View it in raw mode)

1. pip install the following libraries:
For the personalAsistant file:
  import pyttsx3 # for the speaking ability
  import speech_recognition as sr  # NOTICE as for 11/5/20 there is a probleb in pip install PyAudio. I found a solution that require using Brew package manager:     Install brew -> brew install portaudio -> pip3 install PyAudio
  import random
  import time
  import requests # Get the weather Json data from its url
  import wikipedia
  import smtplib # Mailing
  from Google import places_details, distance
For the Google file:
  import requests
  from urllib.parse import urlencode  # a cool tool for making urls
  import googlemaps
  import pprint # NOTICE the package name is prettyprint
  from bs4 import BeautifulSoup
  
2. You will have to register to google's cloud API service to get the API_KEY and enable Geocoding API,Places API, and Distance Matrix API. https://console.developers.google.com/
3. You will have to register to https://openweathermap.org/api as well.
4. Make sure to put them in the right place in the code.

import requests
from random import randrange

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
print('"'+quoteData + '"' + ' ~'+authorData + ' ('+cityData+')')

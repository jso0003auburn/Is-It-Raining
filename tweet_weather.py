# -*- coding: utf-8 -*-
import webapp2
import logging
import sys
import tweepy
import calendar
import ConfigParser
import urllib
import xml.etree.ElementTree as ET
import random
import time
import datetime

from google.appengine.api import taskqueue
from tweepy.auth import OAuthHandler
from tweepy.api import API
from ConfigParser import NoSectionError, NoOptionError
from urllib2 import urlopen, URLError

#settings.cfg contains WOEID for city identification as well as the keys to the Twitter API
#First function is designed to check the current conditions and then tweet the following
#Use Cron to schedule
 
 
            
class ATL(webapp2.RequestHandler):
    def get(self):
        forecast('ATL')
        
class CLT(webapp2.RequestHandler):
    def get(self):
        forecast('CLT')

def forecast(city):
    config = ConfigParser.RawConfigParser()
    config.read('settings.cfg')
    WOEID = config.get(city, 'WOEID')
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = ("select * from weather.forecast where woeid=" + WOEID)
    yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=xml"
    forecastfile = urllib.urlopen(yql_url)
    tree = ET.parse(forecastfile)
    query = tree.getroot()
    root = query[0]
    channel =  root[0]
    item = channel[12]
    description = item[5]
    forecast = item[7]
    high = forecast.attrib['high']
    low = forecast.attrib['low']
    forecastText = forecast.attrib['text']
    currentTemp = description.attrib['temp']
    currentText = description.attrib['text']
    currentC = description.attrib['code']
    currentCondition = int(currentC)
    timeStamp = description.attrib['date']
    forecastfile.close()

    rainCodes = [1,2,3,4,5,6,8,9,10,11,12,18,35,37,38,39,40,47,45,46]
    fairCodes = [31,32,33,34] 
    overcastCodes = [26,27,28]
    snowCodes = [13,14,15,16,41,42,43]
    uniqueCodes = [0,1,2,3,4,5,6,7,8,10,17,18,19,20,21,22,23,24,35,37,38,39,40,44,45,46,47]
    blankCodes = [9,11,12,25,29,30,36,3200]
    
    if currentCondition in rainCodes:
        yes_choices = ['Yes','Yes','Yea','Yep','Ya','Grab an umbrella',"It's raining"]
        a = random.choice(yes_choices)                

    else:
        no_choices = ['No','Nah','Nope','Not raining', 'Not raining']
        a = random.choice(no_choices)

    if currentCondition in fairCodes:
        fair_choices = [", beautiful day", ", clear day", ", nice day",", fair weather", ""]
        comment = random.choice(fair_choices)

    if currentCondition in overcastCodes: 
        overcast_choices = [", gloomy", ", cloudy", ", overcast", ", grey skies", ""]
        comment = random.choice(overcast_choices)

    if currentCondition in snowCodes:
        snow_choices = [", snowing", ", snow", ", snowfall", ", snow coming down"]
        comment = random.choice(snow_choices)

    if currentCondition in uniqueCodes:
        uniqueChoice = str( ", " + currentText )
        unique_choices = [uniqueChoice, ""]
        comment = random.choice(unique_choices)
        
    if currentCondition in blankCodes:
        comment = str('')
                       
    if 'PM' in timeStamp:
        timeStamp = "w/ low tonight of "
        tempHL = low
    else:
        timeStamp = "w/ high today of "
        tempHL = high
        q = taskqueue.Queue(city)
        q.purge()

    a = a.rstrip("\r\n")                                                
    comment = comment.rstrip("\r\n")
    comment = comment.lower()
    forecastText = forecastText.lower()

    answer = (a + comment + '.\n' + currentTemp + '° now ' + timeStamp + tempHL + '°\n' + "Forecast: " + forecastText + '.')
    logging.info(answer)
    CONSUMER_KEY = config.get(city, 'CONSUMER_KEY')
    CONSUMER_SECRET = config.get(city, 'CONSUMER_SECRET')
    ACCESS_TOKEN = config.get(city, 'ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = config.get(city, 'ACCESS_TOKEN_SECRET')
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = API(auth)
    result = api.update_status(status = answer)


app = webapp2.WSGIApplication([
    ('/ATL', EST),
    ('/CLT', CST),
], debug=False)
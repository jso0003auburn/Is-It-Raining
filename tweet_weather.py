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
            
class EST(webapp2.RequestHandler):
    def get(self):
        forecast('ATL')
        forecast('BOS')
        forecast('DC')
        forecast('MIA')

class CST(webapp2.RequestHandler):
    def get(self):
        forecast('ATX')
        forecast('BHM')
        forecast('CHI')
        forecast('DFW')
        forecast('HOU')

class PST(webapp2.RequestHandler):
    def get(self):
        forecast('LA')
        forecast('SEA')
        forecast('SFO')
        
class GMT(webapp2.RequestHandler):
    def get(self):
        forecast('ATA')
        forecast('LDN')
    
class UTC(webapp2.RequestHandler):
    def get(self):
        forecast('HKG')
        
class UTCm3(webapp2.RequestHandler):
    def get(self):
        forecast('RIO')  

class UTC10(webapp2.RequestHandler):
    def get(self):
        forecast('SYD')

class STATS(webapp2.RequestHandler):
    def get(self):
        checkup('ATA')
        checkup('ATL')
        checkup('ATX')
        checkup('BHM')
        checkup('BOS')
        checkup('CHI')
        checkup('DC')
        checkup('DFW')
        checkup('HKG')
        checkup('HOU')
        checkup('LA')
        checkup('LDN')
        checkup('MIA')
        checkup('RIO')
        checkup('SEA')
        checkup('SFO')
        checkup('SYD')

def checkup(city):
    config = ConfigParser.RawConfigParser()
    config.read('settings.cfg')
    myhandle = config.get(city, 'myhandle')
    CONSUMER_KEY = config.get(city, 'CONSUMER_KEY')
    CONSUMER_SECRET = config.get(city, 'CONSUMER_SECRET')
    ACCESS_TOKEN = config.get(city, 'ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = config.get(city, 'ACCESS_TOKEN_SECRET')

    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = API(auth)
    me = api.get_user(screen_name=myhandle)
    x = me.friends_count
    y = me.followers_count
    logging.critical('IsItRaining' + city + ' FOLLOWING:' + str( x ) + ' and FOLLOWERS: ' +  str( y ))

def forecast(city):
    config = ConfigParser.RawConfigParser()
    config.read('settings.cfg')
    WOEID = config.get(city, 'WOEID')
    units = config.get(city, 'units')
    forecastfile = urllib.urlopen("http://weather.yahooapis.com/forecastrss?w=" + WOEID + "&u=" + units)
    tree = ET.parse(forecastfile)
    root = tree.getroot()
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
    ata = 'ATA'

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
        no_choices = ['No','Nah','Nope','Not raining']
        a = random.choice(no_choices)

    if currentCondition in fairCodes:
        fair_choices = [", beautiful day", ", clear day", ", nice day", ""]
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
                       
    if 'pm' in timeStamp:
        timeStamp = "low tonight of "
        tempHL = low
    else:
        timeStamp = "high today of "
        tempHL = high

    if ata in city:
        timeStamp = 'later, '
        tempHL = low
        if currentCondition in snowCodes:
            snow_choices = [", snow", ", snowfall", ", snow coming down"]
            comment = random.choice(snow_choices)
            yes_choices = ["Yes","Yep","Yea","Snowing","Ya"]
            a = random.choice(yes_choices)            

        else:
            no_choices = ['Not snowing','No','Nah']
            a = random.choice(no_choices)
            comment = str('')
            pass

    a = a.rstrip("\r\n")                                                
    comment = comment.rstrip("\r\n")
    comment = comment.lower()
    forecastText = forecastText.lower()

    answer = (a + comment + '.\n' + currentTemp + '° now w/ ' + timeStamp + tempHL + '°\n' + "Forecast: " + forecastText + '.')
    logging.info(answer)
    CONSUMER_KEY = config.get(city, 'CONSUMER_KEY')
    CONSUMER_SECRET = config.get(city, 'CONSUMER_SECRET')
    ACCESS_TOKEN = config.get(city, 'ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = config.get(city, 'ACCESS_TOKEN_SECRET')
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = API(auth)
    result = api.update_status(status = answer )


app = webapp2.WSGIApplication([
    ('/EST', EST),
    ('/CST', CST),
    ('/PST', PST),
    ('/GMT', GMT),
    ('/UTC', UTC),
    ('/UTCm3', UTCm3),
    ('/UTC10', UTC10),
    ('/STATS', STATS),
], debug=False)
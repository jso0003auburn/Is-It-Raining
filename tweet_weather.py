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

config = ConfigParser.RawConfigParser()
config.read('settings.cfg')
WOEID = config.get('auth', 'WOEID')

#First function is designed to check the current conditions and then tweet the following
#    Now: yes/no + random comment
#    Later: forecasted conditions
#    Today: Low - High
#    Currently: Current Temp
#   
#    Use Cron file to schedule
    
class TweetForecast(webapp2.RequestHandler):
    def get(self):

        try:
            q = taskqueue.Queue('default')
            q.purge()
            forecastfile = urllib.urlopen("http://weather.yahooapis.com/forecastrss?w=" + WOEID + "&u=i")
            tree = ET.parse(forecastfile)
            root = tree.getroot()
            channel =  root[0]
            item = channel[12]
            description = item[5]
            forecast = item[7]
            high = forecast.attrib['high']
            low = forecast.attrib['low']
            forecast = forecast.attrib['text']
            currentTemp = description.attrib['temp']
            currentText = description.attrib['text']
            currentC = description.attrib['code']
            currentCondition = int(currentC)
            forecastfile.close()
            
            
            rainCodes = [1,2,3,4,5,6,8,9,10,11,12,18,35,45,46]
            scatteredCodes = [37,38,39,40,47]
            fairCodes = [31,32,33,34] 
            overcastCodes = [26,27,28]
            blankCodes = [29,30,44]
            snowCodes = [13,14,15,16,41,42,43,3200]
            uniqueCodes = [17,19,20,21,22,23,24,25,36]


            if currentCondition in rainCodes:
                with open('choices/yeschoices.txt') as yes_choicesf:        
                    yes_choices = yes_choicesf.readlines()
                    yes = random.choice(yes_choices)                
                    yes_choicesf.close()
                    a = yes
                    comment = str('')
            else:
                with open('choices/nochoices.txt') as no_choicesf:
                    no_choices = no_choicesf.readlines() 
                    no = random.choice(no_choices)
                    no_choicesf.close()
                    a = no

            if currentCondition in scatteredCodes:
                with open('choices/scatteredchoices.txt') as scattered_choicesf:
                    scattered_choices = scattered_choicesf.readlines() 
                    scattered = random.choice(scattered_choices)
                    scattered_choicesf.close()
                    a = scattered
                    comment = str('')

            if currentCondition in fairCodes:
                with open('choices/fairchoices.txt') as fair_choicesf:
                    fair_choices = fair_choicesf.readlines() 
                    fair = random.choice(fair_choices)
                    fair_choicesf.close()
                    comment = fair                   

            if currentCondition in overcastCodes: 
                with open('choices/overcastchoices.txt') as overcast_choicesf:
                    overcast_choices = overcast_choicesf.readlines() 
                    overcast = random.choice(overcast_choices)
                    overcast_choicesf.close()
                    comment = overcast 
        
            if currentCondition in blankCodes:
                    comment = str('')
        
            if currentCondition in snowCodes:
                with open('choices/snowchoices.txt') as snow_choicesf:
                    snow_choices = snow_choicesf.readlines() 
                    snow = random.choice(snow_choices)
                    snow_choicesf.close()
                    comment = snow
        

            if currentCondition in uniqueCodes:
                    comment = str( ' ' + currentText + '.')

            a = a.rstrip("\r\n")                                                
            comment = comment.rstrip("\r\n")
            
            
            answer = ('Now: ' + a + ' ' + comment + '\n' + "Later: " + forecast + '.' + '\n' + 'Today: ' + low + '° - ' + high + '°\n' + 'Currently: ' + currentTemp + '°')
            logging.info(answer)
            tweet(answer)

        except URLError:
            logging.error('URLError: ' + str(sys.exc_info()[0]) + str(sys.exc_info()[1]))
            logging.error(answer)

        except IOError:
            logging.error('IOError: ' + str(sys.exc_info()[0]) + str(sys.exc_info()[1]))
            logging.error(answer)
        
        except:
            logging.error('Unexpected error: ' + str(sys.exc_info()[0]) + str(sys.exc_info()[1]))
            logging.error(answer)

#Checks if it is raining or not and replies with a simple yes and the current temp
#
#Uses Google Task Queues to reload it.
#This will ONLY tweet if it is raining.
#If it is NOT raining, then another instance of the task is sent to the default queue
#Polling frequency can be adjusted by changing the settings of the queue
#
#If it IS raining and the tweet is succesful the task queue will be purged and the operation will shut down until it is started again.
#
#Use Cron to start it every afternoon, if it is still running from the previous day then it will just be reloaded.
#
#This ensures that it doesn't tweet Yes more than once a day
#Cron only has to start it once, after that the frequency with which it checks the Yahoo Weather API will vary depending on the Queue settings
#The Google task queue is configured by the queue.yaml file
#Current setting allows 12 tasks per hour... so it checks every 5 minutes

class TweetYes(webapp2.RequestHandler):
    def get(self):
        forecastfile = urllib.urlopen("http://weather.yahooapis.com/forecastrss?w=" + WOEID + "&u=i")
        tree = ET.parse(forecastfile)
        root = tree.getroot()
        channel =  root[0]
        item = channel[12]
        description = item[5]
        currentC = description.attrib['code']
        currentCondition = int(currentC)
        forecast = item[7]
        high = forecast.attrib['high']
        low = forecast.attrib['low']
        forecast = forecast.attrib['text']
        currentTemp = description.attrib['temp']
        currentText = description.attrib['text']
        forecastfile.close()
        rainCodes = [1,2,3,4,5,6,8,9,10,11,12,18,35,45,46,47]  
        thunderCodes = [38]  
        if currentCondition in rainCodes:
        
            yes_choices = ['Yes.', 'Yes.', 'Yep.', "Yes...", 'Yep...', 'Ya', 'Yeah.', 'Yes.', 'Yep.', "You're going to need an umbrella.", "Yea, that's rain you're hearing"]
            yes = random.choice(yes_choices)
            a = str( yes + '\n' + currentTemp + '°')
            tweet(a)  
            logging.info(a)
            q = taskqueue.Queue('default')
            q.purge()
            time.sleep(30)
        
        else:
            logging.debug('Still not raining: ' + currentC + ' ' + currentText + ' ' + currentTemp)
            taskqueue.add(url="/tweet_yes", method="GET")
        
        if currentCondition in thunderCodes:
            
			a = str( currentText + '\n' + currentTemp + '°')
			tweet(a)  
			logging.info(a)
			q = taskqueue.Queue('default')
			q.purge()
			time.sleep(30)

def tweet(answer):
    CONSUMER_KEY = config.get('auth', 'CONSUMER_KEY')
    CONSUMER_SECRET = config.get('auth', 'CONSUMER_SECRET')
    ACCESS_TOKEN = config.get('auth', 'ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = config.get('auth', 'ACCESS_TOKEN_SECRET')

    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = API(auth)
    result = api.update_status(status = answer )



app = webapp2.WSGIApplication([
    ('/tweet_forecast', TweetForecast),
    ('/tweet_yes', TweetYes)
], debug=False)
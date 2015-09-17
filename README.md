#About:

Is-It-Raining automates a Twitter account for the purpose of checking the current weather and forecast.

A forecast tweet that can be scheduled via Cron. 

The forecast tweet will post a tweet in the following format:

	Yes/No, weather comment.
	Currently temp.
	Tonight/Today's high/low and forecast



Example account updated by this script: https://twitter.com/IsItRainingATL


Author: John Olson

#Dependencies: 
tweepy (https://github.com/tweepy/tweepy)

Twitter API: https://dev.twitter.com/


#Configuration:

Configuration is controlled through settings.cfg which must be in the same
directory as tweet_weather.py.  Your Twitter Application ID tokens need to be
stored in this file to give the script permission to post status messages
on your Twitter account. This section is required.

The location of the Weather data is controlled by Yahoo! WOEID which is also
stored in settings.cfg

You can lookup WOEID for a location here:

http://woeid.rosselliot.co.nz/


Example settings.cfg
--------------------

	[ATL]
	WOEID = 2371098
	CONSUMER_KEY = ConsumerKey
	CONSUMER_SECRET = ConsumerSecret
	ACCESS_TOKEN = AccessToken
	ACCESS_TOKEN_SECRET = AccessSecret
	units = i


#Logging:

Status / error messages are stored within the Google App Engine's logging mechanism and
can be checked within the console there.




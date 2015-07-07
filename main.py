import webapp2
#main landing page for the Google App engine:
#Admin links can be used to trigger a forecast tweet or the Yes Check link will restart that process
#These are tied to your google account so they will only work if you are logged in
MAIN_PAGE_HTML = """\
<html>
  <head>
    <title>Is It Raining?</title>
  </head>
  <body><center>
    <h3>Is It Raining?</h3>
    <p>I'm a Twitter bot that posts weather updates.
    <p>I'll give you a current update and forecast at 7:20 AM to get your day started.
    <p>After that, I'll shut up until 4:20 PM, when I'll give you an afternoon update and forecast for the drive home.
    <p>Also, if it starts raining I'll let you know.
    <p><b>Admin Only:</b>
    <p><a href="https://console.developers.google.com/project">Go To Console</a>
    <p><a href="https://appengine.google.com/">Go To App Engine</a>
    <p><a href="/tweet_forecast" target="popup" onclick="window.open('/tweet_forecast','name','width=200,height=200')">Forecast</a>
    <p><a href="/tweet_yes" target="popup" onclick="window.open('/tweet_yes','name','width=200,height=200')">Yes Check</a>
    <p><a href="https://www.yahoo.com/?ilc=401" target="_blank"> <img src="https://poweredby.yahoo.com/purple.png" width="134" height="29"/> </a>
    <p><img src="http://www.logicsoft.md/images/google-app-engine.png"/>
  </center></body>
</html>
"""


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(MAIN_PAGE_HTML)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)

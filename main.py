import webapp2

MAIN_PAGE_HTML = """\
<html>
  <head>
    <title>Is It Raining?</title>
  </head>
  <body><center>
    <h3>Is It Raining?</h3>
    <p>I'm a Twitter bot that posts weather updates.
    <p>I live in Atlanta, but if you want me to add your city or give a suggestion just tell me: <a href="mailto:IsItRainingTwitter@gmail.com?Subject=Hey,%20rainy%20twitter" target="_top">IsItRainingTwitter@gmail.com</a>
    <p>Current locations:
    <p>ATA: Antarctica
    <p>ATL: Atlanta
    <p>ATX: Austin
    <p>BHM: Birmingham
    <p>BOS: Boston
    <p>CHI: Chicago
    <p>CHS: Charleston
    <p>DC: D.C.
    <p>DFW: Dallas
    <p>HKG: Hong Kong
    <p>HOU: Houston
    <p>LA: Los Angeles
    <p>LDN: London
    <p>MIA: Miami
    <p>RIO: Rio de Janiero
    <p>SEA: Seattle
    <p>SFO: San Francisco
    <p>SYD: Sydney.
    <p><b>Admin Only:</b>
    <p><a href="https://console.developers.google.com/project">Go To Console</a>
    <p><a href="https://appengine.google.com/">Go To App Engine</a>
    <p><a href="/EST" target="_blank">EST</a>
    <p><a href="/CST" target="_blank">CST</a>
    <p><a href="/PST" target="_blank">PST</a>
    <p><a href="/GMT" target="_blank">GMT</a>
    <p><a href="/UTC" target="_blank">UTC</a>
    <p><a href="/UTCm3" target="_blank">UTCm3</a>        
    <p><a href="/UTC10" target="_blank">UTC10</a>
    <p><a href="/STATS" target="_blank">STATS</a>
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

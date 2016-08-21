import webapp2

MAIN_PAGE_HTML = """\
<html>
  <head>
    <title>Is It Raining?</title>
  </head>
  <body><center>
    <h3>Is It Raining?</h3>
    <p>I'm a Twitter bot.
</html>
"""


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(MAIN_PAGE_HTML)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)

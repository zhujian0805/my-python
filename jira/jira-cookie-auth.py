class JiraConnection(object):
  def __init__(self,):
    self.server   = "https://jira.domain.net"
    self._auth     = {"username": "jzhu", "password": "!"}
    self._auth_url = self.server + "/rest/auth/latest/session"
    self._api      = "/rest/api/latest"

    self.http = None
    self.authenticate()

  def authenticate(self):
    jar = cookielib.CookieJar()
    self._opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
    request = urllib2.Request(self._auth_url)
    request.add_data(json.dumps(self._auth))
    request.add_header("Content-type", "application/json")
    request.add_header("Accept", "application/json")
    try:
      self.http = self._opener.open(request)
      self.http.close()
    except urllib2.URLError, err:
      print "AUTH Error"
      print err



jira = JiraConnection()

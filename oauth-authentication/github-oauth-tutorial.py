#!/usr/bin/python
from pprint import pprint
import json

# Credentials you get from registering a new application
client_id = '2607467f409a6ff2c25d'
client_secret = '73f30950b9a89ccb665bf75e3a432d26c7da815d'

# OAuth endpoints given in the GitHub API documentation
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'

from requests_oauthlib import OAuth2Session
github = OAuth2Session(client_id)

# Redirect user to GitHub for authorization
authorization_url, state = github.authorization_url(authorization_base_url)
print 'Please go here and authorize,', authorization_url

# Get the authorization verifier code from the callback url
redirect_response = raw_input('Paste the full redirect URL here:')

# Fetch the access token
github.fetch_token(token_url, client_secret=client_secret,
        authorization_response=redirect_response)

# Fetch a protected resource, i.e. user profile
r = github.get('https://api.github.com/user/repos')

decoded = json.loads(r.content)

print json.dumps(decoded, sort_keys=True, indent=4)

#for i in decoded:
#  print i['name']

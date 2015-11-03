#!/usr/bin/python
from pprint import pprint
import json
from requests_oauthlib import OAuth2Session

client_id = 'usas96gfgx4b2rgxxc5sq5d7utng'
client_secret = 'Aa7xzrPFslfjwjmCjaza8ezvJwgAuz6PJca'
authorization_base_url = 'https://www.battlenet.com.cn/oauth/authorize'
token_url = 'https://www.battlenet.com.cn/oauth/token'

battlenet = OAuth2Session(client_id,redirect_uri='https://localhost/callback')
authorization_url, state = battlenet.authorization_url(authorization_base_url)

print 'Please go here and authorize,', authorization_url

redirect_response = raw_input('Paste the full redirect URL here:')

battlenet.fetch_token(token_url, client_secret=client_secret, authorization_response=redirect_response)

r = battlenet.get('https://api.battlenet.com.cn/account/user')

print r.content

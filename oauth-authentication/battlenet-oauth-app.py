#!/usr/bin/python
# ****** Note: This seems doesn't work for CN but works for US

from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify
import json
import os
from pprint import pprint
from werkzeug.serving import make_ssl_devcert, run_simple

app = Flask(__name__)


# This information is obtained upon registration of a new GitHub OAuth
# application here: https://github.com/settings/applications/new
client_id = "dt4"
client_secret = "sS"
authorization_base_url = 'https://www.battlenet.com.cn/oauth/authorize'
token_url = 'https://www.battlenet.com.cn/oauth/token'


@app.route("/")
def demo():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Github)
    using an URL with a few key OAuth parameters.
    """
    github = OAuth2Session(client_id)
    authorization_url, state = github.authorization_url(authorization_base_url)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    print authorization_url
    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider.

@app.route("/callback", methods=["GET"])
def callback():
    print '--------- callbacking ----------------'
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    github = OAuth2Session(client_id, state=session['oauth_state'])
    token = github.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.url)

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /profile.
    print 'token is ---------' , token
    session['oauth_token'] = token
    return redirect('https://dev.battle.net/')


@app.route("/profile", methods=["GET"])
def profile():
    print '---------------- profiling --------------'
    """Fetching a protected resource using an OAuth 2 token.
    """
    github = OAuth2Session(client_id, token=session['oauth_token'])

    #res = github.get('https://api.github.com/user').json()
    res = github.get('https://api.github.com/user/repos').json()
    ret = {}
    for r in res:
      ret[r['name']] = r

    return jsonify(ret)

if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    os.environ['DEBUG'] = "1"
    make_ssl_devcert('/tmp', host='localhost')

    app.secret_key = os.urandom(24)
    #app.run(debug=True)
    run_simple('localhost', 443, app, ssl_context=('/tmp/key.crt', '/tmp/key.key'))

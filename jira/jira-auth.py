#!/usr/bin/python

from jira.client import JIRA

options = { 'server': 'https://jira.atlassian.com' }
server = "https://jira.sample.net"
credentials = ( 'jameszhu', '%t6y7u8i' )

jiraclient = JIRA(basic_auth=credentials, server = server, options = options)

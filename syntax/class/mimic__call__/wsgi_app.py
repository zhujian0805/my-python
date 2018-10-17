#!/usr/bin/python

from Router import Router
from os import environ

router = Router()


#here is the application
@router('/hello')
def hello(environ, start_response):
    status = '200 OK'
    output = 'Hello'
    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    write = start_response(status, response_headers)
    return [output]


@router('/world')
def world(environ, start_response):
    status = '200 OK'
    output = 'World!'
    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    write = start_response(status, response_headers)
    return [output]


#here run the application
result = router.route(environ, start_response)
for value in result:
    write(value)

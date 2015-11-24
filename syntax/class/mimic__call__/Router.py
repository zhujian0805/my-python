#!/usr/bin/python

class Router(object):  
    def __init__(self):  
        self.path_info = {}  
    def route(self, environ, start_response):  
        application = self.path_info[environ['PATH_INFO']]  
        return application(environ, start_response)  
    def __call__(self, path):  
        def wrapper(application):  
            self.path_info[path] = application  
        return wrapper

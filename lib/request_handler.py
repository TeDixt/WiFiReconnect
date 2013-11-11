#!/usr/bin/env python
#-*- coding: utf-8 -*-
import urllib, urllib2, cookielib
import random, json, os ,sys

script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
UA = json.load(open(os.path.join(script_dir, 'ua.txt')))

class Response:
    """Simple class for storing response info"""

    def __init__(self, body=None, error=None, code=None, url=None):
        if body:
            self.code = body.code
            self.headers = body.headers.dict
            self.url = body.url
            self.body = body.read()
        else:
            self.code = code
            self.headers = {}
            self.url = url
            self.body = ''
        self.error = error


class RequestHandler:
    """Simple class for processing requests"""

    def __init__(self, headers={}, user_agent=''): # headers - global headers for all requests
        self.cookie = cookielib.CookieJar()
        handlers = [urllib2.HTTPCookieProcessor, urllib2.HTTPCookieProcessor(self.cookie)]
        self.opener = urllib2.build_opener(*handlers)
        self.response = None
        self.headers = headers
        self.headers['User-Agent'] = user_agent or random.choice(UA)

    def openurl(self, url, GET={}, POST={}, headers={}): # headers - temporary headers for current request
        temp_headers = self.headers
        temp_headers.update(headers)

        if GET:
            get_data = urllib.urlencode(GET)
            url += '?' + get_data

        post_data = ''
        if POST:
            post_data = urllib.urlencode(POST)

        request = urllib2.Request(url, post_data, self.headers)
        try:
            self.response = Response(body=self.opener.open(request))
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                self.response = Response(error=e.reason, url=url)
            elif hasattr(e, 'code'):
                self.response = Response(code=e.code, url=url)
        return self.response

#!/usr/bin/env python
#-*- coding: utf-8 -*-
import urllib, urllib2, cookielib
import random, json, os ,sys

UA = [
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36",
	"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36",
	"Mozilla/5.0 (X11; Linux i686; rv:21.0) Gecko/20100101 Firefox/21.0",
	"Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:25.0) Gecko/20100101 Firefox/25.0",
	"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
	"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10",
	"Opera/9.80 (Windows NT 6.1; U; ru) Presto/2.8.131 Version/11.10",
	"Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14"
]


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

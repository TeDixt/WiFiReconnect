#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time
from lib import request_handler

LINK_FOR_TESTS = "http://www.yandex.ru"
WIFI_LINK = "https://startwifi.beeline.ru/status"
TIMEOUT = 2 # in seconds

REQUEST_DICT = {
    "url":LINK_FOR_TESTS,
    "mode": "partner",
}

r = request_handler.RequestHandler()
r.openurl(WIFI_LINK)

def reconnect():
    r.openurl(WIFI_LINK, POST=REQUEST_DICT)

def check_connection():
    response = r.openurl(LINK_FOR_TESTS)
    if 'beeline' in response.url:
        return False
    return True

while True:
    if not check_connection():
        print "Connecting"
        reconnect()
        conn = check_connection()
        if r.response.code == 403:
            print "You haven\'t connected to WiFi yet"
        elif conn:
            print "Connected"
        elif not conn or r.response.error:
            print 'Unknown error'
    time.sleep(TIMEOUT)

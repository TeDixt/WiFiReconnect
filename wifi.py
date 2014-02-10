#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time
from lib import request_handler

LINK_FOR_TESTS = "http://www.yandex.ru"
WIFI_LINK = "https://startwifi.beeline.ru/status"
TIMEOUT = 2 # in seconds
KEYWORD = 'beeline' #word, which is searching in url to check for redirect on wifi page

REQUEST_DICT = {
    "url":LINK_FOR_TESTS,
    "mode": "partner",
}

class WiFiReconnecter(request_handler.RequestHandler):
    def connect(self):
        self.openurl(WIFI_LINK)

    def reconnect(self):
        self.openurl(WIFI_LINK, POST=REQUEST_DICT)

    def check_connection(self):
        self.openurl(LINK_FOR_TESTS)
        if KEYWORD in self.response.url:
            return False
        return True

    def check_wifi_connection(self):
        self.openurl(WIFI_LINK)
        if self.response.code == 403:
            return False
        return True


def run():
    print "Starting"

    r = WiFiReconnecter()
    r.connect()

    if r.check_connection(): print 'Already connected'

    while True:
        if not r.check_connection():
            print "Connecting"
            r.reconnect()

            connected = r.check_connection()
            connected_to_wifi = r.check_wifi_connection()

            if not connected_to_wifi:
                print "You haven\'t connected to WiFi yet"
            elif connected:
                print "Connected"
            elif not connected or r.response.error:
                print 'Unknown error'

        time.sleep(TIMEOUT)

if __name__ == '__main__':
    run()
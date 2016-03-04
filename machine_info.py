#! /usr/bin/env python

import requests
import platform


URL = 'http://127.0.0.1:5000/report'


def send_info():
    uname = platform.uname()
    request = requests.post(URL, data=uname._asdict())
    if request.ok:
        print('Submitted. Thanks!')

if __name__ == '__main__':
    response = input('Send info to test server? (Y/n) ')
    if response != 'n':
        send_info()

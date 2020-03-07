#!/usr/bin/env python
# -- coding: utf-8 --
# Usage: rd1000_spider.py user_id
# Email: weixu_2008@163.com

import requests
import re
import os
import sys
import json
import urllib
import time

def get_downloadurl():
    record_fd = open('history.txt', 'a+')
    all_lines = record_fd.readlines()
    if len(all_lines) <= 0 :
        history_count = 0
    else :
        history_count = all_lines[-1]

    history_count = int(history_count)
    print "have download mp3: %i" % history_count

    search_url = 'https://api.read1000.com/plain/share/recording?uid=%s' % sys.argv[1]
    r = requests.get(search_url, timeout=20)
    data = r.content
    data = data.lstrip('callback(')
    data = data.rstrip(')')
    d = json.loads(data)
    d = d['recordingList']
    total = len(d)
    print "until now, we have %i mp3s in total" % total

    index = 0
    #https://user.read1000.com/user/153835/recording/Big%20Cat%20Yellow%20%E5%A4%A7%E7%8C%AB%E5%88%86%E7%BA%A7%E9%BB%84%E8%89%B2/Water%20Bears/20200218-210237-499.mp3
    for item in d:
        index = index + 1
        if index < history_count :
            print "skip the mp3: " + item['title'] + "which we have downloaded"
            continue

        print "downloading %i " % index + "mp3: " + item['title']
        resource_url = 'https://user.read1000.com/' + urllib.quote(item['osskey'].encode('utf-8'))
        r = requests.get(resource_url, timeout=20, verify=False)
        mp3_title = item['title'] + "-" + item['date_time']
        mp3_fd = open(mp3_title + ".mp3",'wb')
        mp3_fd.write(r.content)
        mp3_fd.close()

        record_fd.writelines(str(index))
        record_fd.write('\n')
        time.sleep(2)

    record_fd.close()

def main():
    filename = sys.argv[0]
    if len(sys.argv) < 2:
        print 'Usage: ' + os.path.basename(filename) + ' username'
        sys.exit()
    get_downloadurl()

if __name__ == '__main__':
    main()

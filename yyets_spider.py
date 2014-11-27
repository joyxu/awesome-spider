#!/usr/bin/env python
# -- coding: utf-8 --
# Usage: yyets_spider.py keyword
# Email: lyleaks@gmail.com

import requests
import re
import os
import sys


def get_downloadurl():
    search_url = 'http://yyets.mirrors.ga/search/index?keyword=%s' % sys.argv[1]
    resource_url = 'http://yyets.mirrors.ga/resource/'
    r = requests.get(search_url, timeout=20)
    data = r.content
    match = re.search(r'yyets\.mirrors\.ga/resource/(\d+)', data)
    if match:
        num = match.group(1)
        resource_url = resource_url + num
        r = requests.get(resource_url, timeout=20)
        data = r.content
        download_list = re.findall(r'"(ed2k://\S+.(S\d+E\d+)\S+1024\w576\S+)"', data)
        if download_list:
            with open('result.txt', 'w') as f:
                for i in download_list:
                    while download_list.count(i) > 1:
                        del download_list[download_list.index(i)]
                    f.write('%s %s\n%s\n' % (sys.argv[1], i[1], i[0]))
                print 'Save as result.txt'
        else:
            print 'No Resource'
    else:
        print 'Not Found'


def main():
    filename = sys.argv[0]
    if len(sys.argv) < 2:
        print 'Usage: ' + os.path.basename(filename) + ' keyword'
        sys.exit()
    get_downloadurl()

if __name__ == '__main__':
    main()

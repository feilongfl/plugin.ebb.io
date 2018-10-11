# -*- coding: utf-8 -*-

import json
import re
import sys
import urllib
import urllib2
import urlparse


from resources.lib import lzstring
x = lzstring.LZString()

def Get(url):
    # print(url)
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0)')
    return urllib2.urlopen(req).read()

def GetUtf16(url):
    # download pages
    page = Get(url)
    # decompress
    return x.decompressFromUTF16(page.decode('utf-8')).encode('utf-8')


matchObj = re.search("\/anime\/(\d+)x(\d+)", """/anime/470x801""", flags=0)
id = matchObj.group(1)
seasons = matchObj.group(2)

jsonArr = json.loads(GetUtf16("https://ebb.io/_/season_list/" + id))
if jsonArr['success'] == True:
    for jsonSeason in jsonArr['list']['seasons']:
        if jsonSeason['id'] == int(seasons):
            for jsonEpisodes in jsonSeason['episodes']:
                print jsonEpisodes['id']

# genTimeList("https://ebb.io/_/hpdata")

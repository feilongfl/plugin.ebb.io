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

# def genTimeList(url):
# download pages
page = Get("https://ebb.io/_/hpdata")
print("get url done")
print(page)
# decompress
jsonStr = x.decompressFromUTF16(page.decode('utf-8')).encode('utf-8')
print(jsonStr)
#load json
jsonArr = json.loads(jsonStr)
# add to list
# jsonDay = jsonArr["calendar"]["days"][0]
# jsonAnime = jsonDay["animes"][0]
# if jsonAnime["path"] != None:
#     print(jsonAnime["name"],jsonAnime["path"])

for jsonDay in jsonArr["calendar"]["days"]:
    for jsonAnime in jsonDay["animes"]:
        if jsonAnime["path"] != None:
            print(jsonAnime["name"].encode("utf-8"),jsonAnime["path"])
            


# genTimeList("https://ebb.io/_/hpdata")

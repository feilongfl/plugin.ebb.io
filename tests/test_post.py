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

def Post(url,params):
    req = urllib2.Request(url)
    _params = urllib.urlencode(params)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0)')
    return urllib2.urlopen(req,_params).read()

def PostForUtf16(url,params):
    page = Post(url,params)
    return x.decompressFromUTF16(page.decode('utf-8')).encode('utf-8')

searchStr = 'dao'
jsonArr = PostForUtf16("https://ebb.io/_/search",{'query': searchStr})
print jsonArr

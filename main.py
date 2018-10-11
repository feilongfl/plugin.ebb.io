# -*- coding: utf-8 -*-

# from resources.lib import kodilogging
# from resources.lib import plugin
#
# import logging
# import xbmcaddon

import json
import re
import sys
import urllib
import urllib2
import urlparse

import xbmc
import xbmcgui
import xbmcplugin

#lz-string
from resources.lib import lzstring
x = lzstring.LZString()

#init plugin
base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def Get(url):
    # print(url)
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0)')
    return urllib2.urlopen(req).read()

def Post(url,params):
    req = urllib2.Request(url)
    _params = urllib.urlencode(params)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0)')
    return urllib2.urlopen(req,_params).read()

def GetUtf16(url):
    # download pages
    page = Get(url)
    # print("get url done")
    # print(page)
    # decompress
    # jsonStr = x.decompressFromUTF16(page.decode('utf-8')).encode('utf-8')
    return x.decompressFromUTF16(page.decode('utf-8')).encode('utf-8')
    # print(jsonStr)
    # return jsonStr

def PostForUtf16(url,params):
    page = Post(url,params)
    return x.decompressFromUTF16(page.decode('utf-8')).encode('utf-8')

# decode
def ttdecode(code):
    # print code
    str = ""
    key = "ttrandomkeyqdramanet"
    for i in range(0,len(code)):
        if (0 == i or 0 == i % (len(key) + 1)):
            str += code[i]

    return str[::-1]

# home page
mode = args.get('mode', None)
if mode is None:
    li = xbmcgui.ListItem(u'This Season Anime'.encode('utf-8'))
    url = build_url({'mode': 'TS-List'})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    # li = xbmcgui.ListItem(u'New Anime'.encode('utf-8'))
    # url = build_url({'mode': 'NA-List'})
    # xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    #
    # li = xbmcgui.ListItem(u'Excellent Anime'.encode('utf-8'))
    # url = build_url({'mode': 'EA-List'})
    # xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    li = xbmcgui.ListItem(u'All Anime'.encode('utf-8'))
    url = build_url({'mode': 'AA-List'})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    # li = xbmcgui.ListItem(u'Search'.encode('utf-8'))
    # url = build_url({'mode': 'Search'})
    # xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    # li = xbmcgui.ListItem(u'test'.encode('utf-8'))
    # li.setInfo("video",{})
    # video_url = "https://vpx.ebbstatic.com/s/583852059091140608/manifest.csv"
    # xbmcplugin.addDirectoryItem(handle=addon_handle, url=video_url, listitem=li)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'TS-List':
    #https://ebb.io/_/hpdata
    #load json
    jsonArr = json.loads(GetUtf16("https://ebb.io/_/hpdata"))
    # add to list
    for jsonDay in jsonArr["calendar"]["days"]:
        for jsonAnime in jsonDay["animes"]:
            if jsonAnime["path"] != None:
                # print(jsonAnime["name"].encode("utf-8"),jsonAnime["path"])
                try:
                    matchObj = re.search("\/anime\/(\d+)x(\d+)", jsonAnime["path"], flags=0)
                    id = matchObj.group(1)
                    seasons = matchObj.group(2)

                    li = xbmcgui.ListItem(jsonAnime["name"],thumbnailImage="https://ebb.io/_/poster/" + id + "x" + seasons)
                    # print ("https://ebb.io/_/poster/" + id + "x" + seasons)
                    # url = build_url({'mode': 'video-info', 'path': jsonAnime["path"]})
                    url = build_url({'mode': 'video-info', 'id': id, 'seasons': seasons})
                    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
                except BaseException:
                    print("err")

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'AA-List':
    # https://ebb.io/_/anime_list
    #load json
    jsonArr = json.loads(GetUtf16("https://ebb.io/_/anime_list"))
    # add to list
    for jsonAnime in jsonArr:
        try:
            id = str(jsonAnime['anime_id'])
            seasons = str(jsonAnime['season_id'])
            # print (id,seasons,jsonAnime['name_chi'])

            li = xbmcgui.ListItem(jsonAnime['name_chi'],thumbnailImage="https://ebb.io/_/poster/" + id + "x" + seasons)
            li = xbmcgui.ListItem(jsonAnime['name_chi'])
            # print ("https://ebb.io/_/poster/" + id + "x" + seasons)
            # url = build_url({'mode': 'video-info', 'path': jsonAnime["path"]})
            url = build_url({'mode': 'video-info', 'id': id, 'seasons': seasons})
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
        except BaseException:
            print("err")

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'video-info':
    # matchObj = re.search("\/anime\/(\d+)x(\d+)", args['path'][0], flags=0)
    # id = matchObj.group(1)
    # seasons = matchObj.group(2)

    id = args['id'][0]
    seasons = args['seasons'][0]

    jsonArr = json.loads(GetUtf16("https://ebb.io/_/season_list/" + id))
    if jsonArr['success'] == True:
        for jsonSeason in jsonArr['list']['seasons']:
            if jsonSeason['id'] == int(seasons):
                for jsonEpisodes in jsonSeason['episodes']:
                    # print jsonEpisodes['id']
                    li = xbmcgui.ListItem(jsonArr['list']['anime']['name_chi'] + jsonEpisodes['title'],thumbnailImage="https://ebb.io/_/poster/" + id + "x" + seasons)
                    li.setInfo("video",{
                        'director': jsonArr['list']['anime']['author'],
                        'title': jsonArr['list']['anime']['name_chi'] + jsonEpisodes['title'],
                        'originaltitle': jsonArr['list']['anime']['name_jpn'],
                        'plot': jsonArr['list']['anime']['description'],
                        'sorttitle': jsonEpisodes['title'],
                        'status': jsonArr['list']['anime']['is_ended']
                    })
                    video_url = jsonEpisodes['sl']
                    xbmcplugin.addDirectoryItem(handle=addon_handle, url=video_url, listitem=li)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'Search':
    # https://ebb.io/_/search
    searchStr = 'dao'
    jsonArr = PostForUtf16("https://ebb.io/_/search",{'query': searchStr})
    print jsonArr
    xbmcgui.Dialog().ok(u'is developing'.encode('utf-8'),u'is developing'.encode('utf-8'))

else:
    xbmcgui.Dialog().ok(u'is developing'.encode('utf-8'),u'is developing'.encode('utf-8'))

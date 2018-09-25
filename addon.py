import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmc

import requests
import re

def getMoviesFromPage(url):
    inputHTML = requests.get(url).text
    inputList = inputHTML.split('</li>')
    pattern = '<li.*href="(.*)".*title="(.*)".*src="(.*.jpg)".*'
    returnValue = []
    for input in inputList:
        result = re.search(pattern, input, re.IGNORECASE | re.DOTALL)
        if result is not None:
            returnValue.append({'link': result.group(1), 'title': result.group(2), 'image': result.group(3)})
    return returnValue

SERVER_BASE_URL = "http://tamilyogi.cc/"
CATEGORIES = {'home': "home/",
            'new':"category/tamilyogi-full-movie-online/",
            'brrip':"category/tamilyogi-bluray-movies/",
            'dvd':"category/tamilyogi-dvdrip-movies/"}

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])


xbmcplugin.setContent(addon_handle, 'movies')

# returns url to move between tabs
def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

#
def webBuildPageURL(category,pageNumber):
    return SERVER_BASE_URL + CATEGORIES.get(category) + 'page/' + pageNumber

current_category = args.get('current_category',None)
current_level = args.get('level', 'MainMenu')
current_page = args.get('page', None)
current_movie = args.get('movie', None)

if current_level == 'MainMenu':
    for category in CATEGORIES.keys():
        url = build_url({'current_category': category, 'level': 'Folder'})
        li = xbmcgui.ListItem(category.capitalize())
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
elif current_level[0] == 'Folder':
    my_current_page = '1' if current_page is None else current_page[0]
    webPageURL = webBuildPageURL(current_category[0], my_current_page)
    movieList = getMoviesFromPage(webPageURL)

    for movieItem in movieList:
        url = build_url({'level': 'Movie', 'movieURL': movieItem.get('link')})
        li = xbmcgui.ListItem(movieItem.get('title'))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    url = build_url({'current_category': current_category[0], 'level': 'Folder', 'page': str(int(my_current_page)+1)})
    li = xbmcgui.ListItem('Next..')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)
elif current_level[0] == 'Movie':
    xbmc.log("------------------ Inside Movie -------------", level=xbmc.LOGNOTICE)
    xbmcplugin.endOfDirectory(addon_handle)

# TODO : Render Main Menu from categories

# TODO : Render List of movies from current categoryd



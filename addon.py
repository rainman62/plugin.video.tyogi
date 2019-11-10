import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmc

import resolveurl
import requests
import re

from HTMLParser import HTMLParser

counter = 0


def getCount():
    return counter


def incrementCount():
    global counter
    counter = counter + 1


def setCount(x):
    global counter
    counter = x


def getMoviesFromPage(url, queryparameter=None):
    inputHTML = requests.get(url=url, params=queryparameter).text
    inputHTML = inputHTML[inputHTML.find('id=content'):]
    returnValue = {}
    returnValueArray = []
    setCount(0)

    class MyHTMLParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag == 'a' and len(attrs) > 1 and attrs[0][0] == 'href' and attrs[1][0] == 'title':
                print "Encountered a start tag:", tag, " attribute :", attrs
                if returnValue.get(attrs[1][1]) is None:
                    returnValue[attrs[1][1]] = getCount()
                    incrementCount()
                    returnValueArray.append({'link': '', 'image': ''})
                returnValueArray[returnValue[attrs[1][1]]]['link'] = attrs[0][1]
                returnValueArray[returnValue[attrs[1][1]]]['title'] = attrs[1][1]
            elif tag == 'img' and len(attrs) > 1 and attrs[0][0] == 'src' and attrs[1][0] == 'alt':
                print "Encountered a start tag:", tag, " attribute :", attrs
                returnValueArray[returnValue[attrs[1][1]]]['image'] = attrs[0][1]

    parser = MyHTMLParser()
    parser.feed(inputHTML)
    return returnValueArray


SERVER_BASE_URL = "http://tamilyogi.vip/"
CATEGORIES = {'home': "home/",
              'new': "category/tamilyogi-full-movie-online/",
              'brrip': "category/tamilyogi-bluray-movies/",
              'dvd': "category/tamilyogi-dvdrip-movies/",
              'search': ''}

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')


# returns url to move between tabs
def build_url(query):
    return base_url + '?' + urllib.urlencode(query)


#
def webBuildPageURL(category, pageNumber):
    return SERVER_BASE_URL + CATEGORIES.get(category) + 'page/' + pageNumber


current_category = args.get('current_category', None)
current_level = args.get('level', 'MainMenu')
current_page = args.get('page', None)
current_movie = args.get('movieURL', None)
search_query = args.get('query', None)

if current_level == 'MainMenu':
    for category in CATEGORIES.keys():
        url = build_url({'current_category': category, 'level': 'Folder'})
        li = xbmcgui.ListItem(category.capitalize())
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
elif current_level[0] == 'Folder':
    query = None
    if current_category[0] == 'search':
        if search_query is None:
            query = xbmcgui.Dialog().input("Enter your search..")
        else:
            query = search_query[0]
    my_current_page = '1' if current_page is None else current_page[0]
    webPageURL = webBuildPageURL(current_category[0], my_current_page)
    movieList = getMoviesFromPage(webPageURL, None if query is None else {'s': query})

    for movieItem in movieList:
        url = build_url({'level': 'Movie', 'movieURL': movieItem['link']})
        li = xbmcgui.ListItem(label=movieItem['title'], thumbnailImage=movieItem['image'])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    # for movieItem in movieList:
    #     url = build_url({'level': 'Movie', 'movieURL': movieList[movieItem]['link']})
    #     li = xbmcgui.ListItem(label = movieItem, thumbnailImage = movieList[movieItem]['image'])
    #     xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    url = build_url({'current_category': current_category[0], 'level': 'Folder', 'page': str(int(my_current_page) + 1),
                     'query': query})
    li = xbmcgui.ListItem('Next..')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)
elif current_level[0] == 'Movie':
    my_current_movieURL = current_movie[0]
    inputHTML = requests.get(my_current_movieURL).text
    videoList = resolveurl.scrape_supported(inputHTML, regex='''=\s*['"]([^'"]+)''')

    inputHTML2 = requests.request('GET', my_current_movieURL, headers={
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36'}).text
    videoList2 = resolveurl.scrape_supported(inputHTML2, regex='''=\s*['"]([^'"]+)''')

    for video in videoList:
        playableURL = str(resolveurl.resolve(video))
        if playableURL != 'False':
            li = xbmcgui.ListItem(video)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=playableURL, listitem=li)

    for video in videoList2:
        playableURL = str(resolveurl.resolve(video))
        if playableURL != 'False':
            li = xbmcgui.ListItem(video)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=playableURL, listitem=li)

    xbmcplugin.endOfDirectory(addon_handle)

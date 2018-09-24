import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmc

import ListMenu

SERVER_BASE_URL = "http://tamilyogi.cc"
CATEGORIES = {'home': "/home/",
            'new':"/category/tamilyogi-full-movie-online/",
            'brrip':"/category/tamilyogi-bluray-movies/",
            'dvd':"/category/tamilyogi-dvdrip-movies/"}

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmc.log(sys.argv[2], level=xbmc.LOGNOTICE)
xbmc.log(sys.argv[2][1:], level=xbmc.LOGNOTICE)

xbmcplugin.setContent(addon_handle, 'movies')

# returns url to move between tabs
def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

current_category = args.get('category',None)

if current_category is None:
    for category in CATEGORIES.keys():
        url = build_url({'current_category': CATEGORIES.get(category)})
        li = xbmcgui.ListItem(category.capitalize())
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
else:
    current_page = args.get('page',1)
    if current_category == 'home':
        ListMenu.myfunction()
    elif current_category == 'new':
        ListMenu.myfunction()
    elif current_category == 'brrip':
        ListMenu.myfunction()
    elif current_category == 'dvd':
        ListMenu.myfunction()
# TODO : Render Main Menu from categories

# TODO : Render List of movies from current categoryd



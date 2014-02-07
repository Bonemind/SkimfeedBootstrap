from bs4 import BeautifulSoup
import simplejson as json
import httplib
import sys

# The skimfeed url
globalUrl = "skimfeed.com"
linkPrefix = "http://skimfeed.com/"

#build an httplib connection and request
request = httplib.HTTPConnection(globalUrl)
request.request("GET", "/")
response = request.getresponse()

# Check if everything went well, if not, return
if response.status != 200:
    print("Request failed: " + str(response.status) + " " + response.reason)
    sys.exit()

#read the actual data and let beautifulsoup parse it
data = response.read()
soup = BeautifulSoup(data)
feedlist = [] 

#Traverse the tree and fetch the items and site
#Fetch all divs that have the class boxes, those contain the title and links
for site in soup.find_all("div", attrs={"class":"boxes"}):
    feed = {"title":"","url":"", "items":[]}
    feed["title"] = site.h3.a.text
    feed["url"] = site.h3.a["href"]
    items = []
    #Items are stored in an ul, so we need all li elements
    for item in site.ul.find_all("li"):
        itemTitle = item.a["title"].encode('utf-8', errors="replace")
        itemUrl = item.a["href"].encode('utf-8', errors="replace")
        items.append({"title":itemTitle, "url":linkPrefix + itemUrl})

    #Add items to current feed item, the append the current feed to the total feed list
    feed["items"] = items
    feedlist.append(feed)
       
#json output
print(json.dumps(feedlist, sort_keys=False, indent=4*' '))



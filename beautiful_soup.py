from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "https://www.nytimes.com/2017/11/20/t-magazine/travel/cap-ferret-guide.html"
bs = BeautifulSoup(urlopen(url))

metatag_img = bs.find("meta", {"property": "og:image"})
metatag_title = bs.find("meta", {"property": "og:title"})
metatag_head_title = bs.find("title")

if metatag_img is not None:
    print (metatag_img["content"])

if metatag_title is not None:
    print (metatag_title["content"])

if metatag_head_title is not None:
    print (metatag_head_title)

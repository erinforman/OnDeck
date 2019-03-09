from urllib.request import urlopen
from bs4 import BeautifulSoup


# url = "https://www.nytimes.com/2017/11/20/t-magazine/travel/cap-ferret-guide.html"

def beautiful_soup(url):

    return BeautifulSoup(urlopen(url),features="html.parser")

def search_url_image(url):

    metatag_img = beautiful_soup(url).find("meta", {"property": "og:image"})

    if metatag_img:
        return metatag_img["content"]

def search_url_title(url):

    metatag_title = beautiful_soup(url).find("meta", {"property": "og:title"})

    if metatag_title:
        return metatag_title["content"]

def search_url_head_title(url):

    metatag_head_title = beautiful_soup(url).find("title")
    
    if metatag_head_title:
        return metatag_head_title 

def search_url_author(url):

    metatag_author = beautiful_soup(url).find("meta", {"property": "article:author"})

    if metatag_author:
        return metatag_author["content"]

def search_url_site_name(url):

    metatag_site_name = beautiful_soup(url).find("meta", {"property": "og:site_name"})

    if metatag_site_name:
        return metatag_site_name["content"]

def search_url_twitter(url):

    metatag_twitter = beautiful_soup(url).find("meta", {"name": "twitter:domain"})

    if metatag_twitter:
        return metatag_twitter["content"]



# metatag_img = bs.find("meta", {"property": "og:image"})
# metatag_title = bs.find("meta", {"property": "og:title"})
# metatag_head_title = bs.find("title")
# metatag_author = bs.find("meta", {"property": "article:author"})
# metatag_site_name = bs.find("meta", {"property": "og:site_name"})
# metatag_twitter = bs.find("meta", {"name": "twitter:domain"})


# if metatag_img is not None:
#     print (metatag_img["content"])

# if metatag_title is not None:
#     print (metatag_title["content"])

# if metatag_head_title is not None:
#     print (metatag_head_title)

# if metatag_author is not None:
#     print (metatag_author["content"])

# if metatag_site_name is not None:
#     print (metatag_site_name["content"])

# if metatag_twitter is not None:
#     print (metatag_twitter["content"])

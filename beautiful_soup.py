from urllib.request import urlopen
from bs4 import BeautifulSoup


# url = "https://www.nytimes.com/2017/11/20/t-magazine/travel/cap-ferret-guide.html"

def beautiful_soup(url):

    try:
        bs_url_open = BeautifulSoup(urlopen(url),features="html.parser")
    except:
        return
    else:
        return bs_url_open

def search_url_image(url):

    try:
        metatag_img = beautiful_soup(url).find("meta", {"property": "og:image"})
        url_image = metatag_img["content"]
    except:
        return
    else:
        return url_image

def search_url_title(url):

    try:
        metatag_title = beautiful_soup(url).find("meta", {"property": "og:title"})
        url_title = metatag_title["content"]
    except:
        return
    else:
        return url_title

def search_url_head_title(url):

    try:
        metatag_head_title = beautiful_soup(url).find("title")
    except:
        return
    else:
        return metatag_head_title 

def search_url_author(url):

    try:
        metatag_author = beautiful_soup(url).find("meta", {"property": "article:author"})
        url_author = metatag_author["content"]
    except:
        return
    else:
        return metatag_author

def search_url_site_name(url):

    try:
        metatag_site_name = beautiful_soup(url).find("meta", {"property": "og:site_name"})
        url_site_name = metatag_site_name["content"]
    except:
        return
    else:
        return url_site_name

def search_url_twitter(url):

    try:
        metatag_twitter = beautiful_soup(url).find("meta", {"name": "twitter:domain"})
        url_twitter = metatag_twitter["content"]
    except:
        return
    else:
        return url_twitter

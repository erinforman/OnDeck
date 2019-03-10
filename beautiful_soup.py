import requests
from bs4 import BeautifulSoup
# from urllib.request import urlopen

headers = {'User-Agent':'Mozilla/5.0'}

# url = "https://www.nytimes.com/2017/11/20/t-magazine/travel/cap-ferret-guide.html"

def beautiful_soup(url):

    try:
        # bs_url_open = BeautifulSoup(urlopen(url),features="html.parser")
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
    except:
        return
    else:
        return soup

##############################################################################

def search_url_image(url, soup):

    try:
        metatag_img = soup.find("meta", {"property": "og:image"})
        url_image = (metatag_img["content"]).strip()
    except:
        return
    else:
        return url_image

def search_url_title(url, soup):

    try:
        metatag_title = soup.find("meta", {"property": "og:title"})
        url_title = (metatag_title["content"]).strip()
    except:
        return
    else:
        return url_title

def search_url_head_title(url, soup):

    try:
        """Result: <title> UKAHT - Visiting Port Lockroy</title> """
        metatag_head_title = soup.find("title")
        url_head_title = (metatag_head_title.get_text()).strip()
    except:
        return
    else:
        return url_head_title

def search_url_author(url, soup):

    try:
        metatag_author = soup.find("meta", {"property": "article:author"})
        url_author = (metatag_author["content"]).strip()
    except:
        return
    else:
        return str(metatag_author)

def search_url_site_name(url, soup):

    try:
        metatag_site_name = soup.find("meta", {"property": "og:site_name"})
        url_site_name = (metatag_site_name["content"]).strip()
    except:
        return
    else:
        return url_site_name

def search_url_twitter(url, soup):

    try:
        metatag_twitter = soup.find("meta", {"name": "twitter:domain"})
        url_twitter = (metatag_twitter["content"]).strip()
    except:
        return
    else:
        return url_twitter




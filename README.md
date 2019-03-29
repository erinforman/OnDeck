# Via

Via is the travel app that turns wanderlust into action.
* Save travel recommendations and resources.
* Create a bucket list travel map.
* Plan custom itineraries.

![Via Homepage](/static/images/README/1_live_home.gif)

***

# technologies

* Python
* PostgreSQL + SQLAlchemy
* Flask + Jinja
* JavaScript
* jQuery
* Bootstrap + CSS + HTML

# APIs

* Google Maps
* Google Geocoding
* Google Places
* SendGrid

(dependencies are listed in requirements.txt)

***

# about the developer

Erin's inspiration for this app came from wanting to solve 3 problems:

1. Saving bucket list travel destinations alongside the resource or person that recommended them.
2. Effortlessly creating itineraries that take the most efficient route between destinations.
3. Sharing itineraries and resources with friends.

This app is <i>basically</i> scientifically proven to increase happiness: [What a Great Trip! And I’m Not Even There Yet - NYT](https://www.nytimes.com/2014/05/11/travel/what-a-great-trip-and-im-not-even-there-yet.html).


Connect on LinkedIn [here](https://www.linkedin.com/in/formanerin/).

***

# features

<strong>Generate</strong> a latitude and longitude for urls for travel destinations, like travel blogs, city features in magazines, and restaurant websites, using the Google Geocoding API. Save destinations to a postgres database via SQLAlchemy, which the Google Maps API uses to generate individual markers.

![Via Article](/static/images/README/3_live_santa_fe.gif)

<strong>Populate</strong> a photo and article hyperlink in the info window using the Beautiful Soup library in Python to scrape xml.

![3](/static/images/README/3.png)
![1](/static/images/README/1.png)
![2](/static/images/README/2.png)

<strong>Create</strong> custom itineraries with the Google Distance Matrix API. With an algorithm based on the Traveling Salesman Problem, Via creates an efficient trip itinerary from saved destinations

![Via Itinerary 1](/static/images/README/4_live_itinerary_1.gif)

<strong>Share</strong> an itinerary via e-mail using the SendGrid API. 

<p align="center"><img src="/static/images/README/9.png" width="400">  <img src="/static/images/README/10.png" width="400"></p>

<strong>Helpful error handling</strong> to progress the user forward.

![Via Itinerary 2](/static/images/README/5_live_itinerary_1.gif)

<strong>Manage</strong> all locations.

![13](/static/images/README/13.png)


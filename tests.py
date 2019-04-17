import unittest, location_search, beautiful_soup, distance_matrix

from server import app
from model import db, connect_to_db #example_data,


class TestFlaskRoutes(unittest.TestCase):
    """Test Flask routes and settings."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Test GET requests."""

         # Use the test client to make requests
        result = self.client.get("/")
        self.assertIn(b"Email", result.data)

    # def test_login(self):
    #     """Test login page."""

    #     result = self.client.post("/login",
    #                               data={"user_id": "rachel", "password": "123"},
    #                               follow_redirects=True)
    #     self.assertIn(b"You are a valued user", result.data)

    #data is a dictionary of form key/value pairs
    #result.data is the response string (html)

    # def test_favorite_color_form(self):
    #     """Test POST requests."""
    # """Test that /fav-color route processes form data correctly."""

    # client = server.app.test_client()
    #To pass data in a GET request, instead of data use query_string:
    # result = client.post('/fav-color', data={'color': 'blue'})

    # self.assertIn(b'Woah! I like blue, too', result.data)

    # def test_index(self):
    #     """Make sure index page returns correct HTML."""

    #     # Create a test client
    #     client = server.app.test_client()

    #     # Use the test client to make requests
    #     result = client.get('/')

    #     # Compare result.data with assert method
    #     self.assertIn(b'<h1>Color Form</h1>', result.data)
 # def test_some_flask_route(self):
 #      """Some non-database test..."""

 #      result = self.client.get("/my-route")
 #      self.assertEqual(result.status_code, 200)
 #      self.assertIn('<h1>Test</h1>', result.data)


class TestLocationSearch(unittest.TestCase):
    """Tests for geocoding URLs"""
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_search_url(self):

        self.assertEqual(location_search.search_url('https://www.papernstitchblog.com/jacksonville-florida-travel-guide/'), location_search.Search(location='no location', match_type='no match type'))

    def test_search_cleaned_url(self):
        
        self.assertEqual(location_search.search_cleaned_url('https://www.papernstitchblog.com/jacksonville-florida-travel-guide/') 
            , location_search.Search(location={'address_components': [{'long_name': 'Jacksonville', 'short_name': 'Jacksonville', 
                'types': ['locality', 'political']}, {'long_name': 'Duval County', 'short_name': 'Duval County', 
                'types': ['administrative_area_level_2', 'political']}, {'long_name': 'Florida', 'short_name': 'FL', 
                'types': ['administrative_area_level_1', 'political']}, {'long_name': 'United States', 'short_name': 'US', 
                'types': ['country', 'political']}], 'formatted_address': 'Jacksonville, FL, USA', 
                'geometry': {'bounds': {'northeast': {'lat': 30.586232, 'lng': -81.316712}, 
                'southwest': {'lat': 30.103748, 'lng': -82.0495018}}, 'location': {'lat': 30.3321838, 'lng': -81.65565099999999}, 
                'location_type': 'APPROXIMATE', 'viewport': {'northeast': {'lat': 30.586232, 'lng': -81.316712}, 
                'southwest': {'lat': 30.103748, 'lng': -82.0495018}}}, 'partial_match': True, 'place_id': 'ChIJ66_O8Ra35YgR4sf8ljh9zcQ', 
                'types': ['locality', 'political']}, match_type='exact')
            )

class TestBeautifulSoup(unittest.TestCase):
    """Tests for web scraping articles with beautiful soup library"""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_search_url_image(self):
        """Test serch url image function"""

        url = ('https://www.nytimes.com/2017/11/20/t-magazine/travel/cap-ferret-'
            'guide.html')
        soup = beautiful_soup.beautiful_soup(url)

        self.assertEqual(beautiful_soup.search_url_image(url, soup), 
            'https://static01.nyt.com/images/2017/11/14/t-magazine/tmag-capferr'
            'et-slide-KFLI/tmag-capferret-slide-KFLI-facebookJumbo.jpg')

    def test_search_url_title(self):
        """Test serch url title function"""

        url = ('https://www.vogue.com/article/santa-fe-travel-guide-restaurant'
            's-art-hotels?verso=true')
        soup = beautiful_soup.beautiful_soup(url)

        self.assertEqual(beautiful_soup.search_url_title(url, soup), 
            'Looking For a Serene Winter Escape? Try Santa Fe')

class TestDistanceMatrix(unittest.TestCase):
    """Tests for creating itineraries"""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_get_next_trip(self):
        """Test get next trip function"""
        user_id = 3
        #Goudier Island,Wiencke Island, Antarctica | Port Lockroy
        origin_place_id = 'ChIJo5paBStFf7wR7OLZjeVFeGQ'
        excluded_destinations = []

        self.assertEqual(distance_matrix.get_next_trip(user_id, origin_place_id, 
            excluded_destinations), None)

    # def test_create_itinerary(self):

    #     user_id = 3
    #     #http://danielfooddiary.com/2014/01/23/ippudotokyo/
    #     origin_place_id = 'ChIJV0AwM30rDogR2sd-X0cgErU'
    #     #'ChIJ51cu8IcbXWARiRtXIothAS4'
    #     # origin_place_id ='ChIJo5paBStFf7wR7OLZjeVFeGQ'
    #     duration = 3000

    #     self.assertEqual(distance_matrix.create_itinerary(user_id,
    #         origin_place_id, duration), None)



if __name__ == "__main__":
    unittest.main()

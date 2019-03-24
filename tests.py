import unittest, location_search

from server import app
from model import db, connect_to_db #example_data,


class Tests(unittest.TestCase):
    """Tests for site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn(b"Email", result.data)

class TestLocationSearch(unittest.TestCase):
    """Tests for geocoding URLs"""

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

if __name__ == "__main__":
    unittest.main()

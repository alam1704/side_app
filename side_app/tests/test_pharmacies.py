import unittest
from main import create_app
from dotenv import load_dotenv
import os

# we need our environment variables
# Flask gets them for us, but unittest doesn't
# so we load them in manually
load_dotenv()

# Since we are running tests, let's set the FLASK_ENV to testing
os.environ["FLASK_ENV"]="testing"

class TestPharmacies(unittest.TestCase):
    # The setup function runs before each test to prepare for them
    def setUp(self):
        # need to create an app instance to test
        self.app = create_app()
        # the app instance has a handy test_client function
        # this generates an imaginary browser that can make requests
        self.client = self.app.test_client()
    
    def test_pharmacy_index(self):
        # we use the client to make a request
        response = self.client.get("/pharmacies/")
        data = response.get_json()
        
        # Now we can perform tests on the response
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
import unittest
import warnings
from api import app

class MyAppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()
        
        warnings.simplefilter("ignore", category=DeprecationWarning)

    def test_getcustomers(self):
        response = self.app.get("/customers")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Distinctio fugiat iure rerum dicta earum odio" in response.data.decode())

    def test_getcustomers_by_id(self):
        response = self.app.get("/customers/5")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Incidunt fugiat ut molestias illum voluptatem" in response.data.decode())

if __name__ == "__main__":
    unittest.main()
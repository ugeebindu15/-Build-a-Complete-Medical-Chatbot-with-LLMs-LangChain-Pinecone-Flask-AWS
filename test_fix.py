import unittest
from app import app

class TestChatEndpoint(unittest.TestCase):
    def setUp(self):
        # Set up the test client
        self.app = app.test_client()
        self.app.testing = True

    # Test case 1: Happy path — fix works as expected
    # This test verifies that a valid non-empty, non-whitespace query is processed correctly.
    def test_valid_query(self):
        response = self.app.post('/get', data={'msg': 'Hello, how are you?'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Response :', response.data.decode())

    # Test case 2: Edge case — boundary condition
    # This test verifies that a query with only whitespace characters returns a 400 error.
    def test_whitespace_query(self):
        response = self.app.post('/get', data={'msg': '   '})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Query cannot be empty or whitespace only"})

    # Test case 3: Regression test — the original bug no longer occurs
    # This test verifies that an empty string query returns a 400 error, ensuring the original bug is fixed.
    def test_empty_query(self):
        response = self.app.post('/get', data={'msg': ''})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Query cannot be empty or whitespace only"})

if __name__ == '__main__':
    unittest.main()
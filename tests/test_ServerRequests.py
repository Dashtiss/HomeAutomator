import unittest
import logging
from unittest.mock import patch
from moonraker._ServerRequests import ServerRequests

logging.basicConfig(level=logging.INFO)

class TestServerRequests(unittest.TestCase):

    def setUp(self):
        self.server_requests = ServerRequests("http://example.com/server/")
        logging.info("Setup complete")

    @patch('moonraker._ServerRequests.requests.get')
    def test_info(self, mock_get):
        logging.info("Testing info method")
        mock_get.return_value.json.return_value = {"info": "test"}
        mock_get.return_value.raise_for_status = lambda: None
        result = self.server_requests.info()
        self.assertEqual(result, {"info": "test"})
        logging.info("info method passed")

    @patch('moonraker._ServerRequests.requests.get')
    def test_config(self, mock_get):
        logging.info("Testing config method")
        mock_get.return_value.json.return_value = {"config": "test"}
        mock_get.return_value.raise_for_status = lambda: None
        result = self.server_requests.config()
        self.assertEqual(result, {"config": "test"})
        logging.info("config method passed")

    @patch('moonraker._ServerRequests.requests.get')
    def test_temperature(self, mock_get):
        logging.info("Testing temperature method")
        mock_get.return_value.json.return_value = {"temperature": "test"}
        mock_get.return_value.raise_for_status = lambda: None
        result = self.server_requests.temperature()
        self.assertEqual(result, {"temperature": "test"})
        logging.info("temperature method passed")

    @patch('moonraker._ServerRequests.requests.get')
    def test_cached_gcode(self, mock_get):
        logging.info("Testing cached_gcode method")
        mock_get.return_value.json.return_value = {"gcode": "test"}
        mock_get.return_value.raise_for_status = lambda: None
        result = self.server_requests.cached_gcode()
        self.assertEqual(result, {"gcode": "test"})
        logging.info("cached_gcode method passed")

if __name__ == '__main__':
    unittest.main()

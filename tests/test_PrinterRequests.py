import unittest
import logging
from unittest.mock import patch
from moonraker._PrinterRequests import PrinterRequests

logging.basicConfig(level=logging.INFO)

class TestPrinterRequests(unittest.TestCase):

    def setUp(self):
        self.printer_requests = PrinterRequests("http://example.com/printer/")
        logging.info("Setup complete")

    @patch('moonraker._PrinterRequests.requests.get')
    def test_info(self, mock_get):
        logging.info("Testing info method")
        mock_get.return_value.json.return_value = {"info": "test"}
        mock_get.return_value.raise_for_status = lambda: None
        result = self.printer_requests.info()
        self.assertEqual(result, {"info": "test"})
        logging.info("info method passed")

    @patch('moonraker._PrinterRequests.requests.post')
    def test_emergency_stop(self, mock_post):
        logging.info("Testing emergencyStop method")
        mock_post.return_value.json.return_value = {"status": "stopped"}
        mock_post.return_value.raise_for_status = lambda: None
        result = self.printer_requests.emergencyStop()
        self.assertEqual(result, {"status": "stopped"})
        logging.info("emergencyStop method passed")

    @patch('moonraker._PrinterRequests.requests.get')
    def test_list_objects(self, mock_get):
        logging.info("Testing listObjects method")
        mock_get.return_value.json.return_value = [{"object": "test"}]
        mock_get.return_value.raise_for_status = lambda: None
        result = self.printer_requests.listObjects()
        self.assertEqual(result, [{"object": "test"}])
        logging.info("listObjects method passed")

    @patch('moonraker._PrinterRequests.requests.post')
    def test_run_gcode(self, mock_post):
        logging.info("Testing runGCode method")
        mock_post.return_value.json.return_value = {"result": "ok"}
        mock_post.return_value.raise_for_status = lambda: None
        result = self.printer_requests.runGCode("G28")
        self.assertEqual(result, {"result": "ok"})
        logging.info("runGCode method passed")

    @patch('moonraker._PrinterRequests.requests.get')
    def test_get_gcode_help(self, mock_get):
        logging.info("Testing getGCodeHelp method")
        mock_get.return_value.json.return_value = {"help": "test"}
        mock_get.return_value.raise_for_status = lambda: None
        result = self.printer_requests.getGCodeHelp()
        self.assertEqual(result, {"help": "test"})
        logging.info("getGCodeHelp method passed")

if __name__ == '__main__':
    unittest.main()

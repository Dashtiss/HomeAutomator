import unittest
import logging
from unittest.mock import MagicMock
from Tools import MoonrakerTools

logging.basicConfig(level=logging.INFO)

class TestMoonrakerTools(unittest.TestCase):

    def setUp(self):
        self.url = "http://example.com"
        self.tools = MoonrakerTools(self.url)
        self.tools.moonraker.printer = MagicMock()
        self.tools.moonraker.server = MagicMock()
        self.tools.moonraker.server.files = MagicMock()
        logging.info("Setup complete")

    def test_get_tools(self):
        logging.info("Testing get_tools method")
        self.tools.moonraker.printer.some_method = MagicMock()
        self.tools.moonraker.server.some_method = MagicMock()
        self.tools.moonraker.server.files.some_method = MagicMock()
        
        tools = self.tools.get_tools()
        
        self.assertTrue(any(tool['function']['name'].startswith('printer_') for tool in tools))
        self.assertTrue(any(tool['function']['name'].startswith('server_') for tool in tools))
        self.assertTrue(any(tool['function']['name'].startswith('server.files_') for tool in tools))
        logging.info("get_tools method passed")

    def test_getFunc_printer(self):
        logging.info("Testing getFunc method for printer")
        tool = {
            "function": {
                "name": "printer_some_method"
            }
        }
        self.tools.moonraker.printer.some_method = MagicMock()
        func = self.tools.getFunc(tool)
        self.assertEqual(func, self.tools.moonraker.printer.some_method)
        logging.info("getFunc method for printer passed")

    def test_getFunc_server(self):
        logging.info("Testing getFunc method for server")
        tool = {
            "function": {
                "name": "server_some_method"
            }
        }
        self.tools.moonraker.server.some_method = MagicMock()
        func = self.tools.getFunc(tool)
        self.assertEqual(func, self.tools.moonraker.server.some_method)
        logging.info("getFunc method for server passed")

    def test_getFunc_server_files(self):
        logging.info("Testing getFunc method for server files")
        tool = {
            "function": {
                "name": "server.files_some_method"
            }
        }
        self.tools.moonraker.server.files.some_method = MagicMock()
        func = self.tools.getFunc(tool)
        self.assertEqual(func, self.tools.moonraker.server.files.some_method)
        logging.info("getFunc method for server files passed")

if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import patch, Mock
from isy.eisy import EISY

class TestEISY(unittest.TestCase):
    def setUp(self):
        self.url = "http://192.168.1.105:8080/"
        self.username = "admin"
        self.password = "password"
        self.eisy = EISY(self.url, self.username, self.password)

    @patch('isy.eisy.requests.get')
    def test_get_nodes(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        with open('c:\\Users\\brand\\Documents\\HomeAutomated\\nodes.json') as f:
            mock_response.content = f.read()
        mock_get.return_value = mock_response

        nodes = self.eisy.get_nodes()
        self.assertIn("1D 39 A6 1", nodes)
        self.assertEqual(nodes["1D 39 A6 1"]["name"], "Front Porch")

    @patch('isy.eisy.requests.get')
    def test_get_scenes(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        with open('c:\\Users\\brand\\Documents\\HomeAutomated\\scenes.json') as f:
            mock_response.content = f.read()
        mock_get.return_value = mock_response

        scenes = self.eisy.get_scenes()
        self.assertIn("00:21:b9:02:61:23", scenes)
        self.assertEqual(scenes["00:21:b9:02:61:23"]["name"], "ISY")

    @patch('isy.eisy.requests.get')
    def test_get_location(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = '<DT><Lat>37.7749</Lat><Long>-122.4194</Long></DT>'
        mock_get.return_value = mock_response

        location = self.eisy._getLocation()
        self.assertEqual(location, ("37.7749", "-122.4194"))

    @patch('isy.eisy.requests.post')
    def test_enable_node(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        result = self.eisy.enable_node("1D 39 A6 1")
        self.assertTrue(result)

    @patch('isy.eisy.requests.post')
    def test_disable_node(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        result = self.eisy.disable_node("1D 39 A6 1")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()

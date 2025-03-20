import requests
from requests.auth import HTTPBasicAuth
import xmltodict
import json
import logging
import xml
from typing import Optional

logger = logging.getLogger(__name__)

class EISY:
    """
    A class to interact with the EISY REST API for managing nodes, scenes, programs, and more.
    """

    def __init__(self, url: str, username: str, password: str) -> None:
        """
        Initializes the EISY instance with authentication details and fetches initial data.
        
        :param url: Base URL of the EISY REST API
        :param username: Username for authentication
        :param password: Password for authentication
        """
        if not (url.startswith('http://') or url.startswith('https://')):
            raise ValueError("URL must start with http:// or https://")
        if url[-1] != '/':
            url += '/'
        if not url.endswith('rest/'):
            url += 'rest/'
        self.url = url

        self.username = username
        self.password = password
        self.auth = HTTPBasicAuth(username, password)
        self.nodes = self.get_nodes()
        self.location = self._getLocation()
        self.scenes = self.get_scenes()

    def _getLocation(self) -> Optional[tuple[float, float]]:
        """
        Retrieves the geographic location (latitude and longitude) from the EISY system.

        :return: Tuple of latitude and longitude or None if an error occurs
        """
        response = requests.get(self.url + "time", auth=self.auth)
        if response.status_code == 200:
            try:
                data = xmltodict.parse(response.content)
                return float(data["DT"]["Lat"]), float(data["DT"]["Long"])
            except (xml.parsers.expat.ExpatError, KeyError):
                logger.error("Error parsing XML")
                try:
                    data = json.loads(response.content)
                    return float(data["Lat"]), float(data["Long"])
                except (json.JSONDecodeError, KeyError):
                    logger.error("Error parsing JSON")
                    return None
        return None

    def get_nodes(self) -> Optional[dict[str, dict]]:
        """
        Retrieves all nodes from the EISY system.

        :return: Dictionary of nodes with their addresses as keys or None if an error occurs
        """
        response = requests.get(self.url + "nodes", auth=self.auth)
        if response.status_code == 200:
            try:
                data = xmltodict.parse(response.content)
                nodes = {node["address"]: node for node in data["nodes"]["node"]}
                return nodes
            except (xml.parsers.expat.ExpatError, KeyError):
                logger.error("Error parsing XML")
                try:
                    data = json.loads(response.content)
                    nodes = {node["address"]: node for node in data["nodes"]["node"]}
                    return nodes
                except (json.JSONDecodeError, KeyError):
                    logger.error("Error parsing JSON")
                    return None
        return None

    def get_scenes(self) -> Optional[dict[str, dict]]:
        """
        Retrieves all scenes from the EISY system.

        :return: Dictionary of scenes with their addresses as keys or None if an error occurs
        """
        response = requests.get(self.url + "nodes/scenes", auth=self.auth)
        if response.status_code == 200:
            try:
                data = xmltodict.parse(response.content)
                scenes = {scene["address"]: scene for scene in data["nodes"]["group"]}
                return scenes
            except (xml.parsers.expat.ExpatError, KeyError):
                logger.error("Error parsing XML")
                try:
                    data = json.loads(response.content)
                    scenes = {scene["address"]: scene for scene in data["nodes"]["group"]}
                    return scenes
                except (json.JSONDecodeError, KeyError):
                    logger.error("Error parsing JSON")
                    return None
        return None

    def get_Notes(self, node_id: str) -> Optional[list[dict]]:
        """
        Retrieves notes for a specific node.

        :param node_id: ID of the node
        :return: List of notes or None if an error occurs
        """
        response = requests.get(self.url + f"node/{node_id}/notes", auth=self.auth)
        if response.status_code == 200:
            try:
                data = xmltodict.parse(response.content)
                return data["notes"]["note"]
            except (xml.parsers.expat.ExpatError, KeyError):
                logger.error("Error parsing XML")
                try:
                    data = json.loads(response.content)
                    return data.get("note", [])
                except (json.JSONDecodeError, KeyError):
                    logger.error("Error parsing JSON")
                    return None
        return None

    def enable_node(self, node_id: str) -> bool:
        """
        Enables a specific node.

        :param node_id: ID of the node
        :return: True if the node was successfully enabled, False otherwise
        """
        response = requests.post(self.url + f"node/{node_id}/enable", auth=self.auth)
        return response.status_code == 200

    def disable_node(self, node_id: str) -> bool:
        """
        Disables a specific node.

        :param node_id: ID of the node
        :return: True if the node was successfully disabled, False otherwise
        """
        response = requests.post(self.url + f"node/{node_id}/disable", auth=self.auth)
        return response.status_code == 200

    def get_programs(self) -> Optional[list[dict]]:
        """
        Retrieves all programs from the EISY system.

        :return: List of programs or None if an error occurs
        """
        response = requests.get(self.url + "programs", auth=self.auth)
        if response.status_code == 200:
            try:
                data = xmltodict.parse(response.content)
                return data["programs"]["program"]
            except (xml.parsers.expat.ExpatError, KeyError):
                logger.error("Error parsing XML")
                try:
                    data = json.loads(response.content)
                    return data.get("program", [])
                except (json.JSONDecodeError, KeyError):
                    logger.error("Error parsing JSON")
                    return None
        return None

    def run_program(self, program_id: str) -> bool:
        """
        Runs a specific program.

        :param program_id: ID of the program
        :return: True if the program was successfully run, False otherwise
        """
        response = requests.get(self.url + f"programs/{program_id}/run", auth=self.auth)
        return response.status_code == 200

    def stop_program(self, program_id: str) -> bool:
        """
        Stops a specific program.

        :param program_id: ID of the program
        :return: True if the program was successfully stopped, False otherwise
        """
        response = requests.get(self.url + f"programs/{program_id}/stop", auth=self.auth)
        return response.status_code == 200

    def get_variables(self) -> Optional[list[dict]]:
        """
        Retrieves all variables from the EISY system.

        :return: List of variables or None if an error occurs
        """
        response = requests.get(self.url + "vars/definitions/2", auth=self.auth)
        if response.status_code == 200:
            try:
                data = xmltodict.parse(response.content)
                return data["CList"]["e"]
            except (xml.parsers.expat.ExpatError, KeyError):
                logger.error("Error parsing XML")
                try:
                    data = json.loads(response.content)
                    return data.get("e", [])
                except (json.JSONDecodeError, KeyError):
                    logger.error("Error parsing JSON")
                    return None
        return None

    def get_variable_value(self, var_id: str) -> Optional[str]:
        """
        Retrieves the value of a specific variable.

        :param var_id: ID of the variable
        :return: Value of the variable or None if an error occurs
        """
        response = requests.get(self.url + f"vars/get/2/{var_id}", auth=self.auth)
        if response.status_code == 200:
            try:
                data = xmltodict.parse(response.content)
                return data["var"]["val"]
            except (xml.parsers.expat.ExpatError, KeyError):
                logger.error("Error parsing XML")
                try:
                    data = json.loads(response.content)
                    return data.get("val")
                except (json.JSONDecodeError, KeyError):
                    logger.error("Error parsing JSON")
                    return None
        return None

    def set_variable_value(self, var_id: str, value: str) -> bool:
        """
        Sets the value of a specific variable.

        :param var_id: ID of the variable
        :param value: Value to set
        :return: True if the variable was successfully set, False otherwise
        """
        response = requests.get(self.url + f"vars/set/2/{var_id}/{value}", auth=self.auth)
        return response.status_code == 200

    def get_weather(self) -> Optional[dict]:
        """
        Retrieves the weather forecast from the EISY system.

        :return: Weather forecast data or None if an error occurs
        """
        response = requests.get(self.url + "climate", auth=self.auth)
        if response.status_code == 200:
            try:
                data = xmltodict.parse(response.content)
                return data["weather"]["forecast"]
            except (xml.parsers.expat.ExpatError, KeyError):
                logger.error("Error parsing XML")
                try:
                    data = json.loads(response.content)
                    return data.get("forecast", [])
                except (json.JSONDecodeError, KeyError):
                    logger.error("Error parsing JSON")
                    return None
        return None

    def reboot(self) -> bool:
        """
        Reboots the EISY system.

        :return: True if the system was successfully rebooted, False otherwise
        """
        response = requests.get(self.url + "reboot", auth=self.auth)
        return response.status_code == 200

    def get_status(self) -> Optional[dict]:
        """
        Retrieves the status of the EISY system.

        :return: Status data or None if an error occurs
        """
        response = requests.get(self.url + "status", auth=self.auth)
        if response.status_code == 200:
            try:
                data = xmltodict.parse(response.content)
                return data["status"]
            except (xml.parsers.expat.ExpatError, KeyError):
                logger.error("Error parsing XML")
                try:
                    data = json.loads(response.content)
                    return data
                except (json.JSONDecodeError, KeyError):
                    logger.error("Error parsing JSON")
                    return None
        return None


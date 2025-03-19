import requests
from typing import Dict, List, Optional

class PrinterRequests:
    """Class containing methods for interacting with a 3D printer over Moonraker API.

    This class provides methods for interacting with a 3D printer over the Moonraker API.
    The methods include retrieving printer information, triggering an emergency stop,
    restarting the host machine, restarting the printer firmware, listing all objects
    available on the printer, executing a G-code command on the printer, getting help
    information for G-code commands, starting a print job, pausing a print job,
    resuming a paused print job, and canceling a print job.
    """

    def __init__(self, url: str) -> None:
        """Initialize PrinterRequests with a formatted URL.

        Args:
            url (str): URL of the Moonraker API endpoint. Will be formatted to end
                with "/printer/" if it doesn't already.
        """
        # Make sure the URL ends with "/printer/"
        if url[-1] != "/":
            url += "/"
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        
        if not (url.endswith("printer") or url.endswith("printer/")):
            url += "printer/"
        
        # Save the formatted URL
        self.url = url

    def info(self) -> Optional[Dict]:
        """Retrieve printer information.

        Returns:
            Optional[Dict]: A dictionary containing information about the printer, or None if an error occurs.
        """
        try:
            # Send a GET request to the API endpoint
            response = requests.get(self.url + "info")
            # Raise an exception for any HTTP errors
            response.raise_for_status()
            # Return the JSON response
            return response.json()
        except requests.exceptions.RequestException as e:
            # Print an error message if an exception occurs
            print(f"Error: {e}")
            # Return None if an error occurs
            return None

    def emergencyStop(self) -> Optional[Dict]:
        """Trigger an emergency stop on the printer.

        Returns:
            Optional[Dict]: A dictionary containing the result of the command, or None if an error occurs.
        """
        try:
            # Send a POST request to the API endpoint
            response = requests.post(self.url + "emergency_stop")
            # Raise an exception for any HTTP errors
            response.raise_for_status()
            # Return the JSON response
            return response.json()
        except requests.exceptions.RequestException as e:
            # Print an error message if an exception occurs
            print(f"Error: {e}")
            # Return None if an error occurs
            return None

    def hostRestart(self) -> Optional[Dict]:
        """Restart the host machine.

        Returns:
            Optional[Dict]: A dictionary containing the result of the command, or None if an error occurs.
        """
        try:
            # Send a POST request to the API endpoint
            response = requests.post(self.url + "restart")
            # Raise an exception for any HTTP errors
            response.raise_for_status()
            # Return the JSON response
            return response.json()
        except requests.exceptions.RequestException as e:
            # Print an error message if an exception occurs
            print(f"Error: {e}")
            # Return None if an error occurs
            return None

    def firmwareRestart(self) -> Optional[Dict]:
        """Restart the printer firmware.

        Returns:
            Optional[Dict]: A dictionary containing the result of the command, or None if an error occurs.
        """
        try:
            # Send a POST request to the API endpoint
            response = requests.post(self.url + "firmware_restart")
            # Raise an exception for any HTTP errors
            response.raise_for_status()
            # Return the JSON response
            return response.json()
        except requests.exceptions.RequestException as e:
            # Print an error message if an exception occurs
            print(f"Error: {e}")
            # Return None if an error occurs
            return None

    def listObjects(self) -> Optional[List[Dict]]:
        """List all objects available on the printer.

        Returns:
            Optional[List[Dict]]: A list of dictionaries containing information about the objects, or None if an error occurs.
        """
        try:
            # Send a GET request to the API endpoint
            response = requests.get(self.url + "objects/list")
            # Raise an exception for any HTTP errors
            response.raise_for_status()
            # Return the JSON response
            return response.json()
        except requests.exceptions.RequestException as e:
            # Print an error message if an exception occurs
            print(f"Error: {e}")
            # Return None if an error occurs
            return None

    def runGCode(self, gcode: str) -> Optional[Dict]:
        """Execute a G-code command on the printer.

        Args:
            gcode (str): The G-code command to run.

        Returns:
            Optional[Dict]: A dictionary containing the result of the command, or None if an error occurs.
        """
        try:
            # Set the headers and parameters for the request
            headers = {
                "Content-Type": "application/json"
            }
            params = {
                "script": gcode
            }
            # Send a POST request to the API endpoint
            response = requests.post(self.url + "gcode", headers=headers, params=params)
            # Raise an exception for any HTTP errors
            response.raise_for_status()
            # Return the JSON response
            return response.json()
        except requests.exceptions.RequestException as e:
            # Print an error message if an exception occurs
            print(f"Error: {e}")
            # Return None if an error occurs
            return None

    def getGCodeHelp(self) -> Optional[Dict]:
        """Get help information for G-code commands.

        Returns:
            Optional[Dict]: A dictionary containing help information for G-code commands, or None if an error occurs.
        """
        try:
            # Send a GET request to the API endpoint
            response = requests.get(self.url + "gcode/help")
            # Raise an exception for any HTTP errors
            response.raise_for_status()
            # Return the JSON response
            return response.json()
        except requests.exceptions.RequestException as e:
            # Print an error message if an exception occurs
            print(f"Error: {e}")
            # Return None if an error occurs
            return None

    def startPrint(self, file: str) -> bool:
        """Start printing a file.

        Args:
            file (str): The name of the file to print.

        Returns:
            bool: True if the print was successfully started, False otherwise.
        """
        try:
            # Send a POST request to the API endpoint
            response = requests.post(self.url + "print/start?filename=" + file)
            # Raise an exception for any HTTP errors
            response.raise_for_status()
            # Return True if the print was successfully started, False otherwise
            return response.content == b"ok"
        except requests.exceptions.RequestException as e:
            # Print an error message if an exception occurs
            print(f"Error: {e}")
            # Return False if an error occurs
            return False

    def pausePrint(self) -> bool:
        """Pause the ongoing print.

        Returns:
            bool: True if the print was successfully paused, False otherwise.
        """
        try:
            # Send a POST request to the API endpoint
            response = requests.post(self.url + "print/pause")
            # Raise an exception for any HTTP errors
            response.raise_for_status()
            # Return True if the print was successfully paused, False otherwise
            return response.content == b"ok"
        except requests.exceptions.RequestException as e:
            # Print an error message if an exception occurs
            print(f"Error: {e}")
            # Return False if an error occurs
            return False

    def continuePrint(self) -> bool:
        """Resume the paused print.

        Returns:
            bool: True if the print was successfully resumed, False otherwise.
        """
        try:
            # Send a POST request to the API endpoint
            response = requests.post(self.url + "print/continue")
            # Raise an exception for any HTTP errors
            response.raise_for_status()
            # Return True if the print was successfully resumed, False otherwise
            return response.content == b"ok"
        except requests.exceptions.RequestException as e:
            # Print an error message if an exception occurs
            print(f"Error: {e}")
            # Return False if an error occurs
            return False

    def cancelPrint(self) -> bool:
        """Cancel the ongoing print.

        Returns:
            bool: True if the print was successfully canceled, False otherwise.
        """
        try:
            # Send a POST request to the API endpoint
            response = requests.post(self.url + "print/cancel")
            # Raise an exception for any HTTP errors
            response.raise_for_status()
            # Return True if the print was successfully canceled, False otherwise
            return response.content == b"ok"
        except requests.exceptions.RequestException as e:
            # Print an error message if an exception occurs
            print(f"Error: {e}")
            # Return False if an error occurs
            return False


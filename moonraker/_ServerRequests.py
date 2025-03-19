import requests
import hashlib
from typing import Dict, List, Optional

class ServerRequests:
    def __init__(self, url: str) -> None:
        """Initialize ServerRequests with a formatted URL.

        Args:
            url (str): URL of the Moonraker API endpoint. Will be formatted to end
                with "/server/" if it doesn't already.
        """
        if not url:
            raise ValueError("URL cannot be empty.")
        if url[-1] != "/":
            url += "/"
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        if not (url.endswith("server") or url.endswith("server/")):
            url += "server/"
        
        self.url = url
        self.files = self._Files(self.url)

    def info(self) -> Optional[Dict]:
        """Retrieve server information.

        Returns:
            Optional[Dict]: A dictionary containing information about the server, or None if an error occurs.
        """
        try:
            response = requests.get(self.url + "info")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving server information: {e}")
            return None
    
    def config(self) -> Optional[Dict]:
        """Retrieve server configuration.

        Returns:
            Optional[Dict]: A dictionary containing configuration information about the server, or None if an error occurs.
        """
        try:
            response = requests.get(self.url + "config")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving server configuration: {e}")
            return None
    
    def temperature(self, *, include_monitor: bool = False) -> Optional[Dict]:
        """Retrieve temperature information about the server.

        Args:
            include_monitor (bool): Whether to include monitor information. Defaults to False.

        Returns:
            Optional[Dict]: A dictionary containing temperature information about the server, or None if an error occurs.
        """
        try:
            response = requests.get(self.url + "temperature_store?include_monitors=" + str(include_monitor).lower())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving temperature information: {e}")
            return None
    
    def cached_gcode(self, *, count: int = 100) -> Optional[Dict]:
        """Retrieve a cached list of gcode files.

        Args:
            count (int): The number of gcode files to retrieve. Defaults to 100.

        Returns:
            Optional[Dict]: A dictionary containing information about the gcode files, or None if an error occurs.
        """
        try:
            response = requests.get(self.url + "gcode_store?count=" + str(count))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving cached gcode files: {e}")
            return None
    
    def restart_server(self) -> bool:
        """Restart the server.

        Returns:
            Optional[Dict]: A dictionary containing the result of the command, or None if an error occurs.
        """
        try:
            response = requests.post(self.url + "restart")
            response.raise_for_status()
            return response.content == "ok"
        except requests.exceptions.RequestException as e:
            print(f"Error restarting server: {e}")
            return None
    
    class _Files:
        def __init__(self, url: str) -> None:
            """Initialize _Files with a formatted URL.

            Args:
                url (str): URL of the Moonraker API endpoint. Will be formatted to end
                    with "/files/" if it doesn't already.
            """
            if not url:
                raise ValueError("URL cannot be empty.")
            self.url = url

        def get_roots(self) -> Optional[List[str]]:
            """Retrieve a list of root directories.

            Returns:
                Optional[List[str]]: A list of root directories, or None if an error occurs.
            """
            try:
                response = requests.get(self.url + "/files/roots")
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                print(f"Error retrieving root directories: {e}")
                return None
        
        def get_gcodes(self) -> Optional[List[Dict]]:
            """Retrieve a list of gcode files.

            Returns:
                Optional[List[Dict]]: A list of dictionaries containing information about the gcode files, or None if an error occurs.
            """
            try:
                response = requests.get(self.url + "/files/list?root=gcodes")
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                print(f"Error retrieving gcode files: {e}")
                return None
        
        def get_gcode_metadata(self, file_name: str) -> Optional[Dict]:
            """Retrieve metadata about a gcode file.

            Args:
                file_name (str): The name of the gcode file.

            Returns:
                Optional[Dict]: A dictionary containing metadata about the gcode file, or None if an error occurs.
            """
            try:
                response = requests.get(self.url + "/files/metadata?filename=" + file_name)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                print(f"Error retrieving gcode file metadata: {e}")
                return None
        
        def scan_gcode_metadata(self, file_name: str) -> Optional[Dict]:
            """Scan a gcode file for metadata.

            Args:
                file_name (str): The name of the gcode file.

            Returns:
                Optional[Dict]: A dictionary containing metadata about the gcode file, or None if an error occurs.
            """
            try:
                response = requests.post(self.url + "/files/metascan?filename=" + file_name)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                print(f"Error scanning gcode file metadata: {e}")
                return None
        
        def get_gcode_thumbnail(self, file_name: str) -> Optional[Dict]:
            """Retrieve a thumbnail for a gcode file.

            Args:
                file_name (str): The name of the gcode file.

            Returns:
                Optional[Dict]: A dictionary containing a thumbnail for the gcode file, or None if an error occurs.
            """
            try:
                response = requests.get(self.url + "/server/files/thumbnails?filename=" + file_name)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                print(f"Error retrieving gcode file thumbnail: {e}")
                return None
        
        def get_directory(self, path: str, *, extended: bool = False) -> Optional[List[Dict]]:
            """Retrieve a list of files in a directory.

            Args:
                path (str): The path of the directory.
                extended (bool): Whether to return extended information. Defaults to False.

            Returns:
                Optional[List[Dict]]: A list of dictionaries containing information about the files, or None if an error occurs.
            """
            try:
                response = requests.get(self.url + "/files/directory?path=" + path + "&extended=" + str(extended).lower())
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                print(f"Error retrieving directory contents: {e}")
                return None
        
        def create_directory(self, path: str) -> Optional[Dict]:
            """Create a directory.

            Args:
                path (str): The path of the directory to create.

            Returns:
                Optional[Dict]: A dictionary containing the result of the command, or None if an error occurs.
            """
            headers = {
                "Content-Type": "application/json"
            }
            params = {
                "path": path
            }
            try:
                response = requests.post(self.url + "/files/directory", headers=headers, params=params)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                print(f"Error creating directory: {e}")
                return None
        
        def delete_directory(self, path: str, *, forced: bool = False) -> Optional[Dict]:
            """Delete a directory.

            Args:
                path (str): The path of the directory to delete.
                forced (bool): Whether to force deletion. Defaults to False.

            Returns:
                Optional[Dict]: A dictionary containing the result of the command, or None if an error occurs.
            """
            try:
                response = requests.delete(self.url + "/files/directory?path=" + path + "&forced=" + str(forced).lower())
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                print(f"Error deleting directory: {e}")
                return None
        
        def move_file(self, source: str, destination: str) -> Optional[Dict]:
            """Move a file.

            Args:
                source (str): The source path of the file.
                destination (str): The destination path of the file.

            Returns:
                Optional[Dict]: A dictionary containing the result of the command, or None if an error occurs.
            """
            headers = {
                "Content-Type": "application/json"
            }
            params = {
                "source": source,
                "dest": destination
            }
            try:
                response = requests.post(self.url + "/files/move", headers=headers, params=params)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                print(f"Error moving file: {e}")
                return None
        
        def copy_file(self, source: str, destination: str) -> Optional[Dict]:
            """Copy a file.

            Args:
                source (str): The source path of the file.
                destination (str): The destination path of the file.

            Returns:
                Optional[Dict]: A dictionary containing the result of the command, or None if an error occurs.
            """
            headers = {
                "Content-Type": "application/json"
            }
            params = {
                "source": source,
                "dest": destination
            }
            try:
                response = requests.post(self.url + "/files/copy", headers=headers, params=params)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                print(f"Error copying file: {e}")
                return None
        
        def create_zip(self, dest: str, files: List[str], *, store_only: bool = False) -> Optional[Dict]:
            """Create a zip file.

            Args:
                dest (str): The destination path of the zip file.
                files (List[str]): A list of files to include in the zip file.
                store_only (bool): Whether to store the zip file only. Defaults to False.

            Returns:
                Optional[Dict]: A dictionary containing the result of the command, or None if an error occurs.
            """
            headers = {
                "Content-Type": "application/json"
            }
            params = {
                "dest": dest,
                "items": files,
                "store_only": store_only
            }
            try:
                response = requests.post(self.url + "/files/zip", headers=headers, params=params)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                print(f"Error creating zip file: {e}")
                return None
        
        def download_file(self, file_path: str) -> Optional[bytes]:
            """Download a file.

            Args:
                file_path (str): The path of the file to download.

            Returns:
                Optional[bytes]: The contents of the file, or None if an error occurs.
            """
            try:
                root = file_path.split("/")[0]
                file_name = file_path.split("/")[1]
                response = requests.get(self.url + f"/files/{root}/{file_name}")
                response.raise_for_status()
                return response.content
            except requests.exceptions.RequestException as e:
                print(f"Error downloading file: {e}")
                return None
        
        def upload_file(self, url: str, file_path: str, root: str = 'gcodes', path: str = None, checksum: str = None, print_file: bool = False) -> Optional[Dict]:
            """Upload a file.

            Args:
                url (str): The URL of the API endpoint.
                file_path (str): The path of the file to upload.
                root (str): The root directory of the file. Defaults to 'gcodes'.
                path (str): The path of the file in the root directory. Defaults to None.
                checksum (str): The checksum of the file. Defaults to None.
                print_file (bool): Whether to print the file after upload. Defaults to False.

            Returns:
                Optional[Dict]: A dictionary containing the result of the command, or None if an error occurs.
            """
            try:
                with open(file_path, 'rb') as file:
                    file_data = file.read()
                    if checksum is None:
                        checksum = hashlib.sha256(file_data).hexdigest()
                    files = {'file': (file.name, file_data, 'application/octet-stream')}
                    data = {
                        'root': root,
                        'checksum': checksum,
                        'print': str(print_file).lower()
                    }
                    if path:
                        data['path'] = path
                    response = requests.post(url, files=files, data=data)
                    response.raise_for_status()
                    return response.json()
            except FileNotFoundError:
                print(f"File not found: {file_path}")
                return None
            except requests.exceptions.RequestException as e:
                print(f"Error uploading file: {e}")
                return None
        
        def file_delete(self, file_path: str) -> Optional[Dict]:
            """Delete a file.

            Args:
                file_path (str): The path of the file to delete.

            Returns:
                Optional[Dict]: A dictionary containing the result of the command, or None if an error occurs.
            """
            try:
                response = requests.delete(self.url + "/files/delete?file=" + file_path)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                print(f"Error deleting file: {e}")
                return None


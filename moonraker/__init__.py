from ._ServerRequests import ServerRequests as server
from ._PrinterRequests import PrinterRequests as printer

class Moonraker:
    def __init__(self, url: str) -> None:
        self.printer = printer(url)
        self.server = server(url)
        
        
# add printer and server to the moonraker library
__all__ = ["Moonraker", "printer", "server"]

__version__ = "1.0.0"
__author__ = "Dashtiss"
__license__ = "MIT"
__copyright__ = "Copyright 2025 Dashtiss"


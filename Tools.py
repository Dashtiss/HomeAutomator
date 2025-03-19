import inspect
from moonraker import Moonraker

class MoonrakerTools:
    def __init__(self, url: str) -> None:
        self.moonraker = Moonraker(url)

    def get_tools(self) -> list:
        tools = []
        self._add_class_methods(self.moonraker.printer, tools, prefix="printer_")
        self._add_class_methods(self.moonraker.server, tools, prefix="server_")
        self._add_class_methods(self.moonraker.server.files, tools, prefix="server.files_")
        return tools

    def _add_class_methods(self, obj, tools, prefix=""):
        for name, func in inspect.getmembers(obj, predicate=inspect.ismethod):
            if name.startswith("_"):
                continue
            docstring = func.__doc__ or "No description available."
            parameters = inspect.signature(func).parameters
            properties = {}
            required = []
            for param_name, param in parameters.items():
                if param_name == 'self':
                    continue
                param_type = getattr(param.annotation, '__name__', 'string')
                properties[param_name] = {
                    "type": param_type,
                    "description": f"Parameter {param_name}"
                }
                if param.default == inspect.Parameter.empty:
                    required.append(param_name)
            tools.append({
                "type": "function",
                "function": {
                    "name": prefix + name,
                    "description": docstring,
                    "parameters": {
                        "type": "object",
                        "properties": properties,
                        "required": required,
                        "additionalProperties": False
                    },
                    "strict": True
                }
            })
    def getFunc(self, tool: dict):
        func: str = tool["function"]["name"]
        
        if func.startswith("printer_"):
            return getattr(self.moonraker.printer, func[len("printer_"):])
        elif func.startswith("server_"):
            return getattr(self.moonraker.server, func[len("server_"):])
        elif func.startswith("server.files_"):
            return getattr(self.moonraker.server.files, func[len("server.files_"):])
# Example usage
if __name__ == "__main__":
    import json
    
    url = "http://192.168.1.25:7125"
    tools = MoonrakerTools(url)
    print(json.dumps(tools.get_tools(), indent=2))
    with open("tools.json", "w") as f:
        json.dump(tools.get_tools(), f, indent=2)
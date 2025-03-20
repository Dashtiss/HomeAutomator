import moonraker
import Tools
if __name__ == "__main__":
    raker = moonraker.Moonraker("http://192.168.1.25:7125")
    T = Tools.MoonrakerTools(raker)
    
    tools = T.get_tools()
    
    for tool in tools:
        print("Name: ", end="")
        print(tool["function"]["name"])
        print("\nDescription:")
        print(tool["function"]["description"])
        print("\nParameters:")
        # will print the params with their types and descriptions
        for param in tool["function"]["parameters"]["properties"].items():
            print(param[0], ":", param[1]["type"], ":", param[1]["description"])
        print("%^" * 75)
    
    info = raker.server.info()
    for name, result in info["result"].items():
        print(name, ":", result)
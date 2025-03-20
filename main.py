from isy import eisy
import json
def main():
    e = eisy.EISY("http://192.168.1.105:8080/", "admin", "admin")
    
    # will run all functions to test
    for func in dir(e):          
            if func.startswith("_"):
                continue
            fun = getattr(e, func)
            if callable(fun):
                print(f"Running {func}")
                print(fun())

    
        
if __name__ == "__main__":
    main()
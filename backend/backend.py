import fastapi

app = fastapi.FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/")
def connect_root():
    return {"Hello": "World"}
if __name__ == "__main__":
    import uvicorn
    server = uvicorn.run(app, host="0.0.0.0", port=8000)

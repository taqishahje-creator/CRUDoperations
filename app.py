from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_Home():
    return {"message": "Welcome to the Home Page!"}


from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_Home():
    """ Returining baisc browser information for the home page """
    return { "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]}

@app.get("/health")
async def health_check():
    return {"status": "ok"}
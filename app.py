import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

app.mount("/", StaticFiles(directory=PROJECT_ROOT, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

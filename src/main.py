# main.py

import uvicorn
from fastapi import FastAPI

from .routes import lcdman

app = FastAPI()
app.include_router(lcdman.router, prefix="/api")

@app.get("/")
async def serve_root():
    return {"title": "RPi 16x2 LCD Manager"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

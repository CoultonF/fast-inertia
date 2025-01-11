from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# app/__init__.py
__version__ = "0.1.0"
# comment
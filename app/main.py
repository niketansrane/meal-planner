"""FastAPI Application lives here."""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    """Home endpoint."""
    return {"message": "Welcome to the FastAPI application!"}

# src/app.py

from fastapi import FastAPI
from pydantic import BaseModel
from src.password_validator import validate_password

app = FastAPI()


class PasswordRequest(BaseModel):
    password: str


@app.get("/health")
def healthcheck():
    return {"status": "ok"}


@app.post("/validate-password")
def post_password(body: PasswordRequest):
    result = validate_password(body.password)
    return result
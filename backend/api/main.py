from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://127.0.0.1:5500",
    "https://mjpick86.github.io/max-booking-app/",
]

class Num(BaseModel):
    number: int

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/square")
def square(number: Num):
    return {"result": number.number ** 2}
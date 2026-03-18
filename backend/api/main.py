from fastapi import FastAPI
import mysql.connector
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
db_host = os.environ.get('DB_HOST', 'localhost')  # Use a default value if the environment variable is not set
db_user = os.environ.get('DB_USER', 'root')  # Use a default value if the environment variable is not set
db_password = os.environ.get('DB_PASSWORD', 'default_password')  # Use a default value if the environment variable is not set
db_name = os.environ.get('DB_NAME', 'booking')  # Use a default value if the environment variable is not set

origins = [
    "http://127.0.0.1:5500",
    "https://mjpick86.github.io",
]

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=db_password,
    database="booking"
)

class Num(BaseModel):
    number: int

class Booking(BaseModel):
    name: str
    date: str
    comments: str

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

@app.get("/all_dates")
def all_dates():
    cur = conn.cursor()
    cur.execute("SELECT date FROM bookings;")
    return {"dates": [date[0] for date in cur.fetchall()]}

@app.post("/place_booking")
def place_booking(booking: Booking):
    cur = conn.cursor()
    cur.execute("INSERT INTO bookings (name, date, comments) VALUES (%s, %s, %s);", (booking.name, booking.date, booking.comments))
    conn.commit()
    return {"message": "Booking placed successfully"}

@app.get("/db_test")
def db_test():
    cur = conn.cursor()
    cur.execute("SELECT version();")
    return {"version": cur.fetchone()}
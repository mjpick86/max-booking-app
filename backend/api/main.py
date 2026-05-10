from fastapi import FastAPI, HTTPException
import mysql.connector
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import datetime as dt
import uvicorn
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

class BookingRange(BaseModel):
    name: str
    start_date: str
    end_date: str
    comments: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

def is_valid_date(date_str):
    try:
        dt.datetime.strptime(date_str, "%d/%m/%Y")
        return True
    except:
        return False
    
def is_valid_start_date(date_str):
    if not is_valid_date(date_str): return False
    dates = all_dates()["dates"]
    return date_str not in dates

def is_valid_dates(start_str, end_str):
    if not is_valid_date(start_str) or not is_valid_date(end_str): return False
    dates = all_dates()["dates"]
    start_date = dt.datetime.strptime(start_str, "%d/%m/%Y").date()
    end_date = dt.datetime.strptime(end_str, "%d/%m/%Y").date()
    max_length = dt.timedelta(days=30)
    if (start_date + max_length) < end_date: return False 
    if start_date <= dt.date.today(): return False
    for date in dates:
        if start_date <= date < end_date: return False
    return True

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/all_dates")
def all_dates():
    cur = conn.cursor()
    cur.execute("DELETE FROM bookings WHERE date < CURDATE();")
    cur.execute("SELECT date FROM bookings;")
    return {"dates": [date[0] for date in cur.fetchall()]}

@app.post("/place_booking")
def place_booking(booking: Booking):
    if not is_valid_start_date(booking.date):
        raise HTTPException(status_code=500, detail="invalid date")
    cur = conn.cursor()
    cur.execute("INSERT INTO bookings (name, date, comments) VALUES (%s, %s, %s);", (booking.name, booking.date, booking.comments))
    conn.commit()
    return {"message": "Booking placed successfully"}

@app.post("/place_booking_range")
def place_booking_range(booking_range: BookingRange):
    if not is_valid_dates(booking_range.start_date, booking_range.end_date):
        raise HTTPException(status_code=500, detail="invalid date")
    cur = conn.cursor()
    delta = dt.timedelta(days=1)
    start_date = dt.datetime.strptime(booking_range.start_date, "%d/%m/%Y")
    end_date = dt.datetime.strptime(booking_range.end_date, "%d/%m/%Y")
    while start_date < end_date:
        cur.execute("INSERT INTO bookings (name, date, comments) VALUES (%s, %s, %s);", (booking_range.name, start_date.strftime("%Y-%m-%d"), booking_range.comments))
        start_date += delta
    conn.commit()
    return {"message": "Booking placed successfully"}

@app.get("/db_test")
def db_test():
    cur = conn.cursor()
    cur.execute("SELECT version();")
    return {"version": cur.fetchone()}
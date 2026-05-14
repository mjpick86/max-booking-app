from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import psycopg2
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import datetime as dt
load_dotenv()  # Load environment variables from .env file
DATABASE_URL = os.getenv("DATABASE_URL")

origins = [
    "http://127.0.0.1:5500",
    "https://mjpick86.github.io",
]

conn = psycopg2.connect(DATABASE_URL)

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

# Path to the favicon.ico file
favicon_path = os.path.join(os.path.dirname(__file__), "static", "favicon.ico")

# Mount the "static" directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)

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

@app.get("/")
def health():
    return {"status": "ok"}

@app.get("/all_dates")
def all_dates():
    cur = conn.cursor()
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
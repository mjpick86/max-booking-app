from fastapi import FastAPI
import mysql.connector
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
db_password = os.environ.get('DB_PASSWORD', 'default_password')  # Use a default value if the environment variable is not set

origins = [
    "http://127.0.0.1:5500",
    "https://mjpick86.github.io",
]

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=db_password,
    database="squares"
)

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

'''
@app.post("/square")
def square(number: Num):
    result = number.number ** 2
    cur = conn.cursor()
    cur.execute("INSERT INTO squares (squared) VALUES (%s);", (result,))
    conn.commit()
    return {"result": result}
''' 

@app.get("/db_test")
def db_test():
    cur = conn.cursor()
    cur.execute("SELECT version();")
    return {"version": cur.fetchone()}

'''
@app.get("/last_squares")
def last_squares():
    cur = conn.cursor()
    cur.execute("SELECT squared FROM squares ORDER BY id DESC LIMIT 5;")
    return {"result": [row[0] for row in cur.fetchall()]}
'''
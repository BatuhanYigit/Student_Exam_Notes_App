from fastapi import FastAPI
from fastapi.responses import JSONResponse
import psycopg2
import pandas as pd
from pydantic import BaseModel
import hashlib
import sqlquery

app = FastAPI()


conn = psycopg2.connect(
    host = 'db',
    database = 'app_db',
    user = 'postgres',
    password = 'postgres'
)

class User(BaseModel):
    username:str
    password:str

@app.get("/user_table")
def read_items():
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    results = cur.fetchall()
    return JSONResponse(content=results)

@app.post("/register")
async def create_user(user: User):
    cur = conn.cursor()
    username = user.username
    password = user.password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    info ={
        "username":username,
        "password":hashed_password

    }
    
    cur.execute(sqlquery.insert_data.format(**info))
    conn.commit()
    cur.execute("SELECT * FROM users")
    results = cur.fetchall()
    print("username : ",username)
    print("Password : ",hashed_password)
    conn.rollback()
    return JSONResponse(content=results)

@app.post("/login")
async def test_login(user: User):
    cur = conn.cursor()
    username = user.username
    password = user.password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    login= {
        "username":username,
        "password":hashed_password
    }
    cur.execute(sqlquery.check_login.format(**login))
    login_control = cur.fetchone()
    print(login_control)

    if login_control:
        return f"WELCOME {username}"
    else:
        return "Wrong"
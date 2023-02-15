from fastapi import FastAPI
from fastapi.responses import JSONResponse
import psycopg2
import pandas as pd
from pydantic import BaseModel
import hashlib
import sqlquery
import string
import secrets

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

class Token(BaseModel):
    token:str


def generate_token(username):
    alphabet = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(alphabet) for i in range(32))
    hashed_token = hashlib.sha256((token+username).encode()).hexdigest()
    return hashed_token

def check_token(token):

    token_info = {
        "token":token
    }

    cur = conn.cursor()
    cur.execute(sqlquery.check_login.format(**token_info))
    login_control = cur.fetchone()
    return login_control

@app.get("/user_table")
def read_items(token: Token):
    cur = conn.cursor()
    token_info = {

        "token":token.token
    }
    print(token_info)
    cur.execute(sqlquery.check_token.format(**token_info))
    login_control = cur.fetchone()
    print(login_control)
    if login_control:
        cur.execute("SELECT * FROM users")
        results = cur.fetchall()
        return JSONResponse(content=results)
    else:
        return "Wrong"


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
    token = generate_token(username)

    cur.execute(sqlquery.check_login.format(**login))
    login_control = cur.fetchone()
    print(login_control)
    if login_control:
        token = generate_token(username)
        token_test = {
            "username":username,
            "token":token
        }
        cur.execute(sqlquery.update_token.format(**token_test))
        conn.commit()
        return f"WELCOME {username} Access Token : {token}"
    else:
        return "Wrong"
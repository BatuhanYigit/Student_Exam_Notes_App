from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
import psycopg2
import pandas as pd
from pydantic import BaseModel
import hashlib
import sqlquery
import string
import secrets
import datetime


app = FastAPI()


conn = psycopg2.connect(
    host = 'db',
    database = 'app_db',
    user = 'postgres',
    password = 'postgres'
)


    


class User(BaseModel):
    email:str
    password:str
    role:str

class Login(BaseModel):
    email:str
    password:str

class Token(BaseModel):
    token:str

class Lesson_Create(BaseModel):
    email:str
    lesson:str
    exam_marks:int


def generate_token(email):
    alphabet = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(alphabet) for i in range(32))
    hashed_token = hashlib.sha256((token+email).encode()).hexdigest()
    return hashed_token

def token_control(request,response):
    bearer_token = request.headers.get("authorization", "")
    token = bearer_token.split(' ')
    if len(token) != 2:
        return "Hatalı token"

    token = token[1]

    now = datetime.datetime.now()

    print(token)
    cur = conn.cursor()
    token_info = {

        "token":token,
        "now":now

    }
    print(token_info)
    cur.execute(sqlquery.check_token.format(**token_info))
    login_control = cur.fetchone()
    return(login_control)

def letter_grade_check(exam_marks):
    if exam_marks > 79 and exam_marks <= 100:
        return "AA"
    elif exam_marks > 70 and exam_marks <= 80:
        return "BA"
    elif exam_marks > 62 and exam_marks <= 71:
        return "BB"
    elif exam_marks > 54 and exam_marks <= 63:
        return "CB"
    elif exam_marks > 49 and exam_marks <= 55:
        return "CC"
    elif exam_marks > 44 and exam_marks <= 50:
        return "DC"
    elif exam_marks > 34 and exam_marks <= 45:
        return "DD"
    elif exam_marks > 0 and exam_marks <= 35:
        return "FF"
    else:
        return "Yanlış Not"






@app.get("/user_table")
def read_items(
    request: Request,
    response: Response,
):
    cur = conn.cursor()


    if token_control(request,response):
        cur.execute("SELECT * FROM users")
        results = cur.fetchall()
        return JSONResponse(
            content={
            "data": [],
            "success": True,
            "results":results
        })
    else:
        return "Tokenin tarihi geçmiş"



@app.post("/register")
async def create_user(user: User):
    cur = conn.cursor()
    email = user.email
    password = user.password
    role = user.role
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    info ={

        "email":email,
        "password":hashed_password,
        "role":role

    }
    
    cur.execute(sqlquery.insert_data.format(**info))
    conn.commit()
    cur.execute("SELECT * FROM users")
    results = cur.fetchall()
    print("email : ",email)
    print("Password : ",hashed_password)
    conn.rollback()
    return JSONResponse(content=results)

@app.post("/login")
async def test_login(login: Login):
    cur = conn.cursor()
    email = login.email
    password = login.password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    expire_time = datetime.datetime.now() + datetime.timedelta(minutes=15)
    login= {
        "email":email,
        "password":hashed_password
    }
    token = generate_token(email)

    cur.execute(sqlquery.check_login.format(**login))
    login_control = cur.fetchone()
    print(login_control)
    if login_control:
        token = generate_token(email)
        token_test = {
            "email":email,
            "token":token,
            "expire_time":expire_time
        }
        cur.execute(sqlquery.update_token.format(**token_test))
        conn.commit()
        return f"WELCOME {email} Access Token : {token}"
    else:
        return "Wrong"

@app.post("/create_lesson")
def lesson_create(lesson_create:Lesson_Create):
    cur = conn.cursor()
    email = lesson_create.email
    lesson = lesson_create.lesson
    exam_marks = lesson_create.exam_marks
    letter_grade = letter_grade_check(exam_marks)
    create_lesson = {
        "email":email,
        "lesson":lesson,
        "exam_marks":exam_marks,
        "letter_grade":letter_grade
    }
    cur.execute(sqlquery.create_lesson.format(**create_lesson))
    conn.commit()
    return f"Kayıtlar girilmiştir {create_lesson}"

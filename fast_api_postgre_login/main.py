from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
import psycopg2
import pandas as pd
from pydantic import BaseModel
import hashlib
import sqlquery
import string
import secrets
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


conn = psycopg2.connect(
    host = os.getenv('POSTGRES_HOST'),
    database = os.getenv('POSTGRES_DB'),
    user = os.getenv('POSTGRES_USER'),
    password = os.getenv('POSTGRES_PASSWORD'),
)

class User(BaseModel):
    email: str
    password: str
    role: str

class Login(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    token: str

class Lesson_Create(BaseModel):
    email: str
    lesson: str
    exam_marks: int


def check_register_date(email):
    cur = conn.cursor()
    register_info = {
        "email":email
    }
    cur.execute(sqlquery.check_register_date.format(**register_info))
    register_date = cur.fetchall()
    register_date = register_date[0][0]
    register_date_difference = register_date.split(' ')
    register_date_difference = register_date_difference[0]
    format = '%Y-%m-%d'
    now = datetime.datetime.today() 
    register_date_difference = datetime.datetime.strptime(register_date_difference, format)
    if register_date_difference > now:
        difference = (register_date_difference - now).days
    else:
        difference = (now - register_date_difference).days
    # difference = (register_date_difference - now).days
    if difference > 15:
        return "Kullanıcı {} gündür kayıtlı ve 15 günden uzun süredir kayıtlı. Kayıt tarihi = {}".format(difference,register_date)
    else:
        return("Kullanıcı {} Gündür kayıtlı. Kayıt Tarihi = {}".format(difference,register_date))

def generate_token(email):
    alphabet = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(alphabet) for i in range(32))
    hashed_token = hashlib.sha256((token+email).encode()).hexdigest()
    return hashed_token

def token_check(request,response):
    bearer_token = request.headers.get("authorization", "")
    token = bearer_token.split(' ')
    token = token[1]
    return(token)


def token_control(request,response):
    bearer_token = request.headers.get("authorization", "")
    token = bearer_token.split(' ')
    if len(token) != 2:
        return False
    elif token is None:
        return False
    token = token[1]

    now = datetime.datetime.now()

    cur = conn.cursor()
    token_info = {

        "token":token,
        "now":now

    }
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
    elif exam_marks >= 0 and exam_marks <= 35:
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
        token = token_check(request,response)
        role_info = {
            "token":token
        }
        cur.execute(sqlquery.check_role.format(**role_info))
        role = cur.fetchall()
        role = role[0][0]
        if role == "Öğretmen":
            cur.execute("SELECT * FROM users")
            data = cur.fetchall()
            return JSONResponse(
                content={
                "data": data,
                "success": True,
                "token_control":token_control(request,response),
            },
            status_code = status.HTTP_200_OK
            )
        else:
            return JSONResponse(
                content={
                "data":[],
                "success":False,
                "msg":"Kullanıcı tablosunu sadece öğretmen görebilir."
                },
                status_code = status.HTTP_401_UNAUTHORIZED
            )
    else:
        return JSONResponse(
            content={
            "data":[],
            "success":False,
            "message":"Token Yanlış Veya Tarihi Dolmuş"
            },
            status_code = status.HTTP_403_FORBIDDEN
            
        )



@app.post("/register")
async def create_user(user: User):
    try:
        cur = conn.cursor()
        email = user.email
        password = user.password
        role = user.role
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        register_date = datetime.datetime.now()
        info ={

            "email":email,
            "password":hashed_password,
            "role":role,
            "register_date":register_date

        }
        
        cur.execute(sqlquery.insert_data.format(**info))
        conn.commit()
        cur.execute("SELECT * FROM users")
        results = cur.fetchall()
        conn.rollback()
        return JSONResponse(content=results)
    except psycopg2.errors.UniqueViolation:
        return "Mail adresi Kullanılmaktadır", status.HTTP_406_NOT_ACCEPTABLE

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
    if login_control:
        token = generate_token(email)
        token_test = {
            "email":email,
            "token":token,
            "expire_time":expire_time
        }

        cur.execute(sqlquery.update_token.format(**token_test))
        conn.commit()
        data = check_register_date(email)
        return JSONResponse(
            content={
            "Hoşgeldin":email,
            "Access TOken":token,
            "Kayıt":data,
            "success":True
            },
            status_code = status.HTTP_200_OK
        )
        
    else:
        msg = "Giriş Yapılamadı"
        return JSONResponse(
            content={
            "msg":msg,
            "success":False
            },
            status_code = status.HTTP_403_FORBIDDEN

        )

@app.post("/create_lesson")
def lesson_create(lesson_create:Lesson_Create,request:Request,response:Response):
    
    
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
    if token_control(request,response):
        token = token_check(request,response)
        role_info = {
            "token":token
        }
        cur.execute(sqlquery.check_role.format(**role_info))
        role = cur.fetchall()
        role = role[0][0]
        if role == "Öğretmen":
            cur.execute(sqlquery.create_lesson.format(**create_lesson))
            conn.commit()
            return f"Kayıtlar girilmiştir {create_lesson}"
        else:
            return JSONResponse(
                content={
                "data":[],
                "success":False,
                "msg":"Ders Girişini sadece öğretmen yapabilir"
                },
                status_code = status.HTTP_401_UNAUTHORIZED
            )
    else:
        return JSONResponse(
            content={
            "data":[],
            "success":False,
            "message":"Token Yanlış Veya Tarihi Dolmuş"
            },
            status_code = status.HTTP_403_FORBIDDEN
        )
    


@app.get("/check-lesson")
def check_lesson(
    request: Request,
    response: Response
):
    cur = conn.cursor()
   
    if token_control(request,response):
        token_info = {
        "token":token_check(request,response)
    }
        cur.execute(sqlquery.check_email.format(**token_info))
        email = cur.fetchall()
        email = email[0][0]
        email_info = {
        "email":email
        } 
        cur.execute(sqlquery.check_lesson.format(**email_info))
        results = cur.fetchall()
        return JSONResponse(results)
    else:
        return "Tokenin Tarihi Geçmiş"

@app.post("/update-lesson")
def update_lesson(
    request:Request,
    response:Response,
    lesson_update:Lesson_Create
):
    token = token_check(request,response)
    cur = conn.cursor()
    email = lesson_update.email
    lesson = lesson_update.lesson
    exam_marks = lesson_update.exam_marks
    letter_grade = letter_grade_check(exam_marks)

    update_lesson = {
        "email":email,
        "lesson":lesson,
        "exam_marks":exam_marks,
        "letter_grade":letter_grade
    }

    if token_control(request,response):
        role_info = {
        "token":token
        }
        cur.execute(sqlquery.check_role.format(**role_info))
        role = cur.fetchall()
        role = role[0][0]
        if role == "Öğretmen":

            cur.execute(sqlquery.update_lesson.format(**update_lesson))
            conn.commit()
            # return f"Kayıtlar Güncellenmiştir {update_lesson}"
            return JSONResponse(
                content={
                "data":update_lesson,
                "success":True,
                "msg":"Kayıtlar Güncellenmiştir."
                },
                status_code= status.HTTP_200_OK
            )
        else:
            return JSONResponse(
                content={
                "data":[],
                "success":False,
                "msg":"Ders Girişini sadece öğretmen yapabilir"
                },
                status_code = status.HTTP_401_UNAUTHORIZED
            )
    else:
        # return "Tokenin Tarihi Geçmiş Tekrar Login olun"
        return JSONResponse(
            content={
            "data":[],
            "msg":"Tokenin Tarihi Geçmiş",
            "success":False
            },
            status_code= status.HTTP_400_BAD_REQUEST
        )



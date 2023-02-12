from fastapi import FastAPI
from pydantic import BaseModel


user_db = {
    'batu':{'username':'batu', 'date_joined':'2023-02-08', 'location':'Kadıköy', 'age':10, 'password':'123'},
    'ahmet':{'username':'ahmet', 'date_joined':'2023-02-10', 'location':'Göztepe', 'age':21},
    'mert':{'username':'mert', 'date_joined':'2023-02-12', 'location':'Maltepe', 'age':5},
}

class User(BaseModel):
    username: str
    date_joined: str
    location: str
    age: int
    password: str

app = FastAPI()

@app.get('/users')
def get_users_query(limit: int=20):
    user_list = list(user_db.values())
    return user_list[:limit]

@app.get('/users/{username}')
def get_users_path(username: str='jack'):
    return user_db[username]

@app.post('/users')
def create_user(user: User):
    username = user.username
    user_db[username] = user.dict()
    return {'message':f'Successfully created user:{username}'}


@app.post('/login')
def login_user(user: User):
    username = user.username
    password = user.password
    if username == user_db[username]["username"] and password == user_db[username]["password"]:
        return{'message':f'WELCOME {username}'}
        
    else:
        return{'NULL'}

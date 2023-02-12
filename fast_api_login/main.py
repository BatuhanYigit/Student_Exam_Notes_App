from fastapi import FastAPI
from pydantic import BaseModel

user_db = {
    'batu':"123",
    'deneme':"123",
    'ahmet':"123"
}

class User(BaseModel):
    username:str
    password:str

app = FastAPI()

@app.get('/users')
def get_users(limit: int = 20):
    user_list = list(user_db.values())
    return user_list[:limit]

@app.post('/login')
def login(user: User):
    username = user.username
    password = user.password

    try:

        if password == user_db[username]:
            return(f'Welcome {username}')
        else:
            return("Wrong Username or Password")
    except KeyError:
        return("Wrong Username or Password")
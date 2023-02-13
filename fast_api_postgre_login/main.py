from fastapi import FastAPI
from fastapi.responses import JSONResponse
import psycopg2
import pandas as pd

app = FastAPI()

conn = psycopg2.connect(
    host = 'db',
    database = 'app_db',
    user = 'postgres',
    password = 'postgres'
)

@app.get("/items")
def read_items():
    cur = conn.cursor()
    cur.execute("SELECT * FROM items")
    results = cur.fetchall()
    return JSONResponse(content=results)


@app.get("/pandas")
def get_items():
    df = pd.read_sql("SELECT * FROM items", conn)
    print(df)
    return "welcome"


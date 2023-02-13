from fastapi import FastAPI
from fastapi.responses import JSONResponse
import psycopg2

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

@app.post("/items_add")
def items_add():
    cur = conn.cursor()

    cur.execute("""INSERT INTO items (id,name,description) VALUES ('{id}', '{name}', '{description}')""")
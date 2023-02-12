from fastapi import FastAPI

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}, {"item_name": "Deneme"}, {"item_name": "Ahmet"}, {"item_name": "Mert"},
                 {"item_name": "deneme"}, {"item_name": "batuhan"}, {"item_name": "ahmet"}, {"item_name": "mert"}, {"item_name": "fundi"}, {"item_name": "funda"}, ]

@app.get("/items/")
async def read_item(start: int = 0, finish: int = 10):
    return fake_items_db[start : finish]
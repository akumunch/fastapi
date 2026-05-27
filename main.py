from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str

user = User(id=123, name='Jane Doe')
print(user.model_dump())



# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def home():
#     return {"message":"Hello World"}

# @app.get("/add")
# def add(a: int, b:int):
#     return {"sum":a+b}

# @app.get("/user/{name}")
# def name(name:str):
#     return {"name":f"Hello {name}"}




# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()


# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: bool | None = None


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str | None = None):
#     return {"item_id": item_id, "q": q}


# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}
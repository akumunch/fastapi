from fastapi import FastAPI
from database import engine, Base
from routers import notes

#reads all models that inherit from Base and creates tables for them in MySQL, if they dont exist yet
Base.metadata.create_all(bind=engine) 

app = FastAPI()

app.include_router(notes.router)
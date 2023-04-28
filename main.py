from fastapi import FastAPI
from routes.users import users

app = FastAPI(
    title="Rest API with FastAPI and Mongodb",
    description='This is a example of Rest Api using FastAPI framework',
)

app.include_router(users)

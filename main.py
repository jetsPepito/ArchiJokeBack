from fastapi import FastAPI
from endpoints import jokes, users
app = FastAPI()

app.include_router(jokes.router)
app.include_router(users.router)

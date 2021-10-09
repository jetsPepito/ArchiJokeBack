from fastapi import FastAPI
from endpoints import jokes
app = FastAPI()

app.include_router(jokes.router)

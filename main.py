from fastapi import FastAPI
from endpoints import jokes, users, health
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jokes.router)
app.include_router(users.router)
app.include_router(health.router)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import users, contact

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["*"] to allow all
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(contact.router)

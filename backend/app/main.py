from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import (
    users, items, cart, user_dashboard, auth,
    transactions, admin, admin_dashboard, wishlist, 
    subscriptions
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(items.router)
app.include_router(cart.router)
app.include_router(user_dashboard.router)
app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(admin.router)
app.include_router(admin_dashboard.router)
app.include_router(wishlist.router)
app.include_router(subscriptions.router)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"msg": "Hello World"}
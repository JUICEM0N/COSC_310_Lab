from fastapi import FastAPI
from backend.app.routers import users, items, cart, user_dashboard, auth, transactions

app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)
app.include_router(cart.router)
app.include_router(user_dashboard.router)
app.include_router(auth.router)
app.include_router(transactions.router)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"msg": "Hello World"}


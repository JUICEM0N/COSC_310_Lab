from fastapi import FastAPI

# Uncomment below when testing with PyTest
# from backend.app.routers.items import router as items_router

# Uncomment below when running FastAPI
# from app.routers import router as items_router
from routers import users, items, cart, user_dashboard

app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)
app.include_router(cart.router)
app.include_router(user_dashboard.router)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"msg": "Hello World"}


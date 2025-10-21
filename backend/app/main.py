from fastapi import FastAPI

# Uncomment below when testing with PyTest
# from backend.app.routers.items import router as items_router

# Uncomment below when running FastAPI
from routers.items import router as items_router

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"msg": "Hello World"}

app.include_router(items_router)

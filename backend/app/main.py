from fastapi import FastAPI
from routers.items import router as items_router

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
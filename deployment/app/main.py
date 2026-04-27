from fastapi import FastAPI
from mangum import Mangum
from app.routes import router

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is running"}

app.include_router(router)

handler = Mangum(app)
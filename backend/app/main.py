from fastapi import FastAPI
from sqlalchemy import text
from app.db.session import engine
from app.routers.auth_router import router as auth_router

app = FastAPI(title="Adaptive Learning Platform")

app.include_router(auth_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/health/db")
def db_health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"database": "connected"}
    except Exception as e:
        return {"database": "error", "detail": str(e)}
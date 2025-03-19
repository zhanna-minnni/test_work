from fastapi import FastAPI
from .database import engine, Base
from .routes import router


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/api/v1", tags=["wallets"])
from fastapi import FastAPI
from app.database import Base, engine
from app.routers import entries, webhook
from app.telegram_bot import start_telegram_bot
import asyncio

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(entries.router)
app.include_router(webhook.router)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_telegram_bot())

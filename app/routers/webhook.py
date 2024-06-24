from fastapi import APIRouter, Request
from telegram import Update, Bot
from telegram.ext import Application
from app.telegram_bot import setup_dispatcher

router = APIRouter()
TOKEN = "6976371602:AAFs3EbCgKCzsLi4tGzJaibXLD_uzXdypoQ"
bot = Bot(token=TOKEN)

@router.post(f"/webhook/{TOKEN}")
async def webhook(request: Request):
    update = Update.de_json(await request.json(), bot)
    app = Application.builder().token(TOKEN).build()
    setup_dispatcher(app)
    app.process_update(update)
    return "OK"

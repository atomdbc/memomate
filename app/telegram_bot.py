from telegram import Update, ForceReply, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from app.crud import create_entry
from app.database import SessionLocal
from app.schemas import Entry
from app.ai import generate_text
import logging
import asyncio
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=TOKEN)

async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    await update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

async def journal(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    content = update.message.text

    # Use Gemini Pro to process the content
    ai_content = await generate_text(prompt=content)

    entry = Entry(user_id=user_id, content=ai_content)
    db = SessionLocal()
    create_entry(db, entry)
    db.close()
    
    # Send only the AI-generated response
    await update.message.reply_text(ai_content)

def setup_dispatcher(app: Application):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, journal))

async def start_telegram_bot():
    application = Application.builder().token(TOKEN).build()
    setup_dispatcher(application)
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

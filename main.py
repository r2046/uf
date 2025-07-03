
import os
from yt_dlp import YoutubeDL
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
MY_USER_ID = int(os.getenv("USER_ID"))

def download_media(url):
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        'format': 'best',
        'quiet': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    await update.message.reply_text("🔄 Downloading...")
    try:
        file_path = download_media(url)
        await context.bot.send_document(chat_id=MY_USER_ID, document=open(file_path, 'rb'))
        os.remove(file_path)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

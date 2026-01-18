import os
import yt_dlp
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler

# دالة الترحيب
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلاً بك! أنا بوت تحميل الفيديوهات لعام 2026.\n\nأرسل لي رابط الفيديو (TikTok, YouTube, Insta) وسأقوم بتحميله لك فوراً.")

# دالة التحميل والمعالجة
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not url.startswith("http"):
        return

    chat_id = update.message.chat_id
    msg = await update.message.reply_text("⏳ جاري معالجة الرابط... انتظر قليلاً")

    try:
        file_path = f"{chat_id}_vid.mp4"
        ydl_opts = {
            'format': 'best',
            'outtmpl': file_path,
            'quiet': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            await asyncio.to_thread(ydl.download, [url])

        with open(file_path, 'rb') as video:
            await update.message.reply_video(video=video, caption="✅ تم التحميل بنجاح!")
        
        os.remove(file_path)
        await msg.delete()
    except Exception as e:
        await msg.edit_text(f"❌ حدث خطأ: {str(e)}")

def main():
    token = os.environ.get("BOT_TOKEN")
    app = Application.builder().token(token).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_video))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()

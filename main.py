import os
import yt_dlp
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# دالة معالجة الروابط وتحميل الفيديو
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    
    # التأكد أن الرسالة تحتوي على رابط
    if not url.startswith("http"):
        return

    chat_id = update.message.chat_id
    sent_message = await update.message.reply_text("⏳ جاري فحص الرابط وتحميل الفيديو... يرجى الانتظار.")

    try:
        # إعدادات التحميل (أفضل جودة mp4)
        file_path = f"{chat_id}_video.mp4"
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': file_path,
            'quiet': True,
            'no_warnings': True,
        }

        # عملية التحميل باستخدام مكتبة yt-dlp المطورة
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            await asyncio.to_thread(ydl.download, [url])

        # إرسال الفيديو للمستخدم
        with open(file_path, 'rb') as video:
            await update.message.reply_video(video=video, caption="✅ تم التحميل بنجاح بواسطة بوتك!")
        
        # حذف الفيديو من السيرفر بعد الإرسال لتوفير المساحة
        os.remove(file_path)
        await sent_message.delete()

    except Exception as e:
        await sent_message.edit_text(f"❌ حدث خطأ أثناء التحميل: {str(e)}")
        if os.path.exists(file_path):
            os.remove(file_path)

# تشغيل البوت
def main():
    # سيقوم Render بسحب التوكن من Environment Variables
    token = os.environ.get("BOT_TOKEN")
    if not token:
        print("خطأ: لم يتم العثور على BOT_TOKEN!")
        return

    app = Application.builder().token(token).build()
    
    # معالجة أي نص يتم إرساله (روابط)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🚀 البوت يعمل الآن ومستعد للتحميل...")
    app.run_polling()

if __name__ == '__main__':
    main()

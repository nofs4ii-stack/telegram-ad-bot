import os
import logging
from dotenv import load_dotenv
from supabase import create_client, Client
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

# 1. تحميل متغيرات البيئة من ملف .env للحماية
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
WEB_APP_URL = os.getenv("WEB_APP_URL", "https://telegram-ad-bot-xi.vercel.app")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# إعداد السجلات (Logging)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 2. إنشاء اتصال آمن مع Supabase
supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 3. دالة حفظ/تحديث المستخدم في Supabase
def sync_user_to_supabase(user):
    if not supabase:
        return
    try:
        data = {
            "telegram_id": user.id,
            "first_name": user.first_name,
            "username": user.username,
        }
        # حفظ أو تحديث بيانات المستخدم في جدول users
        supabase.table("users").upsert(data, on_conflict="telegram_id").execute()
    except Exception as e:
        logging.error(f"خطأ في حفظ المستخدم في Supabase: {e}")

# 4. أمر /start المعالج
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # حفظ بيانات المستخدم فوراً في Supabase
    sync_user_to_supabase(user)

    # أزرار الـ WebApp الموجهة للمسارات المناسبة
    keyboard = [
        [InlineKeyboardButton("📝 نشر إعلان جديد", web_app=WebAppInfo(url=f"{WEB_APP_URL}/post"))],
        [InlineKeyboardButton("📋 إعلاناتي", web_app=WebAppInfo(url=f"{WEB_APP_URL}/myads"))],
        [InlineKeyboardButton("👀 مشاهدة الإعلانات", web_app=WebAppInfo(url=f"{WEB_APP_URL}/ads"))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"👋 أهلاً بك يا {user.first_name} في منصة الإعلانات!\n\n"
        "📌 يمكنك استخدام الأزرار أدناه لتصفح المنصة وإدارة إعلاناتك:",
        reply_markup=reply_markup
    )

# 5. تشغيل التطبيق
def main():
    if not TOKEN:
        raise ValueError("⚠️ لم يتم العثور على BOT_TOKEN في ملف .env")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    print("✅ البوت الآمن يعمل الآن والمزامن مع Supabase جاهز...")
    app.run_polling()

if __name__ == "__main__":
    main()
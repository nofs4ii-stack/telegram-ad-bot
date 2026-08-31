import logging
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ========== الإعدادات ==========
TOKEN = "8946692822:AAF8MH5zAW78XTcmQOuYaTR69mQ2wBBzN9U"  # استبدل بالتوكن الخاص بك
ADMIN_IDS = [1442106217]  # استبدل بمعرف التليجرام الخاص بك (id)

# ========== قاعدة البيانات ==========
def init_db():
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY, phone TEXT, registered INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS posts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  user_id INTEGER, 
                  text TEXT, 
                  photo_id TEXT, 
                  status TEXT, 
                  reason TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()
    print("✅ قاعدة البيانات جاهزة")

init_db()

# ========== دوال مساعدة ==========
def is_admin(user_id):
    return user_id in ADMIN_IDS

def is_registered(user_id):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute("SELECT registered FROM users WHERE user_id=?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result and result[0] == 1

def register_user(user_id, phone=None):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO users (user_id, phone, registered) VALUES (?, ?, 1)", (user_id, phone))
    conn.commit()
    conn.close()

def get_post(post_id):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute("SELECT id, user_id, text, photo_id, status, reason FROM posts WHERE id=?", (post_id,))
    result = c.fetchone()
    conn.close()
    return result

def update_post_status(post_id, status, reason=None):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    if reason:
        c.execute("UPDATE posts SET status=?, reason=? WHERE id=?", (status, reason, post_id))
    else:
        c.execute("UPDATE posts SET status=? WHERE id=?", (status, post_id))
    conn.commit()
    conn.close()

def get_pending_posts():
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute("SELECT id, user_id, text, photo_id FROM posts WHERE status='pending' ORDER BY created_at DESC")
    result = c.fetchall()
    conn.close()
    return result

# ========== القائمة الرئيسية ==========
def main_menu(user_id=None):
    is_admin_user = is_admin(user_id) if user_id else False
    keyboard = [
        [InlineKeyboardButton("📝 نشر إعلان جديد", callback_data="post")],
        [InlineKeyboardButton("🔍 بحث عن إعلانات", callback_data="search")],
        [InlineKeyboardButton("📋 إدارة إعلاناتي", callback_data="myads")],
    ]
    if is_admin_user:
        keyboard.append([InlineKeyboardButton("👑 لوحة المشرف", callback_data="admin")])
    keyboard.append([InlineKeyboardButton("❓ المساعدة", callback_data="help")])
    return InlineKeyboardMarkup(keyboard)

# ========== أمر /start ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text(
        "👋 أهلاً بك في بوت الإعلانات!\n\n"
        "📌 استخدم الأزرار أدناه للتنقل:",
        reply_markup=main_menu(user_id)
    )

# ========== معالج الأزرار (الأهم) ==========
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    data = query.data

    # ===== قبول الإعلان =====
    if data.startswith("approve_"):
        if not is_admin(user_id):
            await query.edit_message_text("⛔ هذه الخاصية للمشرفين فقط.", reply_markup=main_menu(user_id))
            return
        
        post_id = int(data.split("_")[1])
        post = get_post(post_id)
        if not post:
            await query.edit_message_text("❌ الإعلان غير موجود.", reply_markup=main_menu(user_id))
            return
        
        update_post_status(post_id, "approved")
        
        # إشعار المعلن
        try:
            await context.bot.send_message(
                post[1],
                f"✅ تم الموافقة على إعلانك!\n\n"
                f"📝 نص الإعلان:\n{post[2]}"
            )
        except:
            pass
        
        await query.edit_message_text(
            f"✅ تم قبول الإعلان رقم {post_id} وإشعار المعلن.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="admin")]])
        )
        return

    # ===== رفض الإعلان =====
    if data.startswith("reject_"):
        if not is_admin(user_id):
            await query.edit_message_text("⛔ هذه الخاصية للمشرفين فقط.", reply_markup=main_menu(user_id))
            return
        
        post_id = int(data.split("_")[1])
        context.user_data['reject_post_id'] = post_id
        await query.edit_message_text(
            f"✏️ اكتب سبب رفض الإعلان رقم {post_id}:",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 إلغاء", callback_data="admin")]])
        )
        return

    # ===== زر النشر =====
    if data == "post":
        if not is_registered(user_id):
            await query.edit_message_text(
                "🔐 يبدو أنك غير مسجل. أرسل رقم هاتفك للتسجيل (مرة واحدة فقط)."
            )
            context.user_data['waiting_for_registration'] = True
            return
        
        await query.edit_message_text(
            "📤 أرسل نص إعلانك.\nيمكنك إرفاق صورة مع النص (اختياري).",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="back")]])
        )
        context.user_data['waiting_for_post'] = True

    # ===== زر البحث =====
    elif data == "search":
        await query.edit_message_text(
            "🔍 قريباً: نظام البحث المتقدم.",
            reply_markup=main_menu(user_id)
        )

    # ===== إدارة إعلاناتي =====
    elif data == "myads":
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        c.execute("SELECT id, text, status, reason FROM posts WHERE user_id=? ORDER BY created_at DESC LIMIT 10", (user_id,))
        posts = c.fetchall()
        conn.close()
        
        if not posts:
            await query.edit_message_text("📋 ليس لديك إعلانات.", reply_markup=main_menu(user_id))
            return
        
        status_map = {'pending': '⏳ قيد المراجعة', 'approved': '✅ تم الموافقة', 'rejected': '❌ مرفوض'}
        msg = "📋 آخر 10 إعلانات:\n\n"
        for p in posts:
            msg += f"🆔 {p[0]}\n📝 {p[1][:50]}...\n📊 {status_map.get(p[2], p[2])}"
            if p[3]:
                msg += f"\n💬 السبب: {p[3]}"
            msg += "\n\n"
        
        await query.edit_message_text(msg, reply_markup=main_menu(user_id))

    # ===== لوحة المشرف =====
    elif data == "admin":
        if not is_admin(user_id):
            await query.edit_message_text("⛔ هذه اللوحة خاصة بالمشرفين فقط.", reply_markup=main_menu(user_id))
            return
        
        keyboard = [
            [InlineKeyboardButton("📊 الإحصائيات", callback_data="stats")],
            [InlineKeyboardButton("📝 الإعلانات المعلقة", callback_data="pending")],
            [InlineKeyboardButton("👥 المستخدمين", callback_data="users")],
            [InlineKeyboardButton("📢 إرسال إشعار", callback_data="broadcast")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="back")],
        ]
        await query.edit_message_text("👑 لوحة التحكم:", reply_markup=InlineKeyboardMarkup(keyboard))

    # ===== الإحصائيات =====
    elif data == "stats":
        if not is_admin(user_id):
            await query.edit_message_text("⛔ خاصة بالمشرفين.", reply_markup=main_menu(user_id))
            return
        
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM users")
        users_count = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM posts")
        posts_count = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM posts WHERE status='pending'")
        pending_count = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM posts WHERE status='approved'")
        approved_count = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM posts WHERE status='rejected'")
        rejected_count = c.fetchone()[0]
        conn.close()
        
        await query.edit_message_text(
            f"📊 الإحصائيات:\n\n"
            f"👥 المستخدمين: {users_count}\n"
            f"📝 الكلية: {posts_count}\n"
            f"⏳ المعلقة: {pending_count}\n"
            f"✅ المقبولة: {approved_count}\n"
            f"❌ المرفوضة: {rejected_count}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="admin")]])
        )

    # ===== الإعلانات المعلقة =====
    elif data == "pending":
        if not is_admin(user_id):
            await query.edit_message_text("⛔ خاصة بالمشرفين.", reply_markup=main_menu(user_id))
            return
        
        pending_posts = get_pending_posts()
        if not pending_posts:
            await query.edit_message_text(
                "✅ لا توجد إعلانات معلقة.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="admin")]])
            )
            return
        
        for post in pending_posts:
            post_id, post_user_id, text, photo_id = post
            keyboard = [
                [
                    InlineKeyboardButton("✅ قبول", callback_data=f"approve_{post_id}"),
                    InlineKeyboardButton("❌ رفض", callback_data=f"reject_{post_id}")
                ]
            ]
            
            if photo_id:
                await query.message.reply_photo(
                    photo_id,
                    caption=f"📝 إعلان #{post_id}\n👤 من: {post_user_id}\n\n{text}",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
            else:
                await query.message.reply_text(
                    f"📝 إعلان #{post_id}\n👤 من: {post_user_id}\n\n{text}",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
        
        await query.edit_message_text(
            "📋 الإعلانات المعلقة أعلاه.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="admin")]])
        )

    # ===== عرض المستخدمين =====
    elif data == "users":
        if not is_admin(user_id):
            await query.edit_message_text("⛔ خاصة بالمشرفين.", reply_markup=main_menu(user_id))
            return
        
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        c.execute("SELECT user_id, phone FROM users LIMIT 20")
        users = c.fetchall()
        conn.close()
        
        if not users:
            await query.edit_message_text("👥 لا يوجد مستخدمون.", reply_markup=main_menu(user_id))
            return
        
        msg = "👥 المستخدمون (آخر 20):\n\n"
        for u in users:
            msg += f"🆔 {u[0]}\n📱 {u[1] or 'غير محدد'}\n\n"
        
        await query.edit_message_text(msg, reply_markup=main_menu(user_id))

    # ===== بث إشعار =====
    elif data == "broadcast":
        if not is_admin(user_id):
            await query.edit_message_text("⛔ خاصة بالمشرفين.", reply_markup=main_menu(user_id))
            return
        
        await query.edit_message_text(
            "📢 أرسل النص للإشعار:",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="admin")]])
        )
        context.user_data['waiting_for_broadcast'] = True

    # ===== المساعدة =====
    elif data == "help":
        await query.edit_message_text(
            "❓ المساعدة:\n\n"
            "📝 نشر: اضغط زر النشر وأرسل النص.\n"
            "🔍 بحث: للعثور على إعلانات.\n"
            "📋 إدارة: عرض إعلاناتك.\n"
            "👑 المشرف: لوحة التحكم.",
            reply_markup=main_menu(user_id)
        )

    # ===== رجوع =====
    elif data == "back":
        await query.edit_message_text(
            "📌 القائمة الرئيسية:",
            reply_markup=main_menu(user_id)
        )

# ========== معالج الرسائل ==========
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    photo = update.message.photo

    # تسجيل المستخدم
    if context.user_data.get('waiting_for_registration'):
        register_user(user_id, text)
        context.user_data['waiting_for_registration'] = False
        await update.message.reply_text(
            "✅ تم التسجيل! يمكنك الآن النشر.",
            reply_markup=main_menu(user_id)
        )
        return

    # كتابة سبب الرفض
    if context.user_data.get('reject_post_id'):
        post_id = context.user_data['reject_post_id']
        reason = text
        post = get_post(post_id)
        
        update_post_status(post_id, "rejected", reason)
        
        if post:
            try:
                await context.bot.send_message(
                    post[1],
                    f"❌ تم رفض إعلانك.\n\n"
                    f"💬 السبب: {reason}\n\n"
                    f"📌 يمكنك تعديله وإعادة النشر."
                )
            except:
                pass
        
        context.user_data['reject_post_id'] = None
        await update.message.reply_text(
            f"✅ تم رفض الإعلان #{post_id} وإشعار المعلن.",
            reply_markup=main_menu(user_id)
        )
        return

    # استلام إعلان جديد
    if context.user_data.get('waiting_for_post'):
        photo_id = photo[-1].file_id if photo else None
        
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        c.execute("INSERT INTO posts (user_id, text, photo_id, status) VALUES (?, ?, ?, 'pending')",
                  (user_id, text, photo_id))
        conn.commit()
        conn.close()
        
        context.user_data['waiting_for_post'] = False
        
        await update.message.reply_text(
            "✅ تم استلام إعلانك!\n"
            "📌 قيد المراجعة من المشرف.\n"
            "🕒 سيتم إشعارك عند الموافقة أو الرفض.",
            reply_markup=main_menu(user_id)
        )
        
        # إشعار المشرفين
        for admin_id in ADMIN_IDS:
            try:
                await context.bot.send_message(
                    admin_id,
                    f"📢 إعلان جديد من {user_id}\n"
                    f"📝 {text[:100]}...\n"
                    f"🆔 اذهب إلى 'الإعلانات المعلقة' للمراجعة."
                )
            except:
                pass
        return

    # بث إشعار
    if context.user_data.get('waiting_for_broadcast'):
        if not is_admin(user_id):
            context.user_data['waiting_for_broadcast'] = False
            await update.message.reply_text("⛔ خاصة بالمشرفين.", reply_markup=main_menu(user_id))
            return
        
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        c.execute("SELECT user_id FROM users")
        users = c.fetchall()
        conn.close()
        
        sent = 0
        for user in users:
            try:
                await context.bot.send_message(user[0], f"📢 إشعار:\n\n{text}")
                sent += 1
            except:
                pass
        
        context.user_data['waiting_for_broadcast'] = False
        await update.message.reply_text(
            f"✅ أرسل إلى {sent} مستخدم.",
            reply_markup=main_menu(user_id)
        )
        return

    # أي رسالة غير معروفة
    await update.message.reply_text(
        "❓ استخدم الأزرار للتنقل.",
        reply_markup=main_menu(user_id)
    )

# ========== تشغيل البوت ==========
def main():
    app = Application.builder().token(TOKEN).build()
    
    # تسجيل المعالجات
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_message))
    
    print("✅ البوت يعمل... اضغط Ctrl+C للإيقاف")
    app.run_polling()

if __name__ == "__main__":
    main()
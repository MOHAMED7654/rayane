from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask, request, jsonify
import os
import asyncio
import threading
import requests
import time

# إعدادات البوت
BOT_TOKEN = "8519815975:AAHXPYn4psfjs27XwjR6VF9kSLdjucTjwI8"
SECRET_TOKEN = "my_secret_123"
WEBHOOK_URL = "https://rayanebbot.onrender.com/webhook"
PORT = int(os.environ.get('PORT', 10000))

app = Flask(__name__)

# === قائمة الأيديانات الجديدة ===
USER_IDS = [
    5592743997, 6795112628, 5807627117, 7145108955, 7613612920,
    6712236521, 5557878774, 6581292938, 6886241869, 5619175448,
    6964293134, 5688295689, 5982240406, 7119992441, 8375808263,
    5356507141, 6675672115, 7041826366, 6699219169, 6044649059,
    5999090994, 6696406725, 6171509723, 7222564726, 6785287067,
    8363650266, 6022007749, 6571216307, 6578949341, 8148031366
]

# المسموح لهم باستخدام الأوامر
ALLOWED_IDS = {
    7635779264,   # المطور
    8435281777,   # الشخص الأول
    6571216307    # الشخص الثاني
}

DEVELOPER_ID = 7635779264

# إنشاء تطبيق البوت
application = Application.builder().token(BOT_TOKEN).build()

async def check_permissions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    # السماح المباشر للـ ALLOWED_IDS + المطور
    if user_id in ALLOWED_IDS:
        return True

    # السماح لمشرفي المجموعة فقط
    if update.message.chat.type in ["group", "supergroup"]:
        try:
            chat_id = update.message.chat_id
            admins = await context.bot.get_chat_administrators(chat_id)
            admin_ids = [admin.user.id for admin in admins]
            return user_id in admin_ids
        except:
            return False
    
    return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_permissions(update, context):
        return
    
    user = update.message.from_user
    welcome_text = f"""🎊 مرحباً {user.first_name}!

🤖 البوت: بوت التاق الجماعي
⚡ يقوم بعمل تاق لـ {len(USER_IDS)} عضو

📧 الحساب: @Mik_emm

📋 الأوامر المتاحة:
/tagall - عمل تاق لجميع الأعضاء

💡 لعمل تاق: أرسل /tagall"""
    
    await update.message.reply_text(welcome_text, disable_web_page_preview=True)

async def tag_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_permissions(update, context):
        return

    mention_texts = [f"<a href='tg://user?id={uid}'>•</a>" for uid in USER_IDS]
    message = " ".join(mention_texts)
    await update.message.reply_text(message, parse_mode='HTML')

# إضافة handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("tagall", tag_all))

@app.route('/')
def home():
    return "🤖 بوت التاق الجماعي يعمل مع Webhook - @Mik_emm"

@app.route('/health')
def health():
    return "✅ البوت يعمل بشكل صحيح"

# إنشاء event loop منفصل
bot_loop = asyncio.new_event_loop()

def process_update_sync(update_data):
    async def process_async():
        try:
            update = Update.de_json(update_data, application.bot)
            await application.process_update(update)
        except Exception as e:
            print(f"⚠️ خطأ في معالجة التحديث: {e}")
    
    asyncio.run_coroutine_threadsafe(process_async(), bot_loop)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('X-Telegram-Bot-Api-Secret-Token') != SECRET_TOKEN:
        return jsonify({"status": "error", "message": "Forbidden"}), 403
    
    try:
        update_data = request.get_json()
        process_update_sync(update_data)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"❌ خطأ في webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

async def setup_webhook():
    try:
        await application.initialize()
        await application.start()
        await application.bot.set_webhook(
            url=WEBHOOK_URL,
            secret_token=SECRET_TOKEN,
            drop_pending_updates=True
        )
        print("✅ تم تعيين Webhook بنجاح!")
    except Exception as e:
        print(f"❌ خطأ في تعيين Webhook: {e}")

def run_bot_loop():
    asyncio.set_event_loop(bot_loop)
    bot_loop.run_forever()

def start_bot():
    try:
        loop_thread = threading.Thread(target=run_bot_loop, daemon=True)
        loop_thread.start()
        asyncio.run_coroutine_threadsafe(setup_webhook(), bot_loop)
    except Exception as e:
        print(f"❌ خطأ في بدء البوت: {e}")

# ----- نبضة الحياة لمنع السبات -----
def keep_alive():
    url = "https://rayanebbot.onrender.com/health"
    while True:
        try:
            requests.get(url)
            print("💓 نبضة حياة تم إرسالها للحفاظ على البوت نشط")
        except Exception as e:
            print(f"❌ خطأ في نبضة الحياة: {e}")
        
        time.sleep(300)  # كل 5 دقائق

# ----- تشغيل كل شيء -----
if __name__ == "__main__":
    print(f"🚀 بدء تشغيل البوت...")
    print(f"📧 المطور: @Mik_emm")

    # تشغيل نبضة الحياة
    heartbeat_thread = threading.Thread(target=keep_alive, daemon=True)
    heartbeat_thread.start()

    # بدء البوت
    start_bot()

    print(f"🌐 تشغيل السيرفر على port {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)


from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask, request, jsonify
import os
import asyncio
import threading

# إعدادات البوت
BOT_TOKEN = "7383216151:AAEaD8BsdXhCyf-Ek7kYCcml9p-88xFvQMY"
SECRET_TOKEN = "my_secret_123"
WEBHOOK_URL = "https://rayanebbot.onrender.com/webhook"
PORT = int(os.environ.get('PORT', 10000))

app = Flask(__name__)

# قائمة الأيديانات الكاملة
USER_IDS = [
    5280469859, 5050233048, 6529610870, 5162944665, 5865749707,
    5895975234, 5471981588, 7160694880, 6137472806, 5656742718,
    7756099247, 8212828112, 7846745264, 8488306059, 6605734186,
    6022281494, 8430441112, 5945043931, 6697785303, 5168545800,
    5976402210, 6251555634, 5939301889, 5781392258, 2066573460,
    6556920201, 7975592822, 5678391804, 8487100883, 6019338682,
    6547513045, 7994548186, 5570625096, 7457028027, 5587961611,
    5046283890, 5362271964, 8072491430, 8394179289, 5494507856,
    7804755639, 7743058014, 7443386013, 7304051315, 6519425672,
    6406749226, 6351063786, 6061503802, 6017365522, 5775010322,
    5629751714, 5335249266, 5046140529, 2037438285, 2002345779,
    1995582641, 1960203863, 1816184446, 7635779264, 1499667757
]

DEVELOPER_ID = 7635779264

# إنشاء تطبيق البوت
application = Application.builder().token(BOT_TOKEN).build()

async def check_permissions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id == DEVELOPER_ID:
        return True
    if update.message.chat.type not in ["group", "supergroup"]:
        return False
    try:
        chat_id = update.message.chat_id
        admins = await context.bot.get_chat_administrators(chat_id)
        admin_ids = [admin.user.id for admin in admins]
        return user_id in admin_ids
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_permissions(update, context):
        return
    
    user = update.message.from_user
    welcome_text = f"""🎊 مرحباً {user.first_name}!

🤖 البوت: بوت التاق الجماعي
⚡ الوصف: يقوم بعمل تاق لـ {len(USER_IDS)} عضو

📧 الحساب: @Mik_emm (https://t.me/Mik_emm)

📋 الأوامر المتاحة:
/tagall - عمل تاق لجميع الأعضاء

💡 لعمل تاق: أرسل /tagall"""
    
    await update.message.reply_text(welcome_text, disable_web_page_preview=True)

async def tag_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_permissions(update, context):
        return
    
    # بدون try/except - لا ترسل رسالة خطأ
    mention_texts = []
    for user_id in USER_IDS:
        mention_texts.append(f"<a href='tg://user?id={user_id}'>•</a>")
    
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
    """معالجة التحديث بشكل متزامن في الـ loop المنفصل"""
    async def process_async():
        try:
            update = Update.de_json(update_data, application.bot)
            await application.process_update(update)
        except Exception as e:
            print(f"⚠️ خطأ في معالجة التحديث: {e}")
    
    asyncio.run_coroutine_threadsafe(process_async(), bot_loop)

@app.route('/webhook', methods=['POST'])
def webhook():
    # التحقق من الـ Secret Token
    if request.headers.get('X-Telegram-Bot-Api-Secret-Token') != SECRET_TOKEN:
        return jsonify({"status": "error", "message": "Forbidden"}), 403
    
    try:
        # معالجة التحديث في الـ loop المنفصل
        update_data = request.get_json()
        process_update_sync(update_data)
        
        return jsonify({"status": "success"}), 200
        
    except Exception as e:
        print(f"❌ خطأ في webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

async def setup_webhook():
    """تعيين Webhook"""
    try:
        await application.initialize()
        await application.start()
        
        # تعيين Webhook
        await application.bot.set_webhook(
            url=WEBHOOK_URL,
            secret_token=SECRET_TOKEN,
            drop_pending_updates=True
        )
        print("✅ تم تعيين Webhook بنجاح!")
        print(f"🌐 Webhook URL: {WEBHOOK_URL}")
        print("🤖 البوت جاهز لاستقبال الرسائل!")
        
    except Exception as e:
        print(f"❌ خطأ في تعيين Webhook: {e}")

def run_bot_loop():
    """تشغيل event loop البوت"""
    asyncio.set_event_loop(bot_loop)
    bot_loop.run_forever()

def start_bot():
    """بدء تشغيل البوت"""
    try:
        # تشغيل الـ loop في thread منفصل
        loop_thread = threading.Thread(target=run_bot_loop, daemon=True)
        loop_thread.start()
        
        # تعيين Webhook
        asyncio.run_coroutine_threadsafe(setup_webhook(), bot_loop)
        
    except Exception as e:
        print(f"❌ خطأ في بدء البوت: {e}")

if __name__ == "__main__":
    # بدء البوت
    print(f"🚀 بدء تشغيل البوت مع Webhook...")
    print(f"📧 المطور: @Mik_emm")
    
    # تشغيل إعداد Webhook
    start_bot()
    
    # تشغيل Flask
    print(f"🌐 تشغيل السيرفر على port {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import logging

# تفعيل اللوغ لرؤية الأخطاء
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# إعدادات البوت
BOT_TOKEN = "7383216151:AAGTRnZNR1ZweoG7PNtT1VzgWxYNzL29D5w"

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
    1995582641, 1960203863, 1816184446, 1499667757
]

# أيدي المطور (أنت)
DEVELOPER_ID = 7635779264

def check_permissions(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id == DEVELOPER_ID:
        return True
    
    if update.message.chat.type not in ["group", "supergroup"]:
        update.message.reply_text("❌ هذا البوت للمجموعات فقط!")
        return False
    
    try:
        chat_id = update.message.chat_id
        bot = context.bot
        admins = bot.get_chat_administrators(chat_id)
        admin_ids = [admin.user.id for admin in admins]
        
        if user_id in admin_ids:
            return True
        else:
            update.message.reply_text("❌ يجب أن تكون مشرف في المجموعة!")
            return False
    except Exception as e:
        update.message.reply_text("❌ حدث خطأ في التحقق من الصلاحيات!")
        return False

def start(update: Update, context: CallbackContext):
    if not check_permissions(update, context):
        return
    
    user = update.message.from_user
    is_developer = user.id == DEVELOPER_ID
    
    welcome_text = f"""🎊 **مرحباً {user.first_name}!**

🤖 **البوت:** بوت التاق الجماعي
⚡ **الوصف:** يقوم بعمل تاق لـ {len(USER_IDS)} عضو

{'👑 **أنت المطور**' if is_developer else '👨‍💼 **أنت مشرف**'}

📧 **الحساب:** [@Mik_emm](https://t.me/Mik_emm)

📋 **الأوامر المتاحة:**
/tagall - عمل تاق لجميع الأعضاء

💡 **لعمل تاق:** أرسل /tagall"""
    
    update.message.reply_text(welcome_text, parse_mode='Markdown', disable_web_page_preview=True)

def tag_all(update: Update, context: CallbackContext):
    if not check_permissions(update, context):
        return
    
    try:
        mention_texts = []
        for user_id in USER_IDS:
            mention_texts.append(f"<a href='tg://user?id={user_id}'>⁠</a>")
        
        message = " ".join(mention_texts)
        update.message.reply_text(message, parse_mode='HTML')
        
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("🚀 بدء تشغيل البوت...")
    
    # إنشاء البوت
    updater = Updater(BOT_TOKEN, use_context=True)
    
    # إضافة handlers
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("tagall", tag_all))
    
    print("🤖 بوت التاق الجماعي يعمل...")
    print(f"👑 المطور: {DEVELOPER_ID} (@Mik_emm)")
    print(f"👥 عدد الأعضاء المضافين: {len(USER_IDS)}")
    print("🎯 الأوامر المتاحة: /start, /tagall")
    print("🔄 جاري التشغيل بالبولينغ...")
    
    # بدء البوت
    updater.start_polling()
    print("✅ البوت يعمل ويستقبل الأوامر...")
    
    # إبقاء البوت يعمل
    updater.idle()

if __name__ == "__main__":
    main()

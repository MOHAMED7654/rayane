from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# إعدادات البوت
BOT_TOKEN = "7383216151:AAH4zKoZAuD5jgXu87O5k-CzU19NyAQdS7o"

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
    1995582641, 1960203863, 1816184446,7635779264, 1499667757
]

# أيدي المطور (أنت)
DEVELOPER_ID = 7635779264

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
    is_developer = user.id == DEVELOPER_ID
    
    welcome_text = f"""🎊 **مرحباً {user.first_name}!**

🤖 **البوت:** بوت التاق الجماعي
⚡ **الوصف:** يقوم بعمل تاق لـ {len(USER_IDS)} عضو

{'👑 **أنت المطور**' if is_developer else '👨‍💼 **أنت مشرف**'}

📧 **الحساب:** [@Mik_emm](https://t.me/Mik_emm)

📋 **الأوامر المتاحة:**
/tagall - عمل تاق لجميع الأعضاء

💡 **لعمل تاق:** أرسل /tagall"""
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown', disable_web_page_preview=True)

async def tag_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_permissions(update, context):
        return
    
    try:
        # عمل تاق باستخدام mentions مرئية
        mention_texts = []
        for user_id in USER_IDS:
            mention_texts.append(f"<a href='tg://user?id={user_id}'>•</a>")
        
        # رسالة واحدة كاملة
        message = " ".join(mention_texts)
        await update.message.reply_text(message, parse_mode='HTML')
        
    except Exception as e:
        pass

def main():
    # إنشاء البوت
    application = Application.builder().token(BOT_TOKEN).build()
    
    # إضافة handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("tagall", tag_all))
    
    print("🤖 بوت التاق الجماعي يعمل...")
    print(f"👑 المطور: {DEVELOPER_ID} (@Mik_emm)")
    print(f"👥 عدد الأعضاء المضافين: {len(USER_IDS)}")
    print("🎯 الأوامر المتاحة: /start, /tagall")
    print("🔄 جاري التشغيل بالبولينغ...")
    
    # بدء البوت
    application.run_polling()

if __name__ == "__main__":
    main()

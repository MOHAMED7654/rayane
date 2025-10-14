from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

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

async def check_permissions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """التحقق من أن المستخدم هو المطور أو مشرف في المجموعة"""
    user_id = update.message.from_user.id
    
    # إذا كان المستخدم هو المطور، اسمح له دائماً
    if user_id == DEVELOPER_ID:
        return True
    
    # التحقق من أن الأمر في مجموعة
    if update.message.chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("❌ هذا البوت للمجموعات فقط!")
        return False
    
    # التحقق من أن المستخدم مشرف باستخدام طريقة بديلة
    try:
        chat_id = update.message.chat_id
        admins = await context.bot.get_chat_administrators(chat_id)
        admin_ids = [admin.user.id for admin in admins]
        
        if user_id in admin_ids:
            return True
        else:
            await update.message.reply_text("❌ يجب أن تكون مشرف في المجموعة لاستخدام هذا البوت!")
            return False
            
    except Exception as e:
        await update.message.reply_text("❌ لا يمكن التحقق من الصلاحيات. تأكد من إضافة البوت للمجموعة!")
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # التحقق من الصلاحيات
    if not await check_permissions(update, context):
        return
    
    user = update.message.from_user
    is_developer = user.id == DEVELOPER_ID
    
    welcome_text = f"""
🎊 **مرحباً {user.first_name}!**

🤖 **البوت:** بوت التاق الجماعي
⚡ **الوصف:** يقوم بعمل تاق لـ {len(USER_IDS)} عضو
 

 
📧 **الحساب:** [@Mik_emm](https://t.me/Mik_emm)

📋 **الأوامر المتاحة:**
/tagall - عمل تاق لجميع الأعضاء
 

💡 **لعمل تاق:** أرسل /tagall
    """
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown', disable_web_page_preview=True)

async def tag_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # التحقق من الصلاحيات
    if not await check_permissions(update, context):
        return
    
    await update.message.reply_text(f"🔄 جاري عمل تاق لـ {len(USER_IDS)} عضو...")
    
    try:
        # عمل تاق باستخدام الـ mentions
        mention_texts = []
        
        for user_id in USER_IDS:
            mention_texts.append(f"<a href='tg://user?id={user_id}'>⁠</a>")
        
        # تقسيم إلى رسالتين فقط
        half = len(mention_texts) // 2
        first_half = mention_texts[:half]
        second_half = mention_texts[half:]
        
        # الرسالة الأولى
        message1 = "📢 **تاق جماعي (1/2):**\n\n"
        message1 += " ".join(first_half)
        message1 += f"\n\n👥 {half} عضو | 🛠 @Mik_emm"
        
        # الرسالة الثانية
        message2 = "📢 **تاق جماعي (2/2):**\n\n"
        message2 += " ".join(second_half)
        message2 += f"\n\n👥 {len(second_half)} عضو | 🛠 @Mik_emm"
        
        # إرسال الرسائل
        await update.message.reply_text(message1, parse_mode='HTML')
        await update.message.reply_text(message2, parse_mode='HTML')
        
        await update.message.reply_text(f"✅ تم عمل تاق لـ {len(USER_IDS)} عضو بنجاح!")
        
    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ: {str(e)}")

async def tag_all_one_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تاق في رسالة واحدة فقط"""
    # التحقق من الصلاحيات
    if not await check_permissions(update, context):
        return
    
    await update.message.reply_text(f"🔄 جاري عمل تاق لـ {len(USER_IDS)} عضو في رسالة واحدة...")
    
    try:
        # عمل تاق باستخدام الـ mentions في رسالة واحدة
        mention_texts = []
        
        for user_id in USER_IDS:
            mention_texts.append(f"<a href='tg://user?id={user_id}'>⁠</a>")
        
        # رسالة واحدة كاملة
        message = "📢 **تاق جماعي لجميع الأعضاء:**\n\n"
        message += " ".join(mention_texts)
        message += f"\n\n👥 {len(USER_IDS)} عضو | 🛠 @Mik_emm"
        
        # إرسال الرسالة
        await update.message.reply_text(message, parse_mode='HTML')
        
    except Exception as e:
        # إذا كانت الرسالة طويلة جداً، نستخدم الطريقة المقسومة
        await tag_all(update, context)

async def show_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # التحقق من الصلاحيات
    if not await check_permissions(update, context):
        return
    
    members_text = f"""
📊 **إحصائيات الأعضاء المضافين:**

👥 **عدد الأعضاء:** {len(USER_IDS)}
🛠 **المطور:** [@Mik_emm](https://t.me/Mik_emm)

💡 **الأوامر المتاحة:**
/tagall - تاق في رسالتين
/tagone - تاق في رسالة واحدة
    """
    await update.message.reply_text(members_text, parse_mode='Markdown')

def main():
    # إنشاء تطبيق البوت
    application = Application.builder().token(BOT_TOKEN).build()
    
    # إضافة handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("tagall", tag_all))
    application.add_handler(CommandHandler("tagone", tag_all_one_message))
    application.add_handler(CommandHandler("members", show_members))
    
    # بدء البوت
    print("🤖 بوت التاق الجماعي يعمل...")
    print(f"👑 المطور: {DEVELOPER_ID} (@Mik_emm)")
    print(f"👥 عدد الأعضاء المضافين: {len(USER_IDS)}")
    print("🔒 البوت يعمل فقط للمشرفين والمطور")
    print("🚫 البوت لا يحتاج إلى صلاحيات مشرف")
    print("📨 التاق في رسالة أو رسالتين فقط")
    print("⚡ جاهز على Render...")
    
    application.run_polling()

if __name__ == "__main__":
    main()

import io
import logging
import requests
import cloudscraper
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# লগিং সেটআপ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# টোকেন ও কনফিগারেশন
BOT_TOKEN = '8242188726:AAH0UCO-NbPAHsnsRnfJrSsM4qzDW2yxEcg'
CHANNEL_USERNAME = '@unknownapps1'
BOT_NAME_HEADER = "👑 TAMIM VAI PRO EXTRACTOR 👑\n\n"
DEVELOPER_SIGNATURE = "\n\nDEVELOPER TAMIM BHAI"

user_codes_db = {}
user_states = {}
total_users = set()
total_files_generated = 0

def get_main_keyboard():
    return ReplyKeyboardMarkup([
        ["📝 Coding To File", "🌐 Link To File"],
        ["📊 Statistic"],
        ["👨‍💻 Support", "👑 Developer"]
    ], resize_keyboard=True)

async def check_membership(user_id: int, bot) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except: return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    total_users.add(user_id)
    if not await check_membership(user_id, context.bot):
        keyboard = [[InlineKeyboardButton("Join Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")]]
        await update.message.reply_text(f"{BOT_NAME_HEADER}বটটি ব্যবহার করতে আগে জয়েন করুন।{DEVELOPER_SIGNATURE}", reply_markup=InlineKeyboardMarkup(keyboard))
        return
    await update.message.reply_text(f"{BOT_NAME_HEADER}তামিম ভাই, ফোন অফ থাকলেও আমি এখন কাজ করবো! লিংক দিন।{DEVELOPER_SIGNATURE}", reply_markup=get_main_keyboard())

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    total_users.add(user_id)

    if text == "📝 Coding To File":
        user_states[user_id] = "CODE"
        await update.message.reply_text(f"{BOT_NAME_HEADER}আপনার কোডটি পেস্ট করুন।{DEVELOPER_SIGNATURE}")
    elif text == "🌐 Link To File":
        user_states[user_id] = "LINK"
        await update.message.reply_text(f"{BOT_NAME_HEADER}যেকোনো লিংকে দিন। আমি অল-ইন-ওয়ান লজিক দিয়ে কোড আনছি।{DEVELOPER_SIGNATURE}")
    elif text == "📊 Statistic":
        await update.message.reply_text(f"{BOT_NAME_HEADER}📊 পরিসংখ্যান:\n👥 ইউজার: {len(total_users)}\n📁 ফাইল: {total_files_generated}{DEVELOPER_SIGNATURE}")
    elif text in ["👨‍💻 Support", "👑 Developer"]:
        await update.message.reply_text(f"{BOT_NAME_HEADER}সাপোর্ট: @tamim_bhai_dv{DEVELOPER_SIGNATURE}")
    else:
        state = user_states.get(user_id)
        if state == "LINK":
            proc = await update.message.reply_text("⚡ রিয়েল কোডিং এক্সট্রাক্ট করা হচ্ছে...")
            try:
                url = text if text.startswith("http") else "http://" + text
                # প্রফেশনাল স্ক্র্যাপার লজিক
                scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True})
                response = scraper.get(url, timeout=30)
                
                if response.status_code == 200:
                    user_codes_db[user_id] = response.text
                    await proc.delete()
                    await send_ext_menu(update)
                else:
                    await proc.edit_text(f"{BOT_NAME_HEADER}সাইটটি হয়তো ব্লক করা।{DEVELOPER_SIGNATURE}")
            except Exception as e:
                await proc.edit_text(f"এরর: {e}")
        elif state == "CODE":
            user_codes_db[user_id] = text
            await send_ext_menu(update)

async def send_ext_menu(update: Update):
    keyboard = [
        [InlineKeyboardButton("HTML (.html)", callback_data=".html"), InlineKeyboardButton("JS (.js)", callback_data=".js")],
        [InlineKeyboardButton("PY (.py)", callback_data=".py"), InlineKeyboardButton("PHP (.php)", callback_data=".php")],
        [InlineKeyboardButton("CSS (.css)", callback_data=".css"), InlineKeyboardButton("TXT (.txt)", callback_data=".txt")]
    ]
    await update.message.reply_text(f"{BOT_NAME_HEADER}সঠিক কোড পাওয়া গেছে! ফরম্যাট বেছে নিন।{DEVELOPER_SIGNATURE}", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global total_files_generated
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    ext = query.data
    code = user_codes_db.get(user_id)

    if code:
        file_data = io.BytesIO(code.encode('utf-8'))
        file_data.name = f"Tamim_Source{ext}"
        await context.bot.send_document(chat_id=user_id, document=file_data, caption=f"{BOT_NAME_HEADER}আপনার ফাইল তৈরি।{DEVELOPER_SIGNATURE}")
        total_files_generated += 1
    else:
        await query.message.reply_text("আবার ট্রাই করুন।")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))
    app.add_handler(CallbackQueryHandler(button_callback))
    print("Bot is running...")
    app.run_polling()

import telebot
import base64
from datetime import datetime

# আপনার বট টোকেন
TOKEN = '8684625421:AAG1OZBtpMob7XcKgY9O_8MSxgQKjaseL90'
bot = telebot.TeleBot(TOKEN)

# প্রটেক্টেড হেডার টেমপ্লেট
def get_header():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f""""""
    return header

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "স্বাগতম! আপনার HTML ফাইলটি পাঠান, আমি সেটিকে TAMIM OBSCUREATOR দিয়ে প্রটেক্ট করে দেব।")

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    if message.document.file_name.endswith('.html'):
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        original_code = downloaded_file.decode('utf-8')

        # লজিক: হেডার চেক করার স্ক্রিপ্ট যোগ করা
        # যদি কেউ 'TAMIM_HTML_PROTECTED' লেখাটি মুছে ফেলে, তবে পেজ ব্ল্যাঙ্ক হয়ে যাবে বা লক হবে
        encoded_content = base64.b64encode(original_code.encode('utf-8')).decode('utf-8')

        protected_html = f"""{get_header()}
<script>
    (function() {{
        const h = document.documentElement.innerHTML;
        if (!h.includes('TAMIM_HTML_PROTECTED')) {{
            document.body.innerHTML = '<h1 style="color:red; text-align:center; margin-top:20%;">SCREEN LOCKED: Unauthorized Modification!</h1>';
            alert('Header modified! System locked by TAMIM OBSCUREATOR.');
            throw new Error('Unauthorized');
        }}
    }})();
</script>
<script>
    document.write(atob('{encoded_content}'));
</script>"""

        with open("protected_file.html", "w", encoding="utf-8") as f:
            f.write(protected_html)

        with open("protected_file.html", "rb") as f:
            bot.send_document(message.chat.id, f, caption="✅ Your HTML is Protected by TAMIM OBSCUREATOR")
    else:
        bot.reply_to(message, "অনুগ্রহ করে একটি .html ফাইল পাঠান।")

print("Bot is running...")
bot.polling()
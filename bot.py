TAMIM OBSUCREATOR BOT

Fixed Full Working Version

IMPORTANT: Replace with your NEW bot token from BotFather

import telebot from datetime import datetime import os

BOT_TOKEN = "8684625421:AAH_YOM0KENnGCVgjAe2jt-Fb6f4qfOVtjM" BOT_NAME = "TAMIM OBSUCREATOR BOT" CHANNEL_LINK = "https://t.me/unknownapps1" SIGNATURE = "TAMIM_HTML_PROTECTED"

bot = telebot.TeleBot(BOT_TOKEN)

HEADER_TEMPLATE = """<!--
╔══════════════════════════════════════════════════════════╗
║  🔒 PROTECTED HTML - DO NOT MODIFY THIS HEADER 🔒       ║
║══════════════════════════════════════════════════════════║
║  Obfuscated By:   @tamim_obsucreator_bot               ║
║  TG Channel : {channel}                                ║
║  Timestamp: {timestamp}                                ║
║  Signature: {signature}                                ║
║══════════════════════════════════════════════════════════║
║  ⚠ WARNING: Removing or modifying this credit header   ║
║  will cause this page to stop working!                 ║
╚══════════════════════════════════════════════════════════╝
--> """

PROTECTION_SCRIPT = """

<script>
(function(){
    const requiredSignature = 'TAMIM_HTML_PROTECTED';

    function lockScreen(){
        document.body.innerHTML = `
            <div style="display:flex;align-items:center;justify-content:center;height:100vh;background:#000;color:#fff;font-family:sans-serif;text-align:center;padding:20px;">
                <div>
                    <h1>ACCESS BLOCKED</h1>
                    <p>Protected Header Removed or Modified!</p>
                    <p>This HTML is locked by TAMIM OBSUCREATOR BOT</p>
                </div>
            </div>
        `;

        document.documentElement.style.overflow = 'hidden';

        setInterval(function(){
            document.body.innerHTML = `
                <div style="display:flex;align-items:center;justify-content:center;height:100vh;background:#000;color:#fff;font-family:sans-serif;text-align:center;padding:20px;">
                    <div>
                        <h1>ACCESS BLOCKED</h1>
                        <p>Protected Header Removed!</p>
                    </div>
                </div>
            `;
        }, 1000);
    }

    const source = document.documentElement.innerHTML;

    if (!source.includes(requiredSignature)) {
        lockScreen();
    }

    document.addEventListener('contextmenu', function(e){
        e.preventDefault();
    });

    document.addEventListener('keydown', function(e){
        if (
            e.key === 'F12' ||
            (e.ctrlKey && e.shiftKey && ['I','J','C'].includes(e.key.toUpperCase()))
        ) {
            e.preventDefault();
        }
    });
})();
</script>"""

def protect_html(content): timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

header = HEADER_TEMPLATE.format(
    channel=CHANNEL_LINK,
    timestamp=timestamp,
    signature=SIGNATURE
)

protected = header + "\n" + PROTECTION_SCRIPT + "\n" + content
return protected

@bot.message_handler(commands=['start']) def start(message): text = f"""👋 Welcome!

🔒 {BOT_NAME}

Send your HTML file and I will protect it.

Features: ✅ Header Signature Lock ✅ Right Click Block ✅ Devtools Key Block ✅ Credit Protection ✅ Screen Lock if Header Removed ✅ Protected HTML Output """

bot.reply_to(message, text)

@bot.message_handler(content_types=['document']) def handle_file(message): try: file_info = bot.get_file(message.document.file_id) downloaded_file = bot.download_file(file_info.file_path)

original_name = message.document.file_name
    input_path = original_name
    output_path = f"protected_{original_name}"

    with open(input_path, 'wb') as file:
        file.write(downloaded_file)

    with open(input_path, 'r', encoding='utf-8', errors='ignore') as file:
        html_content = file.read()

    protected_content = protect_html(html_content)

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(protected_content)

    with open(output_path, 'rb') as file:
        bot.send_document(
            message.chat.id,
            file,
            caption="✅ Your HTML is Protected by TAMIM OBSUCREATOR"
        )

    if os.path.exists(input_path):
        os.remove(input_path)

    if os.path.exists(output_path):
        os.remove(output_path)

except Exception as e:
    bot.reply_to(message, f"Error: {str(e)}")

print(f"{BOT_NAME} is running...") bot.infinity_polling()

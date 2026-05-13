#!/data/data/com.termux/files/usr/bin/python

import requests, uuid, random, os, sys, time
import telebot
from telebot import types

# ================== REPLY KEYBOARD ==================
markup = types.ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True)
markup.row("Get Cookies", "Refresh All")

# ================== GLOBAL ==================
BOT_TOKEN = None
bot = None

def clear():
    os.system('clear')

# ================== TOKEN INPUT ==================
def get_bot_token():
    global BOT_TOKEN
    print("\n🤖  FB Cookie Extractor Bot")
    print("="*40)
    
    token = input("Enter your Telegram Bot Token: ").strip()
    
    if not token or ":" not in token or len(token) < 30:
        print("❌ Invalid Token!")
        sys.exit(1)
    
    BOT_TOKEN = token
    print("✅ Token accepted.\n")
    return token

# ================== FACEBOOK LOGIN ==================
def fb_login(uid, ps):
    adid = str(uuid.uuid4())
    data = {
        "adid": adid, "format": "json", "device_id": str(uuid.uuid4()),
        "cpl": "true", "family_device_id": str(uuid.uuid4()),
        "credentials_type": "device_based_login_password",
        "source": "device_based_login", "email": uid, "password": ps,
        "access_token": "350685531728|62f8ce9f74b12f84c123cc23437a4a32",
        "generate_session_cookies": "1", "meta_inf_fbmeta": "",
        "advertiser_id": str(uuid.uuid4()), "locale": "en_GB",
        "client_country_code": "GB", "method": "auth.login",
        "fb_api_req_friendly_name": "authenticate",
        "fb_api_caller_class": "com.facebook.account.login.protocol.Fb4aAuthHandler",
        "api_key": "882a8490361da98702bf97a021ddc14d"
    }

    head = {
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10; SM-N960F Build/QP1A.190711.020) [FBAN/Orca-Android;FBAV/257.1.0.21.120;FBPN/com.facebook.orca;FBLC/en_US;FBCR/null;FBMF/samsung;FBBD/samsung;FBDV/SM-N960F;FBSV/10;FBCA/arm64-v8a:null;FBDM={density=2.625,width=1080,height=2094};FB_FW/1;] FBBK/1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'graph.facebook.com',
        'X-FB-Net-HNI': str(random.randint(20000, 40000)),
        'X-FB-SIM-HNI': str(random.randint(20000, 40000)),
        'X-FB-Connection-Type': 'MOBILE.LTE',
        'X-fb-connection-token': 'd29d67d37eca387482a8a5b740f84f62',
    }

    try:
        po = requests.post('https://b-graph.facebook.com/auth/login', 
                          data=data, headers=head, timeout=30).json()

        if 'session_key' in po:
            cookies = ";".join([f"{i['name']}={i['value']}" for i in po.get("session_cookies", [])])
            return {"status": "success", "uid": po.get('uid'), "cookies": cookies}
        elif 'checkpoint' in str(po).lower() or 'www.facebook.com' in str(po):
            return {"status": "checkpoint"}
        else:
            return {"status": "failed"}
    except:
        return {"status": "error"}

# ================== BOT HANDLERS ==================
def register_handlers():
    global bot
    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.chat.id, 
            f"👋 <b>Welcome {message.from_user.first_name}!</b>\n\n"
            f"🤖 <b>FB Self Login & Cookie Extractor Bot</b>\n\n"
            f"নিচের বাটন ব্যবহার করুন 👇", 
            parse_mode='HTML', reply_markup=markup)

    @bot.message_handler(func=lambda m: True)
    def button_handler(message):
        text = message.text

        if text == "Refresh All":
            start(message)
            return

        elif text == "Get Cookies":
            msg = bot.send_message(message.chat.id, "🔑 <b>ইউজারনেম / ইমেইল / ফোন নাম্বার দাও:</b>", parse_mode='HTML')
            bot.register_next_step_handler(msg, process_username)
            return

        bot.send_message(message.chat.id, "🤖 Use the buttons below.", reply_markup=markup)

    def process_username(message):
        username = message.text
        msg = bot.send_message(message.chat.id, "🔒 <b>এখন পাসওয়ার্ড দাও:</b>", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_password, username)

    def process_password(message, username):
        password = message.text
        msg = bot.send_message(message.chat.id, "⏳ <b>Logging in... Please wait...</b>", parse_mode='HTML')

        result = fb_login(username, password)

        if result["status"] == "success":
            response = (
                f"✅ <b>LOGIN SUCCESSFUL!</b>\n\n"
                f"👤 <b>UID:</b> <code>{result['uid']}</code>\n\n"
                f"🍪 <b>Cookies:</b>\n<code>{result['cookies']}</code>"
            )
            bot.edit_message_text(response, message.chat.id, msg.message_id, parse_mode='HTML')

        elif result["status"] == "checkpoint":
            bot.edit_message_text("⚠️ <b>Checkpoint / 2FA Required!</b>", message.chat.id, msg.message_id, parse_mode='HTML')
        else:
            failed_msg = (
                "❌ <b>লগইন ব্যর্থ হয়েছে!</b>\n\n"
                "🔍 অ্যাকাউন্ট তৈরি করার সাথে সাথে কুকিজ বের করতে হয়\n"
                "✈️ একাউন্ট বেশি ওল্ড হইলে সমস্যা হয়"
            )
            bot.edit_message_text(failed_msg, message.chat.id, msg.message_id, parse_mode='HTML')

        bot.send_message(message.chat.id, "✅ Done! Use buttons below.", reply_markup=markup)

# ================== MAIN ==================
def main():
    global bot
    clear()
    
    get_bot_token()
    
    bot = telebot.TeleBot(BOT_TOKEN)
    register_handlers()          # ← Important: register after bot is created
    
    print("🤖 Bot is Running...")
    print("="*50)
    print("✅ Bot Started Successfully 🔥")
    print("✅ Now open Telegram and send /start")
    print("="*50)
    
    bot.infinity_polling(none_stop=True, interval=1, timeout=90)

if __name__ == '__main__':
    main()
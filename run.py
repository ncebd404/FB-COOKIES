#!/data/data/com.termux/files/usr/bin/python3

import os
import sys
import subprocess
import telebot
import time
import threading
from telebot import apihelper


# Auto update
try:
    print("[*] Checking for updates...")
    subprocess.run(["git", "pull"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print("[+] Update completed!")
except:
    print("[!] Update skipped.")

try:
    import tool
    print("[+] tool loaded successfully!")

    bot = tool.bot
    BOT_TOKEN = tool.BOT_TOKEN if hasattr(tool, 'BOT_TOKEN') else None

    if not BOT_TOKEN:
        print("[-] BOT_TOKEN not found!")
        sys.exit(1)

    print(f"[+] Bot is running with token: {BOT_TOKEN[:15]}...")

    
    apihelper.SESSION_TIME_TO_LIVE = 5 * 60      
    apihelper.READ_TIMEOUT = 60
    apihelper.CONNECT_TIMEOUT = 15

    print("[+] Anti-idle & reconnect settings applied")


    def start_bot():
        print("[*] Starting robust Telegram Bot (will auto-reconnect on network loss)...")
        
        while True:                     
            try:
                bot.infinity_polling(
                    none_stop=True,
                    interval=1,
                    timeout=90,               
                    long_polling_timeout=60,
                    skip_pending=True,
                    allowed_updates=None,
                    logger_level=0            
                )
            except Exception as e:
                error_str = str(e).lower()
                if "connection" in error_str or "timeout" in error_str or "abort" in error_str or "reset" in error_str:
                    print(f"[!] Network issue detected: {e}")
                    print("[*] Waiting for network to come back... Retrying in 8 seconds")
                else:
                    print(f"[!] Unexpected error: {e}")
                
                time.sleep(8)   

    # Bot 
    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()

    print("\n" + "="*50)
    print("✅ Bot is Running 🔥🔥")
    print("✅ Send /start or any command from Telegram")
    print("="*50)

    
    while True:
        time.sleep(10)

except Exception as e:
    print(f"[-] Critical Error: {e}")
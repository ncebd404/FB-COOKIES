#!/data/data/com.termux/files/usr/bin/python3

import os
import sys
import subprocess
import time
import threading

# Auto update
try:
    print("[*] Checking for updates...")
    subprocess.run(["git", "pull"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print("[+] Update completed!")
except:
    print("[!] Update skipped.")

# Import tool (your main bot logic)
try:
    import tool
    print("[+] tool.py loaded successfully!")
except Exception as e:
    print(f"[-] Failed to import tool.py: {e}")
    sys.exit(1)

print("\n" + "="*50)
print(" FB Cookie Extractor Bot is Running ")
print(" Send /start in Telegram")
print("="*50)

# Keep the script alive
try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    print("\n[!] Bot stopped by user.")
    sys.exit(0)
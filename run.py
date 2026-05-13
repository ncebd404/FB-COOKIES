#!/data/data/com.termux/files/usr/bin/python3

import os
import sys
import subprocess
import time

# Auto update
try:
    print("[*] Checking for updates...")
    subprocess.run(["git", "pull"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print("[+] Update completed!")
except:
    print("[!] Update skipped.")

try:
    import tool
    
    print("[+] tool.py loaded successfully!")
    
    # এখানে main() কল করা হচ্ছে — টোকেন ইনপুট নেবে
    tool.main()

except Exception as e:
    print(f"[-] Critical Error: {e}")
    sys.exit(1)

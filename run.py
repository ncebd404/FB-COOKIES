#!/data/data/com.termux/files/usr/bin/python3

import os
import sys
import subprocess
import time
import threading

if '64' not in os.uname().machine:
    sys.exit("[-] Only 64-bit device supported!")

# Auto update
try:
    print("[*] Checking for updates...")
    subprocess.run(["git", "pull"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print("[+] Update completed!")
except:
    print("[!] Update skipped.")

try:
    import tool
    
    print("[+] Tool loaded successfully!")
    
    # Run the main function from tool.py
    if hasattr(tool, 'main'):
        tool.main()
    else:
        print("[-] main() function not found in tool.py")
        sys.exit(1)

except Exception as e:
    print(f"[-] Critical Error: {e}")
    import traceback
    traceback.print_exc()
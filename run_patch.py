import os
print("Checking index.html...")
if os.path.exists("index.html"):
    print("✅ index.html found. Ready to patch.")
else:
    print("❌ index.html not found in current directory!")

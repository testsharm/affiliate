import os
import zipfile
import shutil
import subprocess

ZIP_NAME = "promptpad.zip"

print("🚀 Starting PromptPad Automated Setup...")

if not os.path.exists(ZIP_NAME):
    print(f"\n❌ Error: '{ZIP_NAME}' not found in the current folder.")
    print("👉 Please drag and drop your 'promptpad.zip' file into the left sidebar of VS Code (Explorer), then run this command again: python3 setup.py")
    exit(1)

print("📦 Unzipping promptpad.zip...")
with zipfile.ZipFile(ZIP_NAME, 'r') as zip_ref:
    zip_ref.extractall("extracted_temp")

extracted_path = "extracted_temp/promptpad"
if not os.path.exists(extracted_path):
    extracted_path = "extracted_temp" # fallback

print("📂 Moving files to root repository directory...")
for item in os.listdir(extracted_path):
    s = os.path.os.path.join(extracted_path, item)
    d = os.path.os.path.join(".", item)
    if os.path.exists(d):
        if os.path.isdir(d):
            shutil.rmtree(d)
        else:
            os.remove(d)
    shutil.move(s, d)

# Also check for setup guide or root files from temp
for item in os.listdir("extracted_temp"):
    if item == "promptpad":
        continue
    s = os.path.join("extracted_temp", item)
    d = os.path.join(".", item)
    if not os.path.exists(d):
        shutil.move(s, d)

# Cleanup
shutil.rmtree("extracted_temp")
if os.path.exists(ZIP_NAME):
    os.remove(ZIP_NAME)

print("🔗 Staging and pushing files to GitHub...")
subprocess.run(["git", "config", "--global", "user.email", "bot@promptpad.local"], check=True)
subprocess.run(["git", "config", "--global", "user.name", "PromptPad Bot"], check=True)
subprocess.run(["git", "add", "."], check=True)
subprocess.run(["git", "commit", "-m", "Deploy PromptPad: Initial Setup"], check=True)

push_result = subprocess.run(["git", "push", "origin", "main"])
if push_result.returncode == 0:
    print("\n✅ SUCCESS! All files have been successfully pushed to your GitHub repository.")
    print("\n🌐 NEXT STEPS FOR VERCEL DEPLOYMENT:")
    print("1. Go to https://vercel.com/new")
    print("2. Import your GitHub repository ('affiliate')")
    print("3. Leave build settings as default and click Deploy.")
    print("   (Note: As mentioned in your guide, ensure you use Vercel Pro if operating an affiliate/commercial site to avoid compliance suspension).")
else:
    print("\n⚠️ Push encountered an issue. Please check your GitHub credentials or permissions.")


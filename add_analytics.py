import os
import subprocess

script_tag = '    <script defer src="/_vercel/insights/script.js"></script>\n</head>'
count = 0

for root, dirs, files in os.walk("."):
    if ".git" in root or "extracted_temp" in root:
        continue
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            if "_vercel/insights/script.js" not in content:
                if "</head>" in content:
                    content = content.replace("</head>", script_tag)
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(content)
                    count += 1

print(f"✨ Successfully injected analytics into {count} HTML pages!")

subprocess.run(["git", "config", "--global", "user.email", "bot@promptpad.local"], check=True)
subprocess.run(["git", "config", "--global", "user.name", "PromptPad Bot"], check=True)
subprocess.run(["git", "add", "."], check=True)
subprocess.run(["git", "commit", -m, "Add Vercel Web Analytics tracking"], check=True)
subprocess.run(["git", "push", "origin", "main"], check=True)
print("🚀 Changes pushed to GitHub! Vercel will auto-deploy your analytics in 30 seconds.")

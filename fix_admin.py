import os
import subprocess

print("🔧 Updating admin backend with instant fallback password...")
os.makedirs("api", exist_ok=True)

admin_code = """export default function handler(req, res) {
  const password = process.env.ADMIN_PASSWORD || process.env.PASSWORD || "PromptVault123!";

  if (req.method === 'GET') {
    return res.status(200).json({ setup_required: false, configured: true });
  }

  if (req.method === 'POST') {
    let body = req.body;
    if (typeof body === 'string') {
      try { body = JSON.parse(body); } catch(e) {}
    }
    const pass = body && body.pass;
    if (pass === password) {
      return res.status(200).json({ success: true });
    } else {
      return res.status(401).json({ success: false, message: "Invalid password" });
    }
  }

  return res.status(200).json({ success: true });
}
"""

with open("api/admin.js", "w", encoding="utf-8") as f:
    f.write(admin_code)

subprocess.run(["git", "config", "--global", "user.email", "bot@promptpad.local"], check=True)
subprocess.run(["git", "config", "--global", "user.name", "PromptPad Bot"], check=True)
subprocess.run(["git", "add", "."], check=True)
subprocess.run(["git", "commit", "-m", "Add instant password fallback"], check=True)
subprocess.run(["git", "push", "origin", "main"], check=True)
print("🚀 Pushed to GitHub! Vercel is auto-deploying right now.")

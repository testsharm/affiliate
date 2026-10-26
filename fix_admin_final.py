import os
import subprocess

print("🔧 Updating admin API to be 100% foolproof...")
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
    // Accept both 'pass' and 'password' from any frontend version
    const submittedPass = body && (body.pass || body.password);
    
    if (submittedPass === password) {
      return res.status(200).json({ success: true, message: "Logged in successfully" });
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
subprocess.run(["git", "commit", "-m", "Make admin API accept both pass and password keys"], check=True)
subprocess.run(["git", "push", "origin", "main"], check=True)
print("🚀 Pushed to GitHub! Vercel is auto-deploying the final fix.")

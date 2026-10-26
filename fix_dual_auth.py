import os
import subprocess

print("🔧 Updating admin API to accept both Vercel env password and PromptVault123!...")
os.makedirs("api", exist_ok=True)

admin_code = """export default async function handler(req, res) {
  const envPassword = process.env.ADMIN_PASSWORD || process.env.PASSWORD;
  const fallbackPassword = "PromptVault123!";

  if (req.method === 'GET') {
    return res.status(200).json({ setup_required: false, configured: true });
  }

  if (req.method === 'POST') {
    let body = req.body;

    if (!body && req.readable) {
      body = await new Promise((resolve) => {
        let data = '';
        req.on('data', chunk => { data += chunk; });
        req.on('end', () => {
          try { resolve(JSON.parse(data)); } catch(e) { resolve({ raw: data }); }
        });
      });
    }

    if (typeof body === 'string') {
      try { body = JSON.parse(body); } catch(e) {}
    }

    const submittedPass = body && (body.pass || body.password || body.key);

    const isValid = submittedPass === fallbackPassword || (envPassword && submittedPass === envPassword);

    if (isValid) {
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
subprocess.run(["git", "commit", "-m", "Support dual password authentication"], check=True)
subprocess.run(["git", "push", "origin", "main"], check=True)
print("🚀 Pushed to GitHub! Vercel is auto-deploying the dual-auth fix.")

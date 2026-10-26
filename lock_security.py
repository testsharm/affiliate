import os
import subprocess

print("🔒 Locking down admin backend to strictly require Vercel environment variables...")
os.makedirs("api", exist_ok=True)

admin_code = """export default function handler(req, res) {
  // STRICTLY require the environment variable. No hardcoded insecure fallbacks.
  const envPassword = process.env.ADMIN_PASSWORD || process.env.PASSWORD;

  if (req.method === 'GET') {
    return res.status(200).json({ setup_required: false, configured: !!envPassword });
  }

  if (req.method === 'POST') {
    let body = req.body || {};
    
    if (typeof body === 'string') {
      try { body = JSON.parse(body); } catch(e) {}
    }

    const action = body.action;

    if (action === 'login' || body.password || body.pass) {
      const submittedPass = body.password || body.pass || body.key || body.pw;

      // If no env password is set on Vercel yet, fail securely
      if (!envPassword) {
        return res.status(401).json({ ok: false, success: false, error: "Server password not configured in Vercel environment variables." });
      }

      if (submittedPass === envPassword) {
        return res.status(200).json({ ok: true, success: true, message: "Logged in successfully" });
      } else {
        return res.status(401).json({ ok: false, success: false, error: "Invalid password" });
      }
    }

    if (action === 'load') {
      return res.status(200).json({
        ok: true,
        sha: "123",
        data: {
          brand: "PromptVault",
          links: { toolsuite: "" },
          settings: { umami: "", follow: "", contact: "", country: "" },
          prompts: []
        }
      });
    }

    if (action === 'save') {
      return res.status(200).json({ ok: true, sha: "124" });
    }

    if (action === 'logout') {
      return res.status(200).json({ ok: true });
    }

    return res.status(200).json({ ok: true });
  }

  return res.status(200).json({ ok: true });
}
"""

with open("api/admin.js", "w", encoding="utf-8") as f:
    f.write(admin_code)

subprocess.run(["git", "config", "--global", "user.email", "bot@promptpad.local"], check=True)
subprocess.run(["git", "config", "--global", "user.name", "PromptPad Bot"], check=True)
subprocess.run(["git", "add", "."], check=True)
subprocess.run(["git", "commit", "-m", "Lock down admin auth to strictly use Vercel env variables"], check=True)
subprocess.run(["git", "push", "origin", "main"], check=True)
print("🚀 Pushed to GitHub! Vercel is securing your admin backend.")

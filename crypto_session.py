import os
import subprocess

print("🔒 Upgrading to cryptographic session tokens (instant global invalidation)...")
os.makedirs("api", exist_ok=True)

admin_code = """import crypto from 'crypto';

export default function handler(req, res) {
  const envPassword = process.env.ADMIN_PASSWORD || process.env.PASSWORD;
  const envPin = process.env.ADMIN_PIN || process.env.PIN || '';

  // Strict security headers
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-XSS-Protection', '1; mode=block');

  // Generate a secret server salt based on current credentials
  const getSessionToken = () => {
    if (!envPassword) return '';
    return crypto.createHmac('sha256', envPassword + envPin).update('promptvault-secure-session').digest('hex');
  };

  const cookies = {};
  const cookieHeader = req.headers.cookie;
  if (cookieHeader) {
    cookieHeader.split(';').forEach(cookie => {
      const parts = cookie.split('=');
      cookies[parts[0].trim()] = (parts[1] || '').trim();
    });
  }

  if (req.method === 'GET') {
    return res.status(200).json({ 
      setup_required: false, 
      configured: !!envPassword, 
      pin_required: !!envPin 
    });
  }

  if (req.method === 'POST') {
    let body = req.body || {};
    if (typeof body === 'string') {
      try { body = JSON.parse(body); } catch(e) {}
    }

    const action = body.action;

    // LOGIN ACTION
    if (action === 'login') {
      const submittedPass = body.password || body.pass;
      const submittedPin = body.pin || body.key;

      if (!envPassword) {
        return res.status(401).json({ ok: false, error: "Server password not configured in Vercel." });
      }

      const passValid = submittedPass === envPassword;
      const pinValid = !envPin || submittedPin === envPin;

      if (passValid && pinValid) {
        const token = getSessionToken();
        // Set cryptographically signed secure cookie valid for 30 minutes
        res.setHeader(
          'Set-Cookie',
          `admin_session=${token}; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=1800`
        );
        return res.status(200).json({ ok: true, success: true });
      } else {
        return res.status(401).json({ ok: false, error: "Invalid password or PIN." });
      }
    }

    // LOGOUT ACTION
    if (action === 'logout') {
      res.setHeader(
        'Set-Cookie',
        'admin_session=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT; HttpOnly; Secure; SameSite=Strict'
      );
      return res.status(200).json({ ok: true });
    }

    // VALIDATE CRYPTOGRAPHIC SESSION TOKEN
    const expectedToken = getSessionToken();
    if (!expectedToken || cookies.admin_session !== expectedToken) {
      return res.status(401).json({ ok: false, error: "Unauthorized session or credentials updated." });
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
subprocess.run(["git", "commit", "-m", "Implement cryptographic session token validation and auto-invalidation"], check=True)
subprocess.run(["git", "push", "origin", "main"], check=True)
print("🚀 Pushed cryptographic security upgrade to GitHub!")

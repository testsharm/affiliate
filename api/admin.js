export default function handler(req, res) {
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

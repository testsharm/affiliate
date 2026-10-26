export default function handler(req, res) {
  const envPassword = process.env.ADMIN_PASSWORD || process.env.PASSWORD;

  // Helper to parse cookies from request headers
  const cookies = {};
  const cookieHeader = req.headers.cookie;
  if (cookieHeader) {
    cookieHeader.split(';').forEach(cookie => {
      const parts = cookie.split('=');
      cookies[parts[0].trim()] = (parts[1] || '').trim();
    });
  }

  if (req.method === 'GET') {
    return res.status(200).json({ setup_required: false, configured: !!envPassword });
  }

  if (req.method === 'POST') {
    let body = req.body || {};
    if (typeof body === 'string') {
      try { body = JSON.parse(body); } catch(e) {}
    }

    const action = body.action;

    // 1. LOGIN ACTION
    if (action === 'login') {
      const submittedPass = body.password || body.pass || body.key || body.pw;

      if (!envPassword) {
        return res.status(401).json({ ok: false, error: "Server password not configured in Vercel environment variables." });
      }

      if (submittedPass === envPassword) {
        // Set secure HTTP-only session cookie valid for 1 day
        res.setHeader(
          'Set-Cookie',
          'admin_session=authenticated; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=86400'
        );
        return res.status(200).json({ ok: true, success: true, message: "Logged in successfully" });
      } else {
        return res.status(401).json({ ok: false, error: "Invalid password" });
      }
    }

    // 2. LOGOUT ACTION
    if (action === 'logout') {
      // Clear the session cookie
      res.setHeader(
        'Set-Cookie',
        'admin_session=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT; HttpOnly; Secure; SameSite=Lax'
      );
      return res.status(200).json({ ok: true });
    }

    // 3. PROTECTED ACTIONS (load, save, etc.) require valid session cookie
    if (cookies.admin_session !== 'authenticated') {
      return res.status(401).json({ ok: false, error: "Unauthorized session" });
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

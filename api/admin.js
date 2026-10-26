export default function handler(req, res) {
  const envPassword = process.env.ADMIN_PASSWORD || process.env.PASSWORD;
  const envPin = process.env.ADMIN_PIN || process.env.PIN;

  // Strict security headers
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-XSS-Protection', '1; mode=block');

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

    // LOGIN ACTION WITH 2FA PIN SUPPORT
    if (action === 'login') {
      const submittedPass = body.password || body.pass;
      const submittedPin = body.pin || body.key;

      if (!envPassword) {
        return res.status(401).json({ ok: false, error: "Server password not configured in Vercel." });
      }

      const passValid = submittedPass === envPassword;
      const pinValid = !envPin || submittedPin === envPin;

      if (passValid && pinValid) {
        // 30-minute strict session cookie (1800 seconds)
        res.setHeader(
          'Set-Cookie',
          'admin_session=authenticated; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=1800'
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

    // PROTECTED ACTIONS REQUIRE VALID SESSION COOKIE
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

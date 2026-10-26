export default async function handler(req, res) {
  const password = process.env.ADMIN_PASSWORD || process.env.PASSWORD || "PromptVault123!";

  if (req.method === 'GET') {
    return res.status(200).json({ setup_required: false, configured: true });
  }

  if (req.method === 'POST') {
    let body = req.body;

    // Robust stream reader for Vercel serverless functions
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

    // Support all possible frontend payload keys
    const submittedPass = body && (body.pass || body.password || body.key);

    if (submittedPass === password) {
      return res.status(200).json({ success: true, message: "Logged in successfully" });
    } else {
      return res.status(401).json({ success: false, message: "Invalid password" });
    }
  }

  return res.status(200).json({ success: true });
}

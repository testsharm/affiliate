export default function handler(req, res) {
  const password = process.env.ADMIN_PASSWORD || process.env.PASSWORD;
  
  if (!password) {
    return res.status(200).json({ setup_required: true, message: "Not set up yet. Add ADMIN_PASSWORD in Vercel." });
  }

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

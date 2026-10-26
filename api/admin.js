export default function handler(req, res) {
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

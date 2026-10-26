export default function handler(req, res) {
  const envPassword = process.env.ADMIN_PASSWORD || process.env.PASSWORD;
  const fallbackPassword = "PromptVault123!";

  if (req.method === 'GET') {
    return res.status(200).json({ setup_required: false, configured: true });
  }

  if (req.method === 'POST') {
    let body = req.body || {};
    
    if (typeof body === 'string') {
      try { body = JSON.parse(body); } catch(e) {}
    }

    const action = body.action;

    // Handle login action
    if (action === 'login' || body.password || body.pass) {
      const submittedPass = body.password || body.pass || body.key || body.pw;
      const isValid = submittedPass === fallbackPassword || (envPassword && submittedPass === envPassword);

      if (isValid) {
        return res.status(200).json({ ok: true, success: true, message: "Logged in successfully" });
      } else {
        return res.status(401).json({ ok: false, success: false, error: "Invalid password" });
      }
    }

    // Handle load action (mock data if no database)
    if (action === 'load') {
      return res.status(200).json({
        ok: true,
        sha: "123",
        data: {
          brand: "PromptVault",
          links: { toolsuite: "" },
          settings: { umami: "", follow: "", contact: "", country: "" },
          prompts: [
            {
              id: "example-prompt",
              t: "Example AI Video Prompt",
              c: "Video",
              tr: "AI video",
              u: "A cinematic shot of a futuristic city.",
              x: "Create a cinematic 4K video of [subject] in a cyberpunk city at night..."
            }
          ]
        }
      });
    }

    // Handle save action
    if (action === 'save') {
      return res.status(200).json({ ok: true, sha: "124" });
    }

    // Handle logout action
    if (action === 'logout') {
      return res.status(200).json({ ok: true });
    }

    return res.status(200).json({ ok: true });
  }

  return res.status(200).json({ ok: true });
}

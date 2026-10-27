// Public, read-only endpoint. Returns the latest prompts straight from GitHub (cached ~15 seconds at the edge),
// so a prompt saved in the admin shows on the site within seconds, without waiting for a redeploy.
module.exports = async (req, res) => {
  const fail = (c, m) => { res.setHeader('Cache-Control', 'no-store'); return res.status(c).json({ error: m }); };
  if (req.method !== 'GET' && req.method !== 'HEAD') return fail(405, 'Not allowed');
  const REPO = process.env.GITHUB_REPO, TOKEN = process.env.GITHUB_TOKEN, BRANCH = process.env.GITHUB_BRANCH || 'main';
  if (!REPO || !TOKEN) return fail(503, 'Not configured');
  try {
    const r = await fetch(`https://api.github.com/repos/${REPO}/contents/data.json?ref=${encodeURIComponent(BRANCH)}`, {
      headers: { Authorization: `Bearer ${TOKEN}`, Accept: 'application/vnd.github.raw+json', 'User-Agent': 'promptpad-data', 'X-GitHub-Api-Version': '2022-11-28' }
    });
    if (!r.ok) throw new Error('GitHub ' + r.status);
    const d = JSON.parse(await r.text()), s = d.settings || {};
    if (!Array.isArray(d.prompts)) throw new Error('bad data');
    res.setHeader('Cache-Control', 'public, max-age=0, s-maxage=15, stale-while-revalidate=5');
    return res.status(200).json({ brand: d.brand, links: d.links, settings: { umami: s.umami || '', follow: s.follow || '', contact: s.contact || '', country: s.country || '' }, prompts: d.prompts });
  } catch (e) { return fail(502, 'Unavailable'); }
};

// Private admin API. Runs on Vercel only when you use the admin page.
// Every action except "login" needs a valid session cookie, so visitors cannot change anything.
const crypto = require('crypto');

const REPO = process.env.GITHUB_REPO;          // e.g. yourname/promptpad
const BRANCH = process.env.GITHUB_BRANCH || 'main';
const TOKEN = process.env.GITHUB_TOKEN;        // only stored in Vercel, never in the code
const PASS = process.env.ADMIN_PASSWORD;
const SECRET = process.env.SESSION_SECRET;
const PIN = process.env.ADMIN_PIN || '';          // optional second password (digits or text)
const FILE = 'data.json';
const TRS = ['AI video', 'AI image', 'Chat AI'];
const fails = new Map();

const hash = v => crypto.createHash('sha256').update(String(v)).digest();
const same = (a, b) => crypto.timingSafeEqual(hash(a), hash(b));
// The signing key includes the password and PIN, so changing either one instantly logs out every old session.
const KEY = () => SECRET + '|' + hash(PASS + '|' + PIN).toString('hex');
const sign = v => crypto.createHmac('sha256', KEY()).update(String(v)).digest('hex');

const IDLE = 30 * 60e3;   // the session ends 30 minutes after your last action; every action renews it
function cookie() {
  const exp = Date.now() + IDLE;
  return `sid=${exp}.${sign(exp)}; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=${IDLE / 1000}`;
}
function authed(req) {
  const m = /(?:^|; )sid=([^;]+)/.exec(req.headers.cookie || '');
  if (!m) return false;
  const [exp, sig] = m[1].split('.');
  return !!(exp && sig && Number(exp) > Date.now() && same(sig, sign(exp)));
}

const str = (v, max, name, optional) => {
  if (optional && (v === undefined || v === '')) return '';
  if (typeof v !== 'string' || !v.trim() || v.length > max) throw new Error(name + ' is missing or too long');
  return v.trim();
};
function validate(d) {
  if (!d || typeof d !== 'object') throw new Error('No data');
  const link = str((d.links || {}).toolsuite, 600, 'Affiliate link');
  if (!/^https:\/\//.test(link)) throw new Error('The affiliate link must start with https://');
  const settings = d.settings || {};
  const umami = str(settings.umami, 60, 'Umami ID', true);
  if (umami && !/^[a-zA-Z0-9-]+$/.test(umami)) throw new Error('Umami ID looks wrong');
  const follow = str(settings.follow, 300, 'Follow link', true);
  if (follow && !/^https:\/\//.test(follow)) throw new Error('The follow link must start with https://');
  const contact = str(settings.contact, 120, 'Contact email', true);
  if (contact && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(contact)) throw new Error('Contact email looks wrong');
  const country = str(settings.country, 80, 'Country or state', true);
  const out = { brand: str(d.brand, 40, 'Brand name'), links: { toolsuite: link }, settings: { umami, follow, contact, country }, prompts: [] };
  if (!Array.isArray(d.prompts) || d.prompts.length > 500) throw new Error('Too many prompts (limit 500)');
  const seen = new Set();
  for (const p of d.prompts) {
    const id = str(p.id, 60, 'Link name');
    if (!/^[a-z0-9-]+$/.test(id)) throw new Error('Link name can only use a-z, 0-9 and dashes: ' + id);
    if (seen.has(id)) throw new Error('Two prompts share the link name: ' + id);
    seen.add(id);
    if (!TRS.includes(p.tr)) throw new Error('Pick a "Works in" value for ' + id);
    const item = { id, c: str(p.c, 30, 'Category'), t: str(p.t, 80, 'Title'), u: str(p.u, 140, 'Description'), tr: p.tr, x: str(p.x, 20000, 'Prompt text') };
    if (/^\d{4}-\d{2}-\d{2}$/.test(p.d || '')) item.d = p.d;
    out.prompts.push(item);
  }
  return out;
}

async function gh(method, body) {
  const url = `https://api.github.com/repos/${REPO}/contents/${FILE}` + (method === 'GET' ? `?ref=${encodeURIComponent(BRANCH)}` : '');
  const r = await fetch(url, {
    method,
    headers: { Authorization: `Bearer ${TOKEN}`, Accept: 'application/vnd.github+json', 'User-Agent': 'promptpad-admin', 'X-GitHub-Api-Version': '2022-11-28', 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined
  });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) { const e = new Error(j.message || 'GitHub ' + r.status); e.status = r.status; throw e; }
  return j;
}

module.exports = async (req, res) => {
  const send = (c, b) => { res.status(c).json(b); };
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  if (!PASS || !SECRET || !TOKEN || !REPO) return send(500, { error: 'Not set up yet. Add the settings in Vercel (see the setup guide).' });
  if (req.method !== 'POST') return send(405, { error: 'Not allowed' });
  const origin = req.headers.origin;
  try { if (origin && new URL(origin).host !== req.headers.host) return send(403, { error: 'Blocked' }); } catch (e) { return send(403, { error: 'Blocked' }); }
  if (req.headers['x-admin'] !== '1') return send(403, { error: 'Blocked' });

  let b = req.body;
  try { if (typeof b === 'string') b = JSON.parse(b || '{}'); } catch (e) { return send(400, { error: 'Bad request' }); }
  b = b || {};
  const ip = String(req.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'unknown';

  if (b.action === 'login') {
    const f = fails.get(ip) || { n: 0, t: 0 };
    if (f.n >= 5 && Date.now() - f.t < 15 * 60e3) return send(429, { error: 'Too many tries. Wait 15 minutes.' });
    if (typeof b.password === 'string' && same(b.password, PASS) && (!PIN || (typeof b.pin === 'string' && same(b.pin, PIN)))) {
      fails.delete(ip);
      res.setHeader('Set-Cookie', cookie());
      return send(200, { ok: true });
    }
    fails.set(ip, { n: f.n + 1, t: Date.now() });
    await new Promise(r => setTimeout(r, 700));
    return send(401, { error: PIN ? 'Wrong password or PIN' : 'Wrong password' });
  }
  if (b.action === 'logout') {
    res.setHeader('Set-Cookie', 'sid=; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=0');
    return send(200, { ok: true });
  }
  if (!authed(req)) return send(401, { error: 'Please log in' });
  res.setHeader('Set-Cookie', cookie());

  try {
    if (b.action === 'load') {
      const j = await gh('GET');
      return send(200, { data: JSON.parse(Buffer.from(j.content, 'base64').toString('utf8')), sha: j.sha });
    }
    if (b.action === 'save') {
      const clean = validate(b.data);
      if (typeof b.sha !== 'string' || !b.sha) return send(400, { error: 'Reload the page and try again' });
      const j = await gh('PUT', {
        message: 'Update prompts from admin', branch: BRANCH, sha: b.sha,
        content: Buffer.from(JSON.stringify(clean, null, 2) + '\n').toString('base64')
      });
      return send(200, { ok: true, sha: j.content && j.content.sha });
    }
    return send(400, { error: 'Unknown action' });
  } catch (e) {
    if (e.status === 409 || e.status === 422) return send(409, { error: 'The site data changed somewhere else. Reload this page and try again.' });
    if (e.status === 401 || e.status === 403) return send(502, { error: 'GitHub refused the token. Check GITHUB_TOKEN and its permission.' });
    if (e.status === 404) return send(502, { error: 'GitHub could not find the repo or data.json. Check GITHUB_REPO.' });
    return send(e.message && /too long|missing|must start|Link name|Two prompts|Pick a|Too many|looks wrong|No data|email/.test(e.message) ? 400 : 500, { error: e.message });
  }
};

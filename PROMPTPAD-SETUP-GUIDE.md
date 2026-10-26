# PromptPad: Setup and User Guide

**How to use this file:** Paste the whole file into any AI assistant (ChatGPT, Claude, Gemini, Copilot) and say:
"Guide me through this setup one step at a time. I am not a coder. Wait for me to say 'done' after each step."

---

## 0. Instructions for the AI helper reading this

- The user is a non-technical beginner who mostly uses a phone. Use simple words and short steps. Give **one step at a time** and wait for confirmation.
- Never ask the user to paste passwords, tokens or secret keys into the chat. They only go into Vercel's "Environment Variables" screen.
- If something fails, ask for a screenshot or the exact error text, then use Section 10 (Troubleshooting).
- Do not change the code unless the user asks. Everything the user needs to edit day to day is done in the Admin page.
- You are not a lawyer. Do not promise the legal pages protect the user from every claim.

## 1. What this project is

A free "prompt library" website that promotes one affiliate offer (ToolSuite on Whop). Visitors copy AI prompts; the offer is shown on every page with animated banners, a sliding tool showcase, a cost check, and clear "affiliate link" labels.

- Home page: `https://YOURSITE/` (search, categories, all prompts, 12 at a time with "Show more")
- One prompt page: `https://YOURSITE/#prompt-link-name` (that prompt first, then the offer on the same page, then more prompts). Works for any number of prompts (tested with 200).
- Product page: `https://YOURSITE/#toolsuite` (full breakdown of the offer)
- Legal pages: `/terms.html`, `/privacy.html`, `/disclosure.html`. Unknown addresses show `/404.html`.
- Admin page (owner only): `https://YOURSITE/admin/`

Prompt pages use `#` links. They load instantly and are unlimited, but Google does not index each one separately and link previews on social apps show the general site preview. This is fine for traffic coming from videos and posts.

## 2. Files in the project

```
promptpad/
  index.html        The website (all pages, animations and logic)
  data.json         All prompts and settings (the admin edits this file)
  terms.html        Terms and Conditions
  privacy.html      Privacy Policy
  disclosure.html   Affiliate Disclosure
  404.html          "Page not found" page (also promotes the offer)
  vercel.json       Security headers
  admin/index.html  The private admin page (login screen first)
  api/admin.js      Secure server code behind the admin page
```

**Upload the CONTENTS of the `promptpad` folder to GitHub, so `index.html` sits at the top level of the repository, not inside another folder.**

## 3. Important cost and rules to know BEFORE starting

1. **Vercel's free "Hobby" plan is for non-commercial personal use only.** Vercel's own fair-use guidelines say commercial use needs a paid Pro plan, and third-party guides say affiliate sites count as commercial. This site earns affiliate commissions, so plan to use **Vercel Pro (about $20 per month at the time of writing; check vercel.com/pricing)**, or ask an AI to move the project to another host. Using Hobby for an affiliate site could get the project suspended.
2. **Whop's affiliate terms** require a clear disclosure near each affiliate link and truthful presentation of the seller's product. The site already does this. Do not add claims such as "guaranteed income" or "#1" yourself. Read Whop's current affiliate terms yourself.
3. **Legal pages are templates**, not legal advice. Fill in the contact email and country in Admin, then have a lawyer review them if the site grows.
4. The cookie for referral credit is set by Whop. Visitors who click, leave, and buy within the seller's attribution window (about 30 days by Whop's default docs, but check) should be credited, if they use the same browser and device.

## 4. What the user needs before starting

- A laptop for the one-time setup (about 30 minutes). After that, everything can be done from a phone.
- A free GitHub account (github.com).
- A Vercel account (vercel.com, sign up with GitHub), with Pro plan for commercial use (see Section 3).
- The `promptpad.zip` file, unzipped on the laptop.
- Their ToolSuite affiliate link (looks like `https://whop.com/toolsuite?a=THEIRNAME`).

## 5. Step-by-step installation

### Step A. Create the GitHub repository
1. Go to github.com, sign in, click **+** (top right) then **New repository**.
2. Name it `promptpad`. Choose **Private**. Click **Create repository**.

### Step B. Upload the files
1. On the new empty repo page click **uploading an existing file** (or **Add file > Upload files**).
2. On the laptop, open the unzipped `promptpad` folder. Select **everything inside it** (the folders `admin` and `api` plus all the files) and drag it onto the GitHub page.
3. Wait for the upload, then click **Commit changes**.
4. Check: the repo's main page must list `admin`, `api`, `index.html`, `data.json`, `terms.html`, and so on. If you only see one folder called `promptpad`, the upload went one level too deep: delete it and re-upload the contents.

*(Alternative with GitHub Codespaces: open a Codespace, drag `promptpad.zip` into the file list, run `unzip promptpad.zip`, move the files to the top level, then `git add -A && git commit -m "Add site" && git push`.)*

### Step C. Create a GitHub access token (so the admin page can save changes)
1. On GitHub click your profile picture (top right) > **Settings**.
2. Left menu, bottom: **Developer settings** > **Personal access tokens** > **Fine-grained tokens** > **Generate new token**.
3. Token name: `promptpad-admin`. Expiration: choose a long period and write the date in a calendar (when it expires, saving stops until a new token is made).
4. **Repository access:** *Only select repositories* > choose `promptpad`.
5. **Permissions > Repository permissions > Contents:** set to **Read and write**. Leave everything else as it is.
6. Click **Generate token** and **copy it now** (it is shown once). Keep it somewhere private for the next step.

### Step D. Create the Vercel project
1. Go to vercel.com, sign in with GitHub.
2. Click **Add New > Project**, find `promptpad`, click **Import**.
3. **Framework Preset:** Other. Leave Build Command and Output Directory empty.
4. Open **Environment Variables** and add these five (name on the left, value on the right):

| Name | Value |
|---|---|
| `ADMIN_PASSWORD` | A long password only the user knows (12+ characters, not used anywhere else) |
| `SESSION_SECRET` | Any long random text, 40+ characters (mash the keyboard). Never share it |
| `GITHUB_TOKEN` | The token from Step C |
| `GITHUB_REPO` | `their-github-username/promptpad` |
| `GITHUB_BRANCH` | `main` |

5. Click **Deploy**. Wait about a minute. Vercel shows a link like `promptpad-xyz.vercel.app`.
6. If the variables were added after the first deploy, go to **Deployments > the latest one > ... > Redeploy**.

### Step E. Check that it works
1. Open the Vercel link. You should see the purple banner, the prompts, and the sliding tool cards.
2. Open `/admin/` on the same address (keep the final slash). You should see only a login box.
3. Log in with `ADMIN_PASSWORD`. You should see the prompts list.
4. Go to **Site settings** and fill in: Site name, ToolSuite affiliate link, **Contact email**, **Country or state** (these fill in the Terms and Privacy pages). Press **Save and publish**.
5. Wait one minute, refresh the site. Open `/terms.html`, `/privacy.html`, `/disclosure.html`. The red reminders should be gone.

### Step F. (Optional) Custom domain
Vercel project > **Settings > Domains** > add the domain and follow Vercel's instructions.

## 6. Daily use (works from a phone)

1. Open `https://YOURSITE/admin/` and log in.
2. **Add a prompt:** fill Title, Category, Works in, one-line description and the prompt text (long prompts are fine, up to 20,000 characters). Put blanks in square brackets, like `[city]`, and visitors can fill them in. A "link name" is made for you. Press **Add to my list**. New prompts go to the top and get a "New" tag for 14 days.
3. **Edit, move, delete:** use the buttons under each prompt.
4. **Copy link** on each prompt gives the link for one video or post. Use it in comments or DMs. Never change a prompt's link name later, or old links stop working.
5. Press **Save and publish** at the bottom. The site updates in about a minute.
6. **Which link to share:** the home link in a bio, a prompt link under a specific video, the product page link (`/#toolsuite`) when you want to focus on the offer.

## 7. Optional click statistics

1. Create a free account at umami.is (check their current free limits), add the site, copy the **Website ID**.
2. Admin > Site settings > **Umami website ID** > Save and publish.
3. Umami then shows page views, prompt copies, and clicks on the affiliate buttons. The Whop dashboard shows the sales. Do not add extra tracking tags to the Whop link unless Whop's documentation says it supports them.
4. If events do not appear, open the browser console and check for a blocked address; it may need adding to the `Content-Security-Policy` line near the top of `index.html`.

## 8. Changing or adding things later

- **Affiliate link / site name / contact / country:** Admin > Site settings.
- **Prompt categories:** type any new category in the Category box; filters update by themselves.
- **Works in:** `AI video`, `AI image`, `Chat AI` (this decides which tool names are suggested next to the copy button).
- **Another affiliate program later:** the offer's name, price and features are written directly in `index.html` (search for "ToolSuite"), and the affiliate link is `links.toolsuite` in `data.json`. To add a second offer, ask an AI to duplicate those sections with a new `links.<name>` entry, and update the admin API validation in `api/admin.js` to allow it.
- **Admin address:** to make it harder to find, rename the `admin` folder to something private, for example `manage-k39x`, then use that address. The admin page works from any folder name.

## 9. Security notes

- Anyone can open `/admin/` and see a login box, but **no action works without the password**. The server checks a signed login cookie (12 hours), blocks requests from other websites, locks a visitor out for 15 minutes after 5 wrong passwords, and checks and cleans everything before saving.
- The GitHub token and password live only in Vercel's environment variables, never in the code or in the browser.
- Use a long, unique password. Log out on shared devices. If the password or token may have leaked: change `ADMIN_PASSWORD` and `SESSION_SECRET` in Vercel (this logs everyone out), delete the token on GitHub and make a new one, then redeploy.
- Keep the GitHub repository **private** and turn on two-factor login on GitHub and Vercel.

## 10. Troubleshooting

| Problem | What to do |
|---|---|
| Site shows "Could not load the prompts" | `data.json` is missing or broken at the repo top level. Check the repo files and the latest commit. |
| Admin says "Not set up yet" | One of the five environment variables is missing. Add it in Vercel > Settings > Environment Variables, then Redeploy. |
| Login says "Wrong password" | Check `ADMIN_PASSWORD` in Vercel (no spaces). After 5 failures wait 15 minutes. |
| "GitHub refused the token" | Token expired, or it lacks **Contents: Read and write**, or it is not for this repo. Make a new token and update `GITHUB_TOKEN`, then Redeploy. |
| "GitHub could not find the repo" | `GITHUB_REPO` must be `username/promptpad` exactly. |
| "The site data changed somewhere else" | Reload the admin page and make the change again. |
| Saved but the site did not change | Wait 1-2 minutes, then hard refresh. Check Vercel > Deployments for a failed build. |
| `/admin/` shows "404" | The files were uploaded inside an extra folder. Fix the repo structure (Step B.4). |
| Terms page shows red text | Fill in contact email and country in Admin > Site settings. |
| Vercel warns about commercial use | See Section 3, point 1. |

## 11. Reference for AI helpers

**`data.json` format**
```json
{
  "brand": "PromptPad",
  "links": { "toolsuite": "https://whop.com/toolsuite?a=NAME" },
  "settings": { "umami": "", "follow": "", "contact": "", "country": "" },
  "prompts": [
    { "id": "link-name", "d": "2026-10-26", "c": "Video", "t": "Title", "u": "One-line description",
      "tr": "AI video", "x": "The prompt text with [blanks]" }
  ]
}
```
Rules: `id` uses a-z, 0-9 and dashes, unique; `tr` is one of `AI video`, `AI image`, `Chat AI`; `d` is optional `YYYY-MM-DD`; the order in the array is the display order; up to 500 prompts; `x` up to 20,000 characters; links must start with `https://`.

**`/api/admin` (POST only, JSON, header `X-Admin: 1`)**: actions `login` {password}, `logout`, `load` (returns data and the file's sha), `save` {data, sha}. `save` validates the data and commits `data.json` to GitHub through the contents API using `GITHUB_TOKEN`; Vercel then redeploys automatically.

**Environment variables:** `ADMIN_PASSWORD`, `SESSION_SECRET`, `GITHUB_TOKEN`, `GITHUB_REPO`, `GITHUB_BRANCH` (default `main`).

**Features implemented:** purple promo banner on every page; hero card; sliding premium tool cards in alternating directions (auto-scroll, manual swipe or drag, pauses on touch and hover, links to the affiliate page); feature slider; cost check calculator; promo box under every copy button that updates after copying; prev/next prompt links; "Show more" paging; reveal-on-scroll and page-change animations; mobile bottom bar; end-of-page offer section; legal pages with the offer on each; reduced-motion support.

## 12. Honest limits

- Nobody can force a visitor to click. The design makes the offer clear and easy to reach, and keeps every prompt free.
- Figures about ToolSuite (price, ratings, tool names, claims) are copied from the seller's own listing at build time and can change. Re-check the listing now and then and update the text in `index.html` if it changes.
- The legal pages are good-faith templates, not legal advice.

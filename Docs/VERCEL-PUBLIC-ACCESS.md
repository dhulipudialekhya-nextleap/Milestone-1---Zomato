# Make your live site public (no Vercel login)

If visitors see **“Authentication Required”** or a **Vercel login** page, **Deployment Protection** is on. Turn it off in the Vercel dashboard (this cannot be fixed from `vercel.json` alone).

## Steps (about 2 minutes)

1. Open [vercel.com/dashboard](https://vercel.com/dashboard)
2. Open project **Milestone-1---Zomato** (or your DineAI project name)
3. Go to **Settings** → **Deployment Protection**
4. Under **Vercel Authentication**:
   - Set to **Off** / **Disabled**, **or**
   - If your team forces protection: set protection to **Only Preview Deployments** (not Production)
5. Click **Save**
6. Go to **Settings** → **Domains** and note your **Production** domain (e.g. `milestone-1-zomato.vercel.app`)
7. **Deployments** → latest **Production** → **Redeploy** (optional, after changing settings)

## Link to share

Share the **Production** domain from **Domains**, not a long preview URL like:

`https://milestone-1-zomato-xxxxx-username.vercel.app`

Preview/deployment URLs are often protected even when production is public.

**Good:** `https://your-project.vercel.app`  
**Often protected:** `https://your-project-abc123-team.vercel.app`

## Verify (incognito / phone, not logged into Vercel)

- Home page loads without login
- `/api/health` returns JSON

## Team / Hobby plan notes

- **Hobby:** You can disable Vercel Authentication on your own projects.
- **Team/Pro:** An admin may need to change **Team Settings → Deployment Protection** or allow public production for your project.

## Still blocked?

Use **Deployment Protection → Shareable Links** (temporary public link for one deployment) or ask your team admin to disable **Standard Protection** for production.

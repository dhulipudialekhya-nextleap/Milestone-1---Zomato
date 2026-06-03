# Final deploy: live website (Railway + Vercel)

One guide to get the **public website** working end-to-end.

| Part | Platform | URL |
|------|----------|-----|
| Backend API | Railway (already running) | `https://YOUR-APP.up.railway.app` |
| Frontend UI | Vercel | `https://YOUR-APP.vercel.app` |

---

## Part A — Railway (skip if already working)

1. Open `https://YOUR-RAILWAY-URL.up.railway.app/health` → JSON `{"status":"ok"}`
2. Keep Railway running; no changes needed.

---

## Part B — Vercel project settings (exact values)

### 1. Import or open project

- Dashboard → **Add New** → **Project** → **Milestone-1---Zomato**
- Or open your existing project

### 2. General

| Setting | Value |
|---------|--------|
| **Root Directory** | `frontend` |
| **Node.js Version** | 20.x |

> **No** repo-root `vercel.json` in this project — do not add a second root directory anywhere.

### 3. Build and Deployment

| Setting | Value |
|---------|--------|
| **Framework Preset** | Next.js |
| **Build Command** | *(empty)* |
| **Output Directory** | *(empty)* |
| **Install Command** | *(empty)* |

### 4. Environment Variables

Add for **Production** (and Preview if you want):

| Key | Value | Example |
|-----|--------|---------|
| `NEXT_PUBLIC_API_URL` | Your Railway HTTPS URL, **no trailing /** | `https://zomato-api.up.railway.app` |
| `NEXT_PUBLIC_USE_MOCK` | `true` | `true` |

### 5. Deploy

1. **Deployments** → **Redeploy**
2. Uncheck **Use existing Build Cache**
3. Wait for **Ready**

### 6. Verify build log

Must include:

```
Route (app)
┌ ○ /
├ ○ /api/health
├ ○ /login
└ ○ /signup
```

If you see **Python** or **pip** → Root Directory is wrong (must be `frontend`).

---

## Part C — Your final website URLs

After deploy:

1. Click **Visit** on the Vercel project  
2. **Homepage:** `https://YOUR-PROJECT.vercel.app/`  
3. **Health check:** `https://YOUR-PROJECT.vercel.app/api/health` → `{"status":"ok",...}`

### Use the app

1. Open the **Vercel** URL (not Railway)
2. Location: e.g. **Koramangala**
3. Budget: **medium**
4. Cuisine: **Italian**
5. Min rating: **4.0**
6. Submit → see **restaurant recommendations**

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| 404 on homepage | Root Directory = `frontend`; Output Directory empty; redeploy |
| “Additional root directory” | Set Root Directory **only** in Vercel UI (not in `vercel.json`) |
| “Folder already exists” | New project name e.g. `zomato-dineai` |
| Amber banner on site | Add `NEXT_PUBLIC_API_URL` on Vercel, redeploy |
| Failed to fetch | Railway URL in `NEXT_PUBLIC_API_URL`; Railway `/health` works |
| Wrong page (JSON) | You opened Railway — use Vercel URL for UI |

---

## Checklist

```
☐ Railway /health OK
☐ Vercel Root Directory = frontend
☐ Vercel Output Directory = empty
☐ NEXT_PUBLIC_API_URL = Railway URL
☐ NEXT_PUBLIC_USE_MOCK = true
☐ Redeploy → Ready
☐ /api/health OK on Vercel
☐ / shows DineAI form
☐ Submit → recommendations
```

Your **final output website** is the Vercel **Visit** link.

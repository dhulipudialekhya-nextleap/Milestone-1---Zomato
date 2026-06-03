# Final deploy: live website (Railway + Vercel)

## Vercel settings (copy exactly)

| Setting | Value |
|---------|--------|
| **Root Directory** | `frontend` |
| **Node.js Version** | `20.x` |
| **Framework** | Next.js |
| **Build Command** | *(empty — uses `frontend/vercel.json`)* |
| **Install Command** | *(empty)* |
| **Output Directory** | *(empty)* |

## Environment variables

| Key | Value |
|-----|--------|
| `NEXT_PUBLIC_API_URL` | `https://YOUR-RAILWAY-URL.up.railway.app` |
| `NEXT_PUBLIC_USE_MOCK` | `true` |

## Redeploy

Deployments → Redeploy → disable build cache → Ready.

## Verify

- `https://YOUR-APP.vercel.app/api/health` → JSON ok
- `https://YOUR-APP.vercel.app/` → DineAI form

## Errors

| Error | Fix |
|-------|-----|
| No Next.js detected | Root Directory = `frontend` |
| npm run build exited 1 | Root Directory = `frontend`; redeploy latest `main` |
| Couldn't find app directory | Root Directory = `frontend` |
| Invalid rootDirectory | Never in `vercel.json` at repo root |

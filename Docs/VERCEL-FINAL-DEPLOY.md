# Final deploy: live website (Railway + Vercel)

The Next.js app is at the **repository root** (`app/`, `components/`, `lib/`).  
Python backend stays in `src/` (Railway only).

## Vercel settings

| Setting | Value |
|---------|--------|
| **Root Directory** | *(empty — repo root)* |
| **Node.js** | `20.x` |
| **Framework** | Next.js |
| **Build / Install / Output** | *(all empty)* |

## Environment variables

| Key | Value |
|-----|--------|
| `BACKEND_API_URL` | `https://YOUR-RAILWAY-URL.up.railway.app` |
| `NEXT_PUBLIC_API_URL` | Same Railway URL (for build-time checks) |
| `NEXT_PUBLIC_USE_MOCK` | `true` |

Do **not** use your Vercel URL as the API URL — that causes **404** on recommendations.

## Redeploy

Deployments → Redeploy (cache off) → **Ready**.

## Verify

- `https://YOUR-APP.vercel.app/api/health`
- `https://YOUR-APP.vercel.app/` → DineAI form

## Errors

| Error | Fix |
|-------|-----|
| Couldn't find `app` directory | Pull latest `main`; Root Directory must be **empty** |
| No Next.js detected | `package.json` at repo root must include `next` |

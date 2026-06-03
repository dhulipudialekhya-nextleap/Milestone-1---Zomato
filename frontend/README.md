# DineAI Frontend (Next.js)

Deployed on **Vercel**. Talks to the FastAPI backend on **Railway**.

## Local dev

```bash
npm install
copy .env.example .env.local
npm run dev
```

Set `NEXT_PUBLIC_API_URL=http://localhost:8000` and run the backend from the repo root.

## Vercel deploy

| Setting | Value |
|---------|--------|
| Root Directory | **`frontend`** (required — `next` is in `frontend/package.json` only) |
| Framework | Next.js |

**Environment variables:**

| Key | Value |
|-----|--------|
| `NEXT_PUBLIC_API_URL` | `https://YOUR-SERVICE.up.railway.app` |
| `NEXT_PUBLIC_USE_MOCK` | `true` (recommended for demo) |

Full guide: [Docs/deployment-railway-vercel.md](../Docs/deployment-railway-vercel.md)

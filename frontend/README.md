# DineAI Frontend (Next.js)

Deployed on **Vercel**. Talks to the FastAPI backend on **Render**.

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

If Vercel says **No Next.js version detected**, Root Directory is wrong (must be `frontend`, not repo root).

**Environment variables:**

| Key | Value |
|-----|--------|
| `NEXT_PUBLIC_API_URL` | `https://YOUR-RENDER-SERVICE.onrender.com` |
| `NEXT_PUBLIC_USE_MOCK` | `true` (recommended for demo) |

Full guide: [Docs/deployment-render-vercel.md](../Docs/deployment-render-vercel.md)

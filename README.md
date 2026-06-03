# Zomato AI Restaurant Recommendation System

AI-powered restaurant recommendations combining structured Zomato data with LLM reasoning.

## Current status

- Phase 0: project foundation and shared pipeline
- Phase 1: dataset ingestion, preprocessing, and processed-store loading
- Phase 2: centralized input validation service in separate folder
- Phase 3: candidate selection engine in separate folder
- Phase 4: Groq-backed LLM layer in separate folder
- Phase 5: presentation view model + renderer in separate folder
- Phase 6: backend service boundary + contracts in separate folder
- Phase 7: Next.js frontend in `frontend/` consuming backend API
- Phase 8: Frontend-backend API contract (`GET /api/contract`, shared fixtures, regression tests)
- Phase 9: Production deploy — **Vercel** (frontend) + **Railway** (backend) — see [Docs/deployment-railway-vercel.md](Docs/deployment-railway-vercel.md)

### Project structure

```
frontend/                  # Phase 7 — Next.js App Router UI
src/
├── phases/                # Phase-wise namespace (phase0 ... phase7)
├── config.py              # Environment config & validation
├── app.py                 # Pipeline orchestrator
├── models/                # Restaurant, UserPreferences, RecommendationResult
├── input/
│   └── phase2/            # Input defaults + validation service
├── data/
│   ├── loader.py          # Loads processed data (or falls back)
│   └── phase1/            # Ingestion + normalization + persistence
├── filters/
│   └── phase3/            # Filter engine + ranking + payload serializer
├── llm/
│   └── phase4/            # Groq client + prompt + parser + fallback
├── backend/
│   ├── phase6/            # Backend contracts + service + FastAPI server
│   └── phase8/            # API contract manifest, validation, schema export
└── presentation/
    ├── phase5/            # View model + renderer
    ├── web_ui.py          # Legacy Streamlit UI (optional, not deployed)
    └── renderer.py        # Compatibility wrapper to phase5

tests/
├── phase0/                # Foundation + pipeline smoke tests
├── phase1/                # Ingestion / normalization tests
├── phase2/                # Input validation tests
├── phase3/                # Candidate selection tests
├── phase4/                # LLM parsing / fallback tests
├── phase5/                # Presentation view-model / renderer tests
├── phase6/                # Backend boundary tests
├── phase7/                # FastAPI server tests for Next.js frontend
└── phase8/                # Contract compatibility tests

contracts/v1/              # Exported schemas + shared JSON fixtures (Phase 8)
```

### Setup

```bash
cd "MILESTONE 1 - ZOMATO"
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements-dev.txt
copy .env.example .env          # optional; defaults work for Phase 0
```

### Run Phase 1 ingestion (separate folder module)

```bash
python -m src.data.phase1.run_ingestion
```

### Run the Next.js frontend (Phase 7 — primary UI)

**Terminal 1 — backend API:**

```bash
python -m src.backend.phase6.run_server
```

**Terminal 2 — frontend:**

```bash
cd frontend
copy .env.example .env.local
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000), enter preferences, and click **Get recommendations**.

### Deploy (production)

See **[Docs/deployment-railway-vercel.md](Docs/deployment-railway-vercel.md)** — Railway for FastAPI, Vercel for Next.js.  
Railway variables template: [`railway.env.example`](railway.env.example)

### Run via CLI (dev / testing only)

```bash
python -m src --mock-data
python -m src --location Bangalore --budget medium --cuisine Italian --min-rating 4.0
```

### Run tests

```bash
pytest
```

### Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `PROCESSED_DATA_PATH` | `data/processed/restaurants.csv` | Processed dataset (Phase 1) |
| `LLM_PROVIDER` | `mock` | `mock`, `groq`, `openai`, `gemini`, `ollama` |
| `LLM_API_KEY` | — | Required when provider is not `mock` |
| `SHORTLIST_SIZE` | `15` | Max candidates sent to LLM |
| `DISPLAY_TOP_K` | `5` | Results shown in UI |
| `CORS_ORIGINS` | `http://localhost:3000,...` | Allowed origins for backend API |

Frontend env (`frontend/.env.local`):

| Variable | Default | Description |
|----------|---------|-------------|
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | Phase 6 FastAPI backend URL |

See [.env.example](.env.example) for all options.

### Phase 8 API contract

- Document: [Docs/phase8-api-contract.md](Docs/phase8-api-contract.md)
- Live manifest: `GET http://localhost:8000/api/contract` (with backend running)
- Export JSON schemas: `python -m src.backend.phase8.export`
- Tests: `pytest tests/phase8 -q` and `cd frontend && npm run test -- src/lib/contract.test.ts`

### Documentation

- [Problem statement](Docs/problemstatement.md)
- [Architecture](Docs/architecture.md)
- [Deploy: Railway + Vercel](Docs/deployment-railway-vercel.md)
- [Phase 8 API contract](Docs/phase8-api-contract.md)
- [Edge cases](Docs/edge-cases.md)

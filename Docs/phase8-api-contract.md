# Phase 8 — Frontend-Backend API Contract

**Version:** `1.0.0`  
**Status:** Implemented  
**Canonical sources:** `src/backend/phase8/`, `frontend/src/lib/contract.ts`, `contracts/v1/`

---

## Overview

The Next.js frontend and FastAPI backend communicate through a **stable JSON contract**. Business logic may change behind this boundary; the request and response shapes must remain compatible unless the contract version is bumped.

| Artifact | Location |
|----------|----------|
| Backend manifest + schemas | `GET /api/contract` |
| Python models / validation | `src/backend/phase8/` |
| TypeScript types + runtime guards | `frontend/src/lib/contract.ts` |
| Shared fixtures (regression tests) | `contracts/v1/fixtures/` |
| Exported JSON Schema | `contracts/v1/*.schema.json` (run `python -m src.backend.phase8.export`) |

---

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Liveness: `{ "status": "ok" }` |
| `GET` | `/api/contract` | Phase 8 manifest (version, JSON Schemas, endpoint map) |
| `POST` | `/api/recommendations` | Run recommendation pipeline |

### HTTP semantics

- **Validation and runtime business errors** return **HTTP 200** with `{ "ok": false, ... }`.
- **Transport errors** (network, 5xx, non-JSON) are handled by the frontend `ApiError` class.
- The frontend **always** parses the body with `parseBackendResponse()` before using results.

---

## Request contract

`Content-Type: application/json`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `location` | string | yes | Bangalore area (e.g. `Koramangala`) |
| `budget` | `"low"` \| `"medium"` \| `"high"` | yes | Normalized band (frontend maps UI ranges) |
| `cuisine` | string | yes | Preferred cuisine (`Any Cuisine` → `Indian` on client) |
| `min_rating` | number | no | 0–5, default `0` |
| `extras` | string \| null | no | Free-text cravings / filters |
| `use_mock_data` | boolean | no | Dev toggle; default `false` |

### Example

```json
{
  "location": "Koramangala",
  "budget": "medium",
  "cuisine": "Italian",
  "min_rating": 4.0,
  "extras": null,
  "use_mock_data": true
}
```

---

## Response contract

Discriminated union on `ok`.

### Success (`ok: true`)

```json
{
  "ok": true,
  "result": {
    "summary": "string | null",
    "recommendations": [
      {
        "rank": 1,
        "restaurant_id": "string",
        "name": "string",
        "explanation": "string",
        "cuisines": ["string"],
        "rating": 4.5,
        "average_cost": 800,
        "cost_band": "medium"
      }
    ],
    "used_llm_fallback": false,
    "filter_match_count": 12
  }
}
```

### Error (`ok: false`)

```json
{
  "ok": false,
  "error_code": "validation_error",
  "message": "Human-readable error message."
}
```

| `error_code` | When |
|--------------|------|
| `validation_error` | Invalid or missing preferences |
| `config_error` | Missing API key / misconfiguration |
| `runtime_error` | Unexpected pipeline failure |

LLM failures use **`ok: true`** with `used_llm_fallback: true` inside `result` (schema preserved).

---

## Frontend responsibilities

1. Validate the form with `validatePreferenceForm()` before submit.
2. Build the API body with `buildApiRequestBody()`.
3. Parse responses with `parseBackendResponse()`.
4. Render via Phase 5 view model only (`buildPhase5ViewModel()`).

---

## Backend responsibilities

1. Accept only `ApiRecommendationsRequest` at the HTTP layer.
2. Return `BackendResponse` from `run_backend_request()` for all business outcomes.
3. Never expose secrets in `message` fields.

---

## Regression tests

```bash
pytest tests/phase8 -q
cd frontend && npm run test -- src/lib/contract.test.ts
```

---

## Versioning

Bump `CONTRACT_VERSION` in both:

- `src/backend/phase8/manifest.py`
- `frontend/src/lib/contract.ts`

…when making **breaking** changes. Re-export schemas and update fixtures under `contracts/v1/`.

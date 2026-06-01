"""Export Phase 8 contract artifacts to contracts/v1/ (for docs and regression tests)."""

from __future__ import annotations

import json
from pathlib import Path

from src.backend.phase8.manifest import CONTRACT_VERSION, build_contract_manifest

_REPO_ROOT = Path(__file__).resolve().parents[3]
_CONTRACT_DIR = _REPO_ROOT / "contracts" / "v1"
_FIXTURES_DIR = _CONTRACT_DIR / "fixtures"


def export_contract_artifacts() -> Path:
    """Write manifest and fixture templates under contracts/v1/."""
    _CONTRACT_DIR.mkdir(parents=True, exist_ok=True)
    _FIXTURES_DIR.mkdir(parents=True, exist_ok=True)

    manifest = build_contract_manifest()
    manifest_path = _CONTRACT_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    request_schema_path = _CONTRACT_DIR / "request.schema.json"
    request_schema_path.write_text(
        json.dumps(manifest["request"]["schema"], indent=2) + "\n",
        encoding="utf-8",
    )

    response_schema_path = _CONTRACT_DIR / "response.schema.json"
    response_schema_path.write_text(
        json.dumps(manifest["response"]["schema"], indent=2) + "\n",
        encoding="utf-8",
    )

    version_path = _CONTRACT_DIR / "VERSION"
    version_path.write_text(CONTRACT_VERSION + "\n", encoding="utf-8")

    return _CONTRACT_DIR


def main() -> None:
    path = export_contract_artifacts()
    print(f"Exported Phase 8 contract to {path}")


if __name__ == "__main__":
    main()

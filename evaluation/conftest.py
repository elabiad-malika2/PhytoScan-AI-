import sys
from pathlib import Path


# Ensure backend package imports work when pytest rootdir is `evaluation/`.
# - In Docker, backend is mounted at `/app` and the package is `/app/app`.
# - Locally, backend package lives under `<repo>/backend/app`.
repo_root = Path(__file__).resolve().parents[1]
backend_root = repo_root / "backend"

sys.path.insert(0, str(repo_root))
sys.path.insert(0, str(backend_root))


<!-- Copilot instructions for AI coding agents - Song Recommendation System -->

# Overview

This repo is a small FastAPI-based song recommendation prototype that uses TF-IDF + cosine similarity over song text/data. Key artifacts:
- `main.py` — imports show `FastAPI`, `pydantic`, `TfidfVectorizer`, `cosine_similarity` (start here for API routes and recommendation logic).
- `requirements.txt` — lists runtime deps (fastapi, uvicorn, scikit-learn, pandas).
- `spotify_millsongdata (1).csv` — primary dataset (note the filename contains spaces/parentheses).

# Big picture
- API server: FastAPI app exposing endpoints (expected entry `app = FastAPI()` in `main.py`).
- Data pipeline: dataset is loaded (pandas) → text features built with `TfidfVectorizer` → similarity via `cosine_similarity` → results returned by API.
- No separate services or DB present — data is file-backed in the repo.

# How to run (discovered steps)
1. Create and activate a Python venv (Windows):
```powershell
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
```
2. Start the app (ensure `app = FastAPI()` exists in `main.py`):
```powershell
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
If `main.py` does not define `app`, search for other modules that create it before running.

# Project-specific conventions & notes
- Dataset filename: `spotify_millsongdata (1).csv` — be cautious when referencing on code/Windows paths; prefer renaming to a safe filename or use `pathlib.Path("spotify_millsongdata (1).csv")`.
- Minimal single-file prototype: most logic will live in `main.py`. When expanding, prefer module separation (e.g., `api/`, `models/`, `data/`).
- Vectorization pattern: TF-IDF transformer is used at runtime; cache the vectorizer/matrix if endpoints will be called frequently to avoid recomputing on each request.

# Integration points & external deps
- scikit-learn: `TfidfVectorizer`, `cosine_similarity` — used for feature extraction and similarity.
- pandas: for CSV loading and simple ETL.
- FastAPI + uvicorn: web framework and ASGI server.
- No external APIs or databases were found in the repo.

# Guidance for editing and adding features (actionable)
- When adding API endpoints, register them on the global `app` instance in `main.py` or in submodules and `include_router` from a startup file.
- Load the dataset once at startup (module-import time or `@app.on_event("startup")`) and keep precomputed TF-IDF matrix in memory.
- For file paths, use `Path(__file__).resolve().parent` to build repo-relative paths (avoids issues with current working dir).
- Keep dependency changes in `requirements.txt` and pin versions when adding new packages.

# What I couldn't discover (ask the repo owner)
- Intended public endpoints and expected request/response shapes (no route definitions found in the scanned `main.py`).
- Any preferred dataset filename change or .gitignore rules for `venv/`.

If any of these details are incorrect or you want deeper guidance (routing conventions, example endpoints, or a module split), tell me which area to expand.

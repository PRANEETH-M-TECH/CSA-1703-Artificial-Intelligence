import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.database import Base, engine, SessionLocal
from app.routers import auth, tasks, schedule, conflicts, learning
from app.seed import seed_demo_user

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TaskMind API",
    description="Intelligent multi-agent task scheduling: CSP/A* search, forward/backward-chaining "
                "conflict resolution, and decision-tree personalization.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(schedule.router)
app.include_router(conflicts.router)
app.include_router(learning.router)


@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    try:
        seed_demo_user(db)
    finally:
        db.close()


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "TaskMind API"}


# ---------------------------------------------------------------------------
# Single-process production serving: if the frontend has been built
# (`npm run build`, producing frontend/dist), serve it directly from this
# same FastAPI process so the whole app — API + UI — runs as one process on
# one port with one command (`npm run prod` / `npm start` at the repo root).
# In dev mode `frontend/dist` won't exist yet, so this block is skipped and
# the Vite dev server (port 5173) is used instead, as documented in the README.
# ---------------------------------------------------------------------------
_FRONTEND_DIST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "frontend", "dist")
_FRONTEND_DIST = os.path.normpath(_FRONTEND_DIST)

if os.path.isdir(_FRONTEND_DIST):
    app.mount("/assets", StaticFiles(directory=os.path.join(_FRONTEND_DIST, "assets")), name="assets")

    @app.get("/{full_path:path}")
    def serve_spa(full_path: str):
        candidate = os.path.join(_FRONTEND_DIST, full_path)
        if full_path and os.path.isfile(candidate):
            return FileResponse(candidate)
        return FileResponse(os.path.join(_FRONTEND_DIST, "index.html"))

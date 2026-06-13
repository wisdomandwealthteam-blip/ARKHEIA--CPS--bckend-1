"""
ARKHEIA-CPS — FastAPI Application Entry Point
ARKHEIA Contract Protection System
FIA → OIA-PEM → RTCSA pipeline for AUTO and HOUSING contracts
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.db import create_all_tables
from app.routers import contracts, analysis

settings = get_settings()

app = FastAPI(
    title="ARKHEIA Contract Protection System (CPS)",
    description=(
        "Discipline-based real-time contract safety analysis. "
        "FIA (Identity) → OIA-PEM (Pattern) → RTCSA (Safety). "
        "Verticals: AUTO (with Perfection Law) + HOUSING."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS — allow Webflow and any future frontends ─────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Tighten to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────
app.include_router(contracts.router)
app.include_router(analysis.router)


# ── Startup ───────────────────────────────────────────────────
@app.on_event("startup")
def on_startup():
    if settings.ENV == "dev":
        create_all_tables()


# ── Health ────────────────────────────────────────────────────
@app.get("/health", tags=["System"])
def health():
    return {
        "status": "ok",
        "system": settings.APP_NAME,
        "version": settings.VERSION,
        "env": settings.ENV,
    }


@app.get("/", tags=["System"])
def root():
    return {
        "system": "ARKHEIA Contract Protection System",
        "version": "1.0.0",
        "endpoints": {
            "submit_auto":     "POST /contracts/auto",
            "submit_housing":  "POST /contracts/housing",
            "get_analysis":    "GET /analysis/{contract_id}",
            "list_analyses":   "GET /analysis",
            "stats":           "GET /analysis/summary/stats",
            "docs":            "GET /docs",
        },
    }

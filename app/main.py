from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.webhook import router as webhook_router

app = FastAPI(
    title="Formafzar → Hesabfa Integration",
    version="1.0.0",
    description="Webhook service to sync Formafzar contacts and invoices into Hesabfa",
)

# ─────────────────────────────────────────────
# CORS (adjust if needed)
# ─────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
# Routers
# ─────────────────────────────────────────────
app.include_router(webhook_router)


# ─────────────────────────────────────────────
# Health check
# ─────────────────────────────────────────────
@app.get("/health")
async def health():
    return {"status": "ok"}

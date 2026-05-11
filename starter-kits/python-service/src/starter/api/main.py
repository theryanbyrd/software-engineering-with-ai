"""FastAPI application entry point."""

from __future__ import annotations

from fastapi import FastAPI

from starter.api.orders import router as orders_router

app = FastAPI(
    title="Starter Service",
    description="Companion to Software Engineering with AI by Ryan Byrd.",
    version="0.1.0",
)

app.include_router(orders_router)


@app.get("/health")
async def health() -> dict[str, str]:
    """Liveness check."""
    return {"status": "ok"}

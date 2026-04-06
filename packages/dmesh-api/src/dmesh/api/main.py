import os
from fastapi import FastAPI
from mangum import Mangum
from dmesh.api.routers import dps, dcs

def create_app() -> FastAPI:
    app = FastAPI(title="DMesh API")
    
    _BASE = os.environ.get("WS_BASE_PATH", "dmesh").strip("/") or "dmesh"
    
    app.include_router(dps.router, prefix=f"/{_BASE}")
    app.include_router(dcs.router, prefix=f"/{_BASE}")
    
    @app.get(f"/{_BASE}/health")
    async def health():
        return {"status": "ok", "driver": "psycopg3"}
        
    return app

app = create_app()
handler = Mangum(app)

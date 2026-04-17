import os
import sys
import asyncio

# On Windows, psycopg3 requires SelectorEventLoop for async operations.
# This must be set before any event loop is created.
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from contextlib import asynccontextmanager
from fastapi import FastAPI
from mangum import Mangum
from dmesh.api.routers import dps, dcs
from dmesh.api.dependencies import get_factory

@asynccontextmanager
async def lifespan(app: FastAPI):
    # On Windows, verify event loop compatibility with psycopg
    if sys.platform == 'win32':
        loop = asyncio.get_running_loop()
        if type(loop).__name__ == 'ProactorEventLoop':
            # This is a critical warning for Windows users
            import logging
            logging.warning("Using ProactorEventLoop on Windows. Psycopg3 may fail. Run uvicorn with '--loop selector'.")

    factory = get_factory()
    if hasattr(factory, 'open'):
        await factory.open()
        
    yield
    
    # Shutdown: Close the repository factory
    if factory and hasattr(factory, 'close'):
        await factory.close()

def create_app() -> FastAPI:
    app = FastAPI(title="DMesh API", lifespan=lifespan)
    
    _BASE = os.environ.get("WS_BASE_PATH", "dmesh").strip("/") or "dmesh"
    
    app.include_router(dps.router, prefix=f"/{_BASE}")
    app.include_router(dcs.router, prefix=f"/{_BASE}")
    
    @app.get(f"/{_BASE}/health")
    async def health():
        factory = get_factory()
        db_status = "unknown"
        if hasattr(factory, 'is_open'):
            db_status = "connected" if factory.is_open else "disconnected"
        elif hasattr(factory, '_dp_repo'):
             db_status = "connected" # For InMemory, it's always "connected"
             
        return {
            "status": "ok", 
            "driver": "psycopg3", 
            "db": db_status,
            "platform": sys.platform
        }
        
    return app

app = create_app()
handler = Mangum(app)

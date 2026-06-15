import os
import sys
import asyncio

# On Windows, psycopg3 requires SelectorEventLoop for async operations.
# This must be set before any event loop is created.
if sys.platform == 'win32':
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from dmesh.api.routers import dps, dcs
from dmesh.api.routers.discover import discover_router
from dmesh.api.dependencies import get_factory

@asynccontextmanager
async def lifespan(app: FastAPI):
    import logging
    import os
    log_level_str = os.environ.get("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    logging.basicConfig(level=log_level)
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
    
    # Enable CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    from dmesh.sdk.config import get_settings
    _BASE = get_settings().api.base_path.strip("/")
    
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        host = request.client.host if request.client else "unknown"
        port = request.client.port if request.client else "unknown"
        
        # Don't log health check
        is_health = request.url.path.endswith("/health")
        
        if not is_health:
            import logging
            logging.info(f'{host}:{port} - "{request.method} {request.url.path}"')
            
        response = await call_next(request)
        return response

    app.include_router(dps.router, prefix=f"/{_BASE}")
    app.include_router(dcs.router, prefix=f"/{_BASE}")
    app.include_router(discover_router, prefix=f"/{_BASE}")
    
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
        
    viewer_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "viewer")
    if os.path.isdir(viewer_dir):
        from fastapi.staticfiles import StaticFiles
        from fastapi.responses import FileResponse, RedirectResponse
        from fastapi import HTTPException
        
        # Mount the static assets under /dmesh-viewer/assets
        assets_dir = os.path.join(viewer_dir, "assets")
        if os.path.isdir(assets_dir):
            app.mount("/dmesh-viewer/assets", StaticFiles(directory=assets_dir), name="assets")
        
        @app.get("/dmesh-viewer")
        @app.get("/dmesh-viewer/")
        async def serve_spa_root():
            return FileResponse(os.path.join(viewer_dir, "index.html"))

        @app.get("/dmesh-viewer/{catchall:path}")
        async def serve_spa_catchall(request: Request, catchall: str):
            if catchall.startswith(_BASE):
                raise HTTPException(status_code=404, detail="Not Found")
            
            file_path = os.path.join(viewer_dir, catchall)
            if os.path.isfile(file_path):
                return FileResponse(file_path)
                
            return FileResponse(os.path.join(viewer_dir, "index.html"))

        @app.get("/")
        async def root_redirect():
            return RedirectResponse(url="/dmesh-viewer/")

    return app

app = create_app()
handler = Mangum(app)

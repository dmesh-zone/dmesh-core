import os
from fastapi import FastAPI
from app.routers import data_products, data_contracts
from app.db import get_pool

# Configurable base path — default "odm", override with WS_BASE_PATH env var
_BASE = os.environ.get("WS_BASE_PATH", "odm").strip("/")

app = FastAPI(title="open-data-mesh-ws")

app.include_router(data_products.router, prefix=f"/{_BASE}")
app.include_router(data_contracts.router, prefix=f"/{_BASE}")

_pool = None

def _get_pool():
    global _pool
    if _pool is None:
        _pool = get_pool()
    return _pool

@app.get(f"/{_BASE}/health")
def health():
    return {"status": "ok"}

@app.delete(f"/{_BASE}/flush", status_code=204)
def flush():
    """Delete all data products (and their contracts via cascade)."""
    import psycopg2
    from fastapi import HTTPException
    pool = _get_pool()
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM data_products")
        conn.commit()
    except psycopg2.Error:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Database error.")
    finally:
        pool.putconn(conn)

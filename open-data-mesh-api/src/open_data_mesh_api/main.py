import os
from fastapi import FastAPI
from mangum import Mangum
from open_data_mesh_api.routers import dps, dcs
from open_data_mesh_sdk import DataMeshService, PostgresRepository, SQLiteRepository


def get_repository():
    db_type = os.getenv("DB_TYPE", "sqlite").lower()
    
    if db_type == "postgres":
        from psycopg2 import pool
        _pool = pool.SimpleConnectionPool(
            minconn=1,
            maxconn=20,
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres"),
            dbname=os.getenv("DB_NAME", "postgres")
        )
        return PostgresRepository(_pool)
    else:
        # Default to SQLite for local development or simple standalone deployments
        db_path = os.getenv("DB_PATH", "odm.db")
        return SQLiteRepository(db_path)


app = FastAPI(title="Open Data Mesh API")

# Initialize SDK core and Repository
repository = get_repository()
service = DataMeshService(repository)

# Attach service to app state for routers to use
app.state.service = service

_BASE = os.environ.get("WS_BASE_PATH", "odm").strip("/")

app.include_router(dps.router, prefix=f"/{_BASE}")
app.include_router(dcs.router, prefix=f"/{_BASE}")

@app.get(f"/{_BASE}/health")
def health():
    return {"status": "ok"}

# Handler for AWS Lambda
handler = Mangum(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

import os
from fastapi import Request
from psycopg_pool import AsyncConnectionPool
from dmesh.sdk.ports.repository import DataProductRepository, DataContractRepository
from dmesh.sdk.adapters.psycopg import PostgresDataProductRepository, PostgresDataContractRepository

# Global pool instance
_pool = None

def get_pool():
    global _pool
    if _pool is None:
        conn_str = f"host={os.getenv('DB_HOST', 'localhost')} " \
                   f"port={os.getenv('DB_PORT', '5432')} " \
                   f"user={os.getenv('DB_USER', 'postgres')} " \
                   f"password={os.getenv('DB_PASSWORD', 'postgres')} " \
                   f"dbname={os.getenv('DB_NAME', 'postgres')}"
        _pool = AsyncConnectionPool(conninfo=conn_str, open=False)
    return _pool

async def get_dp_repo() -> DataProductRepository:
    """FastAPI dependency to provide a DataProductRepository implementation."""
    pool = get_pool()
    if not pool.opened:
        await pool.open()
    return PostgresDataProductRepository(pool)

async def get_dc_repo() -> DataContractRepository:
    """FastAPI dependency to provide a DataContractRepository implementation."""
    pool = get_pool()
    if not pool.opened:
        await pool.open()
    return PostgresDataContractRepository(pool)

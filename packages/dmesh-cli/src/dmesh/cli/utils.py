import os
from dmesh.sdk import DataMeshService
from dmesh.sdk.persistency.sqlite import SQLiteRepository
from dmesh.sdk.persistency.postgres import PostgresSyncRepository
from dmesh.cli.put.config_reader import ConfigReader
import psycopg_pool

def get_service() -> DataMeshService:
    config = ConfigReader().read()
    if config.sqlite_path:
        repo = SQLiteRepository(config.sqlite_path)
    elif config.pg_host:
        conn_str = f"host={config.pg_host} port={config.pg_port or 5432} user={config.pg_user} password={config.pg_password} dbname={config.pg_db}"
        # For CLI we use a simple threaded pool or similar for sync support
        pool = psycopg_pool.ConnectionPool(conn_str)
        repo = PostgresSyncRepository(pool)
    else:
        raise ValueError("No repository configured.")
    
    return DataMeshService(repo)
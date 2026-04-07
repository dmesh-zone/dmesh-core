import os
from dmesh.sdk import DataMeshService
from dmesh.sdk.persistency.in_memory import InMemoryRepository
from dmesh.cli.put.config_reader import ConfigReader, ConfigNotFoundError

def get_service() -> DataMeshService:
    try:
        config = ConfigReader().read()
        if config.pg_host:
            from dmesh.sdk.persistency.postgres import PostgresSyncRepository
            import psycopg_pool
            conn_str = f"host={config.pg_host} port={config.pg_port or 5432} user={config.pg_user} password={config.pg_password} dbname={config.pg_db}"
            pool = psycopg_pool.ConnectionPool(conn_str)
            repo = PostgresSyncRepository(pool)
        else:
            repo = InMemoryRepository()
    except ConfigNotFoundError:
        # For tests or when no config
        repo = InMemoryRepository()
    
    return DataMeshService(repo)
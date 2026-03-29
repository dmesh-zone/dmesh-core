from open_data_mesh_sdk import DataMeshService, PostgresRepository, SQLiteRepository
from dm.put.config_reader import ConfigReader

def get_service() -> DataMeshService:
    config = ConfigReader().read()
    if config.sqlite_path:
        repo = SQLiteRepository(config.sqlite_path)
    elif config.pg_host:
        from psycopg2 import pool
        _pool = pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            host=config.pg_host,
            port=config.pg_port or 5432,
            user=config.pg_user,
            password=config.pg_password,
            dbname=config.pg_db
        )
        repo = PostgresRepository(_pool)
    elif config.ws_base_url:
        # This is for backward compatibility or if we still want to support HTTP.
        # But for the refactor, we want CLI to use SDK directly.
        # If the user has a WS URL, we might need a RemoteRepository, but for now
        # let's assume CLI always has local DB access or we can add that later.
        raise ValueError("Remote execution is not supported in this CLI version yet. Use SQLite/Postgres.")
    else:
        raise ValueError("No repository configured.")
    
    return DataMeshService(repo)
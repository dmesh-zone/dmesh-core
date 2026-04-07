from typing import Optional, Protocol
from dmesh.sdk.ports.repository import DataProductRepository, DataContractRepository
from dmesh.sdk.persistency.in_memory import AsyncInMemoryDataProductRepository, AsyncInMemoryDataContractRepository

class RepositoryFactory(Protocol):
    def create_data_product_repository(self) -> DataProductRepository: ...
    def create_data_contract_repository(self) -> DataContractRepository: ...

class InMemoryRepositoryFactory:
    def __init__(self):
        self._dp_repo = AsyncInMemoryDataProductRepository()
        self._dc_repo = AsyncInMemoryDataContractRepository()

    def create_data_product_repository(self) -> DataProductRepository:
        return self._dp_repo

    def create_data_contract_repository(self) -> DataContractRepository:
        return self._dc_repo

class PostgresRepositoryFactory:
    def __init__(self, pool):
        from dmesh.sdk.persistency.postgres import PostgresDataProductRepository, PostgresDataContractRepository
        self.pool = pool
        self._dp_repo = PostgresDataProductRepository(self.pool)
        self._dc_repo = PostgresDataContractRepository(self.pool)

    async def open(self):
        await self.pool.open()

    async def close(self):
        await self.pool.close()

    def create_data_product_repository(self) -> DataProductRepository:
        return self._dp_repo

    def create_data_contract_repository(self) -> DataContractRepository:
        return self._dc_repo

class SyncPostgresRepositoryFactory:
    def __init__(self, pool):
        from dmesh.sdk.persistency.postgres import SyncPostgresDataProductRepository, SyncPostgresDataContractRepository
        self.pool = pool
        self._dp_repo = SyncPostgresDataProductRepository(self.pool)
        self._dc_repo = SyncPostgresDataContractRepository(self.pool)

    def create_data_product_repository(self) -> DataProductRepository:
        return self._dp_repo

    def create_data_contract_repository(self) -> DataContractRepository:
        return self._dc_repo

def create_repository_factory(
    db_type: str = "postgres",
    pg_host: Optional[str] = None,
    pg_port: Optional[int] = None,
    pg_user: Optional[str] = None,
    pg_password: Optional[str] = None,
    pg_db: Optional[str] = None,
) -> RepositoryFactory:
    if db_type == "memory":
        return InMemoryRepositoryFactory()
    elif db_type == "postgres":
        if not all([pg_host, pg_user, pg_password, pg_db]):
            raise ValueError("Postgres connection parameters required")
        import psycopg_pool
        conn_str = f"host={pg_host} port={pg_port or 5432} user={pg_user} password={pg_password} dbname={pg_db}"
        pool = psycopg_pool.AsyncConnectionPool(conninfo=conn_str, open=False)
        return PostgresRepositoryFactory(pool)
    elif db_type == "postgres_sync":
        if not all([pg_host, pg_user, pg_password, pg_db]):
            raise ValueError("Postgres connection parameters required")
        import psycopg_pool
        conn_str = f"host={pg_host} port={pg_port or 5432} user={pg_user} password={pg_password} dbname={pg_db}"
        pool = psycopg_pool.ConnectionPool(conn_str)
        return SyncPostgresRepositoryFactory(pool)
    else:
        raise ValueError(f"Unsupported db_type: {db_type}")
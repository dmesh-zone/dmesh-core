from typing import Any, Optional, Protocol
from dmesh.sdk.ports.repository import DataProductRepository, DataContractRepository
from dmesh.sdk.persistency.in_memory import AsyncInMemoryDataProductRepository, AsyncInMemoryDataContractRepository

class RepositoryFactory(Protocol):
    def get_data_product_repository(self) -> DataProductRepository: ...
    def get_data_contract_repository(self) -> DataContractRepository: ...

class InMemoryRepositoryFactory:
    def __init__(self):
        self._dp_repo = AsyncInMemoryDataProductRepository()
        self._dc_repo = AsyncInMemoryDataContractRepository()

    def get_data_product_repository(self) -> DataProductRepository:
        return self._dp_repo

    def get_data_contract_repository(self) -> DataContractRepository:
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

    def get_data_product_repository(self) -> DataProductRepository:
        return self._dp_repo

    def get_data_contract_repository(self) -> DataContractRepository:
        return self._dc_repo


class RepositoryFactory:
    def create_from_settings(self, settings, db_type: str = "postgres") -> RepositoryFactory:
        """
        Creates a repository factory using a Settings object from dmesh.sdk.config.
        """
        return self.create(
            db_type=db_type,
            pg_host=settings.db.host,
            pg_port=settings.db.port,
            pg_user=settings.db.user,
            pg_password=settings.db.password,
            pg_db=settings.db.name
        )

    def create(
        self,
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
            conn_str = f"host={pg_host} port={pg_port or 5432} user={pg_user} password={pg_password} dbname={pg_db} connect_timeout=10"
            pool = psycopg_pool.AsyncConnectionPool(conninfo=conn_str, open=False)
            return PostgresRepositoryFactory(pool)
        else:
            raise ValueError(f"Unsupported db_type: {db_type}")
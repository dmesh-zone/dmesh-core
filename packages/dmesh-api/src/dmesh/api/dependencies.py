import os
from fastapi import Request
from dmesh.sdk.ports.repository import DataProductRepository, DataContractRepository
from dmesh.sdk.persistency.factory import create_repository_factory

# Global factory instance
_factory = None

def get_factory():
    global _factory
    if _factory is None:
        _factory = create_repository_factory(
            db_type="postgres",
            pg_host=os.getenv('DB_HOST', 'localhost'),
            pg_port=int(os.getenv('DB_PORT', '5432')),
            pg_user=os.getenv('DB_USER', 'postgres'),
            pg_password=os.getenv('DB_PASSWORD', 'postgres'),
            pg_db=os.getenv('DB_NAME', 'postgres')
        )
    return _factory

async def get_dp_repo() -> DataProductRepository:
    """FastAPI dependency to provide a DataProductRepository implementation."""
    factory = get_factory()
    return factory.create_data_product_repository()

async def get_dc_repo() -> DataContractRepository:
    """FastAPI dependency to provide a DataContractRepository implementation."""
    factory = get_factory()
    return factory.create_data_contract_repository()

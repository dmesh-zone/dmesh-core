import os
from fastapi import Request
from dmesh.sdk.ports.repository import DataProductRepository, DataContractRepository
from dmesh.sdk.persistency.factory import RepositoryFactory

# Global factory instance
_factory = None

def get_factory():
    global _factory
    if _factory is None:
        from dmesh.sdk.config import get_settings
        settings = get_settings()
        _factory = RepositoryFactory().create_from_settings(settings, db_type=os.getenv('DB_TYPE', 'postgres'))
    return _factory

async def get_dp_repo() -> DataProductRepository:
    """FastAPI dependency to provide a DataProductRepository implementation."""
    factory = get_factory()
    return factory.get_data_product_repository()

async def get_dc_repo() -> DataContractRepository:
    """FastAPI dependency to provide a DataContractRepository implementation."""
    factory = get_factory()
    return factory.get_data_contract_repository()

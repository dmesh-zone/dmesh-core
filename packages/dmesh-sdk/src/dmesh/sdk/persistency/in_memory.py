from typing import List, Optional
from uuid import UUID
from dmesh.sdk.models import DataProduct, DataContract
from dmesh.sdk.ports.repository import DataProductRepository, DataContractRepository

class SyncInMemoryDataProductRepository:
    def __init__(self, data_products_dict):
        self._data_products = data_products_dict

    def save(self, product: DataProduct) -> None:
        self._data_products[product.id] = product

    def get(self, id: UUID) -> Optional[DataProduct]:
        return self._data_products.get(str(id))

    def list(self, domain: Optional[str] = None, name: Optional[str] = None) -> List[DataProduct]:
        results = list(self._data_products.values())
        if domain:
            results = [dp for dp in results if dp.domain == domain]
        if name:
            results = [dp for dp in results if dp.name == name]
        return results

    def delete(self, id: UUID) -> bool:
        dp_id = str(id)
        if dp_id in self._data_products:
            del self._data_products[dp_id]
            return True
        return False

class SyncInMemoryDataContractRepository:
    def __init__(self, data_contracts_dict):
        self._data_contracts = data_contracts_dict

    def save(self, contract: DataContract) -> None:
        self._data_contracts[contract.id] = contract

    def get(self, id: UUID) -> Optional[DataContract]:
        return self._data_contracts.get(str(id))

    def list(self, dp_id: Optional[str] = None) -> List[DataContract]:
        results = list(self._data_contracts.values())
        if dp_id:
            results = [dc for dc in results if dc.data_product_id == dp_id]
        return results

    def delete(self, id: UUID) -> bool:
        dc_id = str(id)
        if dc_id in self._data_contracts:
            del self._data_contracts[dc_id]
            return True
        return False

class InMemoryRepository:
    """Monolithic sync in-memory repository for legacy support."""
    def __init__(self):
        self._data_products = {}
        self._data_contracts = {}
        self.dp = SyncInMemoryDataProductRepository(self._data_products)
        self.dc = SyncInMemoryDataContractRepository(self._data_contracts)

    # Delegate to granular repos
    def create_data_product(self, dp: DataProduct) -> DataProduct:
        self.dp.save(dp); return dp
    def get_data_product(self, dp_id: str) -> Optional[DataProduct]:
        return self.dp.get(UUID(dp_id))
    def list_data_products(self, domain: str = None, name: str = None, version: str = None) -> List[DataProduct]:
        results = self.dp.list(domain=domain, name=name)
        if version:
            results = [dp for dp in results if dp.version == version]
        return results
    def update_data_product(self, dp: DataProduct) -> DataProduct:
        self.dp.save(dp); return dp
    def delete_data_product(self, dp_id: str) -> bool:
        return self.dp.delete(UUID(dp_id))

    def create_data_contract(self, dc: DataContract) -> DataContract:
        self.dc.save(dc); return dc
    def get_data_contract(self, dc_id: str) -> Optional[DataContract]:
        return self.dc.get(UUID(dc_id))
    def list_data_contracts(self, dp_id: str = None) -> List[DataContract]:
        return self.dc.list(dp_id=dp_id)
    def update_data_contract(self, dc: DataContract) -> DataContract:
        self.dc.save(dc); return dc
    def delete_data_contract(self, dc_id: str) -> bool:
        return self.dc.delete(UUID(dc_id))

    # Generic methods to allow passing this object as both repos to DMeshService
    def save(self, obj):
        if isinstance(obj, DataProduct): self.dp.save(obj)
        elif isinstance(obj, DataContract): self.dc.save(obj)
    def get(self, id: UUID):
        # This is ambiguous for monolithic repo, but we know DMeshService calls 
        # it on either dp_repo or dc_repo. If we use this object for both, 
        # we can try to find it in products then contracts.
        return self.dp.get(id) or self.dc.get(id)
    def list(self, **kwargs):
        # Also ambiguous.
        if "dp_id" in kwargs: return self.dc.list(**kwargs)
        return self.dp.list(**kwargs)
    def delete(self, id: UUID) -> bool:
        return self.dp.delete(id) or self.dc.delete(id)

    def flush(self) -> None:
        self._data_products.clear()
        self._data_contracts.clear()


class AsyncInMemoryDataProductRepository(DataProductRepository):
    def __init__(self):
        self.products = {}

    async def get(self, id: UUID) -> Optional[DataProduct]:
        return self.products.get(id)

    async def save(self, product: DataProduct) -> None:
        self.products[product.id] = product

    async def list(self, domain: Optional[str] = None, name: Optional[str] = None) -> List[DataProduct]:
        results = list(self.products.values())
        if domain:
            results = [p for p in results if p.domain == domain]
        if name:
            results = [p for p in results if p.name == name]
        return results

    async def delete(self, id: UUID) -> bool:
        if id in self.products:
            del self.products[id]
            return True
        return False


class AsyncInMemoryDataContractRepository(DataContractRepository):
    def __init__(self):
        self.contracts = {}

    async def get(self, id: UUID) -> Optional[DataContract]:
        return self.contracts.get(id)

    async def save(self, contract: DataContract) -> None:
        self.contracts[contract.id] = contract

    async def list(self, dp_id: Optional[str] = None) -> List[DataContract]:
        results = list(self.contracts.values())
        if dp_id:
            results = [c for c in results if c.data_product_id == dp_id]
        return results

    async def delete(self, id: UUID) -> bool:
        if id in self.contracts:
            del self.contracts[id]
            return True
        return False

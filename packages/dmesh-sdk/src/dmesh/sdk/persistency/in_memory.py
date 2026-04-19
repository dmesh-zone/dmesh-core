from datetime import datetime
from uuid import UUID
from typing import List, Optional
from dmesh.sdk.models import DataProduct, DataContract
from dmesh.sdk.ports.repository import DataProductRepository, DataContractRepository

class AsyncInMemoryDataProductRepository(DataProductRepository):
    def __init__(self):
        self.products = {}

    async def get(self, id: UUID) -> Optional[DataProduct]:
        return self.products.get(id)

    async def save(self, product: DataProduct) -> None:
        if product.id not in self.products:
            product.created_at = datetime.now()
        product.updated_at = datetime.now()
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


    async def truncate(self) -> None:
        self.products.clear()

class AsyncInMemoryDataContractRepository(DataContractRepository):
    def __init__(self):
        self.contracts = {}

    async def get(self, id: UUID) -> Optional[DataContract]:
        return self.contracts.get(id)

    async def save(self, contract: DataContract) -> None:
        if contract.id not in self.contracts:
            contract.created_at = datetime.now()
        contract.updated_at = datetime.now()
        self.contracts[contract.id] = contract

    async def list(self, dp_id: Optional[UUID] = None) -> List[DataContract]:
        results = list(self.contracts.values())
        if dp_id:
            results = [c for c in results if c.data_product_id == dp_id]
        return results

    async def delete(self, id: UUID) -> bool:
        if id in self.contracts:
            del self.contracts[id]
            return True
        return False
    async def truncate(self) -> None:
        self.contracts.clear()

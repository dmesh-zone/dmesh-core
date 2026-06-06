from datetime import datetime
from uuid import UUID
from typing import List, Optional
from dmesh.sdk.models import DataProduct, DataContract
from dmesh.sdk.ports.repository import DataProductRepository, DataContractRepository
import logging

logger = logging.getLogger(__name__)

class AsyncInMemoryDataProductRepository(DataProductRepository):
    def __init__(self):
        self.products = {}

    async def get(self, id: UUID) -> Optional[DataProduct]:
        logger.info(f"get {id}")
        return self.products.get(id)

    async def save(self, product: DataProduct) -> None:
        logger.info(f"save {product.id}")
        now = datetime.now()
        if product.id not in self.products:
            product.created_at = now
        else:
            product.created_at = self.products[product.id].created_at
        product.updated_at = now
        self.products[product.id] = product

    async def list(self, domain: Optional[str] = None, name: Optional[str] = None) -> List[DataProduct]:
        logger.info(f"list domain={domain} name={name}")
        results = list(self.products.values())
        if domain:
            results = [p for p in results if p.domain == domain]
        if name:
            results = [p for p in results if p.name == name]
        return results

    async def delete(self, id: UUID) -> bool:
        logger.info(f"delete {id}")
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
        logger.info(f"get {id}")
        return self.contracts.get(id)

    async def save(self, contract: DataContract) -> None:
        logger.info(f"save {contract.id}")
        now = datetime.now()
        if contract.id not in self.contracts:
            contract.created_at = now
        else:
            contract.created_at = self.contracts[contract.id].created_at
        contract.updated_at = now
        self.contracts[contract.id] = contract

    async def list(self, dp_id: Optional[UUID] = None) -> List[DataContract]:
        logger.info(f"list dp_id={dp_id}")
        results = list(self.contracts.values())
        if dp_id:
            results = [c for c in results if c.data_product_id == dp_id]
        return results

    async def delete(self, id: UUID) -> bool:
        logger.info(f"delete {id}")
        if id in self.contracts:
            del self.contracts[id]
            return True
        return False

    async def truncate(self) -> None:
        logger.info("truncate")
        self.contracts.clear()

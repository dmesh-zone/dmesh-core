from typing import List, Optional
from dmesh.sdk.models import DataProduct, DataContract
from dmesh.sdk.ports.repository import DataMeshRepository

class InMemoryRepository(DataMeshRepository):
    def __init__(self):
        self._data_products = {}
        self._data_contracts = {}

    def create_data_product(self, dp: DataProduct) -> DataProduct:
        self._data_products[dp.id] = dp
        return dp

    def get_data_product(self, dp_id: str) -> Optional[DataProduct]:
        return self._data_products.get(dp_id)

    def list_data_products(self, domain: str = None, name: str = None, version: str = None) -> List[DataProduct]:
        results = list(self._data_products.values())
        if domain:
            results = [dp for dp in results if dp.domain == domain]
        if name:
            results = [dp for dp in results if dp.name == name]
        if version:
            results = [dp for dp in results if dp.version == version]
        return results

    def update_data_product(self, dp: DataProduct) -> DataProduct:
        if dp.id not in self._data_products:
            raise ValueError(f"Data product {dp.id} not found")
        self._data_products[dp.id] = dp
        return dp

    def delete_data_product(self, dp_id: str) -> bool:
        if dp_id in self._data_products:
            del self._data_products[dp_id]
            return True
        return False

    def create_data_contract(self, dc: DataContract) -> DataContract:
        self._data_contracts[dc.id] = dc
        return dc

    def get_data_contract(self, dc_id: str) -> Optional[DataContract]:
        return self._data_contracts.get(dc_id)

    def list_data_contracts(self, dp_id: str = None) -> List[DataContract]:
        results = list(self._data_contracts.values())
        if dp_id:
            results = [dc for dc in results if dc.data_product_id == dp_id]
        return results

    def update_data_contract(self, dc: DataContract) -> DataContract:
        if dc.id not in self._data_contracts:
            raise ValueError(f"Data contract {dc.id} not found")
        self._data_contracts[dc.id] = dc
        return dc

    def delete_data_contract(self, dc_id: str) -> bool:
        if dc_id in self._data_contracts:
            del self._data_contracts[dc_id]
            return True
        return False

    def flush(self) -> None:
        self._data_products.clear()
        self._data_contracts.clear()

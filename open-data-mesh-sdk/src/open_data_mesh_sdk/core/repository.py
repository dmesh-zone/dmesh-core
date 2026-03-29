from abc import ABC, abstractmethod
from typing import List, Optional

from open_data_mesh_sdk.core.models import DataProduct, DataContract


class DataMeshRepository(ABC):
    @abstractmethod
    def create_data_product(self, dp: DataProduct) -> DataProduct:
        pass

    @abstractmethod
    def get_data_product(self, dp_id: str) -> Optional[DataProduct]:
        pass

    @abstractmethod
    def list_data_products(self, domain: str = None, name: str = None, version: str = None) -> List[DataProduct]:
        pass

    @abstractmethod
    def update_data_product(self, dp: DataProduct) -> DataProduct:
        pass

    @abstractmethod
    def delete_data_product(self, dp_id: str) -> bool:
        pass

    @abstractmethod
    def create_data_contract(self, dc: DataContract) -> DataContract:
        pass

    @abstractmethod
    def get_data_contract(self, dc_id: str) -> Optional[DataContract]:
        pass

    @abstractmethod
    def list_data_contracts(self, dp_id: str = None) -> List[DataContract]:
        pass

    @abstractmethod
    def update_data_contract(self, dc: DataContract) -> DataContract:
        pass

    @abstractmethod
    def delete_data_contract(self, dc_id: str) -> bool:
        pass

    @abstractmethod
    def flush(self) -> None:
        """Clear all data."""
        pass

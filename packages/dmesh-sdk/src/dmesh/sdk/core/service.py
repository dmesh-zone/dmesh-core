from typing import Any, List, Optional
from dmesh.sdk.models import DataProduct, DataContract
from dmesh.sdk.sdk import SyncSDK

class DMeshService:
    def __init__(self, factory: Any):
        self.sdk = SyncSDK(factory)

    def create_data_product(self, spec: dict[str, Any]) -> DataProduct:
        return self.sdk.put_data_product(spec, include_metadata=True)

    def get_data_product(self, id: str) -> Optional[DataProduct]:
        return self.sdk.get_data_product(id, include_metadata=True)

    def list_data_products(self, domain: str = None, name: str = None, version: str = None) -> List[DataProduct]:
        results = self.sdk.list_data_products(domain=domain, name=name, include_metadata=True)
        if version:
            results = [r for r in results if r.specification.get("info", {}).get("version") == version]
        return results

    def update_data_product(self, id: str, spec: dict[str, Any]) -> DataProduct:
        spec_with_id = {**spec, "id": id}
        return self.sdk.put_data_product(spec_with_id, include_metadata=True)

    def delete_data_product(self, id: str) -> bool:
        return self.sdk.delete_data_product(id)

    def create_data_contract(self, dp_id: str, spec: dict[str, Any]) -> DataContract:
        return self.sdk.put_data_contract(spec, dp_id=dp_id, include_metadata=True)

    def get_data_contract(self, id: str) -> Optional[DataContract]:
        return self.sdk.get_data_contract(id, include_metadata=True)

    def list_data_contracts(self, dp_id: str = None) -> List[DataContract]:
        return self.sdk.list_data_contracts(dp_id=dp_id, include_metadata=True)

    def update_data_contract(self, id: str, spec: dict[str, Any]) -> DataContract:
        spec_with_id = {**spec, "id": id}
        return self.sdk.put_data_contract(spec_with_id, include_metadata=True)

    def delete_data_contract(self, id: str) -> bool:
        return self.sdk.delete_data_contract(id)

    def patch_data_contract(self, id: str, spec: dict[str, Any]) -> DataContract:
        return self.sdk.patch_data_contract(id, spec, include_metadata=True)

    def put_data_contract(self, spec: dict[str, Any], dp_id: Optional[str] = None) -> DataContract:
        return self.sdk.put_data_contract(spec, dp_id=dp_id, include_metadata=True)

    def put_data_product(self, spec: dict[str, Any]) -> DataProduct:
        return self.sdk.put_data_product(spec, include_metadata=True)

    def flush(self) -> None:
        self.sdk.flush()

from typing import Any, List, Optional

from open_data_mesh_sdk.core.enricher import enrich_spec
from open_data_mesh_sdk.core.models import DataProduct, DataContract
from open_data_mesh_sdk.core.repository import DataMeshRepository
from open_data_mesh_sdk.core.validator import validate_spec
from open_data_mesh_sdk.core.id_generator import make_dc_id


class DataMeshService:
    def __init__(self, repository: DataMeshRepository):
        self.repository = repository

    def create_data_product(self, spec: dict[str, Any]) -> DataProduct:
        enriched = enrich_spec(spec)
        validate_spec(enriched)
        dp = DataProduct(id=enriched["id"], specification=enriched)
        return self.repository.create_data_product(dp)

    def get_data_product(self, dp_id: str) -> Optional[DataProduct]:
        return self.repository.get_data_product(dp_id)

    def list_data_products(self, domain: str = None, name: str = None, version: str = None) -> List[DataProduct]:
        return self.repository.list_data_products(domain, name, version)

    def update_data_product(self, dp_id: str, spec: dict[str, Any]) -> DataProduct:
        # Merge ID to ensure it's preserved
        spec_with_id = {**spec, "id": dp_id}
        enriched = enrich_spec(spec_with_id)
        validate_spec(enriched)
        dp = DataProduct(id=dp_id, specification=enriched)
        return self.repository.update_data_product(dp)

    def delete_data_product(self, dp_id: str) -> bool:
        return self.repository.delete_data_product(dp_id)

    def create_data_contract(self, dp_id: str, spec: dict[str, Any]) -> DataContract:
        # We need the parent DP info to generate DC ID deterministically
        dp = self.repository.get_data_product(dp_id)
        if not dp:
            # Match the CLI test's expected error message
            raise ValueError(f"Parent Data Product {dp_id} not found")

        # Count existing DCs to get index
        existing_dcs = self.repository.list_data_contracts(dp_id=dp_id)
        dc_index = len(existing_dcs)

        # Generate DC ID
        dc_id = make_dc_id(dp.domain, dp.name, dp.version, dc_index)
        
        # Merge ID and apply defaults for validation
        enriched_dc = {
            "apiVersion": "v3.1.0",
            "kind": "DataContract",
            "version": "v1.0.0",
            "status": "draft",
            **spec,
            "id": dc_id
        }
        validate_spec(enriched_dc)

        dc = DataContract(id=dc_id, data_product_id=dp_id, specification=enriched_dc)
        return self.repository.create_data_contract(dc)

    def get_data_contract(self, dc_id: str) -> Optional[DataContract]:
        return self.repository.get_data_contract(dc_id)

    def list_data_contracts(self, dp_id: str = None) -> List[DataContract]:
        return self.repository.list_data_contracts(dp_id=dp_id)

    def update_data_contract(self, dc_id: str, spec: dict[str, Any]) -> DataContract:
        existing = self.repository.get_data_contract(dc_id)
        if not existing:
            raise ValueError(f"Data contract {dc_id} not found")
        
        # Merge ID and apply defaults for validation
        enriched_dc = {
            "apiVersion": "v3.1.0",
            "kind": "DataContract",
            **spec,
            "id": dc_id
        }
        validate_spec(enriched_dc)
        dc = DataContract(id=dc_id, data_product_id=existing.data_product_id, specification=enriched_dc)
        return self.repository.update_data_contract(dc)

    def delete_data_contract(self, dc_id: str) -> bool:
        return self.repository.delete_data_contract(dc_id)

    def put_data_contract(self, dp_id: Optional[str], spec: dict[str, Any]) -> DataContract:
        dc_id = spec.get("id")

        # if dc_id not provided, create an id for dc
        if not dc_id:
            dp = self.repository.get_data_product(dp_id)
            if not dp:
                raise ValueError(f"Parent Data Product {dp_id} not found")
            existing_dcs = self.repository.list_data_contracts(dp_id=dp_id)
            dc_index = len(existing_dcs)
            dc_id = make_dc_id(dp.domain, dp.name, dp.version, dc_index)
            spec["id"] = dc_id

        # ensure defaults are added if not provided
        enriched = {"apiVersion": "v3.1.0", "kind": "DataContract", "version": "v1.0.0", "status": "draft", **spec}
           
        # validate spec upfront (enrich with minimal defaults)
        validate_spec(enriched)

        if dc_id and self.repository.get_data_contract(dc_id):
            return self.update_data_contract(dc_id, spec)
        else:
            return self.create_data_contract(dp_id, spec)

    def put_data_product(self, spec: dict[str, Any]) -> DataProduct:
        dp_id = spec.get("id")

        if not dp_id:
            domain = spec.get("domain")
            name = spec.get("name")
            if domain and name:
                version = spec.get("version", "v1.0.0")
                results = self.list_data_products(domain=domain, name=name, version=version)
                if results:
                    dp_id = results[0].id

        # validate spec against schema and raise ValidationError exception if invalid
        # We enrich first to ensure defaults like apiVersion and kind are present
        enriched = enrich_spec({**spec, "id": dp_id} if dp_id else spec)
        validate_spec(enriched)
        
        if dp_id:
            return self.update_data_product(dp_id, spec)
        else:
            return self.create_data_product(spec)

    def flush(self) -> None:
        self.repository.flush()

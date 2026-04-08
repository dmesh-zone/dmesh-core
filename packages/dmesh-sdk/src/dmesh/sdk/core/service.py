from typing import Any, List, Optional

from dmesh.sdk.core.enricher import enrich_dp_spec, enrich_dc_spec
from dmesh.sdk.models import DataProduct, DataContract
from dmesh.sdk.core.validator import validate_spec
from dmesh.sdk.core.id_generator import make_dc_id
from uuid import UUID


class DMeshService:
    def __init__(self, dp_repo, dc_repo):
        self.dp_repo = dp_repo
        self.dc_repo = dc_repo

    def create_data_product(self, spec: dict[str, Any]) -> DataProduct:
        enriched = enrich_dp_spec(spec)
        validate_spec(enriched)
        dp = DataProduct(id=enriched["id"], specification=enriched)
        self.dp_repo.save(dp)
        return dp

    def get_data_product(self, dp_id: str) -> Optional[DataProduct]:
        try:
            return self.dp_repo.get(UUID(dp_id))
        except ValueError:
            return None

    def list_data_products(self, domain: str = None, name: str = None, version: str = None) -> List[DataProduct]:
        # Note: version filtering could be added to repo list if needed
        return self.dp_repo.list(domain=domain, name=name)

    def update_data_product(self, dp_id: str, spec: dict[str, Any]) -> DataProduct:
        spec_with_id = {**spec, "id": dp_id}
        enriched = enrich_dp_spec(spec_with_id)
        validate_spec(enriched)
        dp = DataProduct(id=dp_id, specification=enriched)
        self.dp_repo.save(dp)
        return dp

    def delete_data_product(self, dp_id: str) -> bool:
        try:
            return self.dp_repo.delete(UUID(dp_id))
        except ValueError:
            return False

    def create_data_contract(self, dp_id: str, spec: dict[str, Any]) -> DataContract:
        dp = self.get_data_product(dp_id)
        if not dp:
            raise ValueError(f"Parent Data Product {dp_id} not found")

        existing_dcs = self.dc_repo.list(dp_id=dp_id)
        dc_index = len(existing_dcs)
        dc_id = make_dc_id(dp.domain, dp.name, dp.version, dc_index)
        
        enriched_dc = enrich_dc_spec({**spec, "id": dc_id}, dp_spec=dp.specification)
        validate_spec(enriched_dc)

        dc = DataContract(id=dc_id, data_product_id=dp_id, specification=enriched_dc)
        self.dc_repo.save(dc)
        return dc

    def get_data_contract(self, dc_id: str) -> Optional[DataContract]:
        try:
            return self.dc_repo.get(UUID(dc_id))
        except ValueError:
            return None

    def list_data_contracts(self, dp_id: str = None) -> List[DataContract]:
        return self.dc_repo.list(dp_id=dp_id)

    def update_data_contract(self, dc_id: str, spec: dict[str, Any]) -> DataContract:
        existing = self.dc_repo.get(UUID(dc_id))
        if not existing:
            raise ValueError(f"Data contract {dc_id} not found")
        
        enriched_dc = enrich_dc_spec({**spec, "id": dc_id})
        validate_spec(enriched_dc)
        dc = DataContract(id=dc_id, data_product_id=existing.data_product_id, specification=enriched_dc)
        self.dc_repo.save(dc)
        return dc

    def delete_data_contract(self, dc_id: str) -> bool:
        try:
            return self.dc_repo.delete(UUID(dc_id))
        except ValueError:
            return False

    def put_data_contract(self, dp_id: Optional[str], spec: dict[str, Any]) -> DataContract:
        dc_id = spec.get("id")

        if not dc_id:
            dp = self.dp_repo.get(UUID(dp_id))
            if not dp:
                raise ValueError(f"Parent Data Product {dp_id} not found")
            existing_dcs = self.dc_repo.list(dp_id=dp_id)
            dc_index = len(existing_dcs)
            dc_id = make_dc_id(dp.domain, dp.name, dp.version, dc_index)
            spec["id"] = dc_id

        enriched = {"apiVersion": "v3.1.0", "kind": "DataContract", "version": "v1.0.0", "status": "draft", **spec}
        validate_spec(enriched)

        if dc_id and self.get_data_contract(dc_id):
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
        enriched = enrich_dp_spec({**spec, "id": dp_id} if dp_id else spec)
        validate_spec(enriched)
        
        if dp_id:
            return self.update_data_product(dp_id, spec)
        else:
            return self.create_data_product(spec)

    def flush(self) -> None:
        with self.dp_repo.pool.connection() as conn:
            conn.execute("DELETE FROM data_products")
            conn.execute("DELETE FROM data_contracts")

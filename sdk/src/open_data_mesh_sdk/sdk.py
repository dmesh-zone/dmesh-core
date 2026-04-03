from typing import Any, List, Optional, Union
from open_data_mesh_sdk.core.service import DataMeshService
from open_data_mesh_sdk.core.repository import DataMeshRepository
from open_data_mesh_sdk.core.models import DataProduct, DataContract

class OpenDataMesh:
    """The python interface for the Open Data Mesh SDK."""
    def __init__(self, repository: DataMeshRepository):
        self._svc = DataMeshService(repository)

    # Data Product Methods
    def create_dp(self, spec: dict[str, Any], domain: Optional[str] = None, name: Optional[str] = None) -> DataProduct:
        """Create a new data product. Domain and name can be provided in the spec or overriden as args."""
        merged_spec = {**spec}
        if domain: merged_spec["domain"] = domain
        if name: merged_spec["name"] = name
        return self._svc.create_data_product(merged_spec)

    def update_dp(self, spec: dict[str, Any]) -> DataProduct:
        """Update or patch an existing data product. Requires id in the spec."""
        dp_id = spec.get("id")
        if not dp_id:
            raise ValueError("Data product id is required for update")
        return self._svc.update_data_product(dp_id, spec)

    def get_dp(self, id: Optional[str] = None, domain: Optional[str] = None, name: Optional[str] = None) -> Optional[DataProduct]:
        """Fetch a single data product by ID or by domain/name."""
        if id:
            return self._svc.get_data_product(id)
        if domain and name:
            results = self._svc.list_data_products(domain=domain, name=name)
            return results[0] if results else None
        return None

    def list_dps(self, domain: Optional[str] = None, name: Optional[str] = None) -> List[DataProduct]:
        """List data products with optional filtering by domain and name."""
        return self._svc.list_data_products(domain=domain, name=name)

    def delete_dp(self, id: str) -> bool:
        """Delete a data product by ID."""
        return self._svc.delete_data_product(id)

    # Data Contract Methods
    def create_dc(self, spec: dict[str, Any], dp_id: str) -> DataContract:
        """Create a data contract for a given data product."""
        return self._svc.create_data_contract(dp_id, spec)

    def update_dc(self, spec: dict[str, Any]) -> DataContract:
        """Update an existing data contract. Requires id in the spec."""
        dc_id = spec.get("id")
        if not dc_id:
            raise ValueError("Data contract id is required for update")
        return self._svc.update_data_contract(dc_id, spec)

    def get_dc(self, id: str) -> Optional[DataContract]:
        """Fetch a single data contract by ID."""
        return self._svc.get_data_contract(id)

    def list_dcs(self, domain: Optional[str] = None, dp_name: Optional[str] = None) -> List[DataContract]:
        """List data contracts, optionally filtering by parent data product domain/name."""
        if domain or dp_name:
            dps = self._svc.list_data_products(domain=domain, name=dp_name)
            all_dcs = []
            for dp in dps:
                all_dcs.extend(self._svc.list_data_contracts(dp_id=dp.id))
            return all_dcs
        return self._svc.list_data_contracts()

    def delete_dc(self, id: str) -> bool:
        """Delete a data contract by ID."""
        return self._svc.delete_data_contract(id)

    # Discovery Methods
    def discover(self, dp_id: Optional[str] = None, domain: Optional[str] = None, name: Optional[str] = None) -> List[Union[DataProduct, DataContract]]:
        """Discovery by ID OR by domain and name. Returns a flat list of DataProduct and DataContract objects."""
        results = []
        dps = []
        if dp_id:
            dp = self._svc.get_data_product(dp_id)
            if dp: dps = [dp]
        elif domain and name:
            dps = self._svc.list_data_products(domain=domain, name=name)
        
        for dp in dps:
            results.append(dp)
            dcs = self._svc.list_data_contracts(dp_id=dp.id)
            results.extend(dcs)
        return results

    def flush(self) -> None:
        """Flush the repository (if supported)."""
        self._svc.flush()

from typing import Any, List, Optional, Union
from open_data_mesh_sdk.core.service import DataMeshService
from open_data_mesh_sdk.core.repository import DataMeshRepository
from open_data_mesh_sdk.core.models import DataProduct, DataContract

class OpenDataMesh:
    """The python interface for the Open Data Mesh SDK."""
    def __init__(self, repository: DataMeshRepository):
        self._svc = DataMeshService(repository)

    # Data Product Methods
    def create_dp(self, spec: dict[str, Any], domain: Optional[str] = None, name: Optional[str] = None, include_metadata: Optional[bool] = False) -> DataProduct:
        """Create a new data product. Domain and name can be provided in the spec or overriden as args."""
        merged_spec = {**spec}
        if domain: merged_spec["domain"] = domain
        if name: merged_spec["name"] = name
        return self._svc.create_data_product(merged_spec).specification if not include_metadata else self._svc.create_data_product(merged_spec)

    def update_dp(self, spec: dict[str, Any], include_metadata: Optional[bool] = False, include_metadata_in_response: Optional[bool] = False) -> DataProduct:
        """Update or patch an existing data product. Requires id in the spec."""
        dp_id = spec.get("id")
        if not dp_id:
            raise ValueError("Data product id is required for update")
        return self._svc.update_data_product(dp_id, spec).specification if not include_metadata_in_response else self._svc.update_data_product(dp_id, spec)

    def get_dp(self, id: Optional[str] = None, domain: Optional[str] = None, name: Optional[str] = None, include_metadata: bool = False) -> Optional[DataProduct]:
        """Fetch a single data product by ID or by domain/name."""
        if id:
            if not include_metadata:
                dp = self._svc.get_data_product(id)
                return dp.specification if dp else None
            else:
                return self._svc.get_data_product(id)
        if domain and name:
            results = self._svc.list_data_products(domain=domain, name=name)
            if results:
                if not include_metadata:
                    return [dp.specification for dp in results]
                else:
                    return results[0]
            else:
                return None
        return None

    def list_dps(self, domain: Optional[str] = None, name: Optional[str] = None, include_metadata: Optional[bool] = False) -> List[DataProduct]:
        """List data products with optional filtering by domain and name."""
        if not include_metadata:
            return [dp.specification for dp in self._svc.list_data_products(domain=domain, name=name)]
        else:
            return self._svc.list_data_products(domain=domain, name=name)

    def delete_dp(self, id: str) -> bool:
        """Delete a data product by ID."""
        return self._svc.delete_data_product(id)

    # Data Contract Methods
    def create_dc(self, spec: dict[str, Any], dp_id: str, include_metadata: Optional[bool] = False) -> DataContract:
        """Create a data contract for a given data product."""
        return self._svc.create_data_contract(dp_id, spec).specification if not include_metadata else self._svc.create_data_contract(dp_id, spec)

    def update_dc(self, spec: dict[str, Any], include_metadata: Optional[bool] = False, include_metadata_in_response: Optional[bool] = False) -> DataContract:
        """Update an existing data contract. Requires id in the spec."""
        dc_id = spec.get("id")
        if not dc_id:
            raise ValueError("Data contract id is required for update")
        return self._svc.update_data_contract(dc_id, spec).specification if not include_metadata_in_response else self._svc.update_data_contract(dc_id, spec)

    def patch_dc(self, spec: dict[str, Any], include_metadata: Optional[bool] = False) -> DataContract:
        """Patch an existing data contract. Supports partial updates and appends to customProperties."""
        dc_id = spec.get("id")
        if not dc_id:
            raise ValueError("Data contract id is required for patch")
        
        # 1. Fetch current
        current_full = self._svc.get_data_contract(dc_id)
        if not current_full:
            raise ValueError(f"Data contract {dc_id} not found")
        
        current_spec = current_full.specification.copy()

        # 2. Merge logic
        spec_to_update = current_spec.copy()
        for key, value in spec.items():
            if key == "customProperties" and key in spec_to_update:
                # When patching, customProperties should be appended instead of replaced
                spec_to_update[key] = spec_to_update[key] + value
            else:
                spec_to_update[key] = value
        
        # 3. Update
        return self.update_dc(spec_to_update, include_metadata=include_metadata)

    def get_dc(self, id: str, include_metadata: Optional[bool] = False, include_metadata_in_response: Optional[bool] = False) -> Optional[DataContract]:
        """Fetch a single data contract by ID."""
        if include_metadata:
            return self._svc.get_data_contract(id)
        else:
            dc = self._svc.get_data_contract(id)
            if dc:
                return dc.specification
            else:
                return None

    def list_dcs(self, domain: Optional[str] = None, dp_name: Optional[str] = None, include_metadata: Optional[bool] = False, include_metadata_in_response: Optional[bool] = False) -> List[DataContract]:
        """List data contracts, optionally filtering by parent data product domain/name."""
        if domain or dp_name:
            dps = self._svc.list_data_products(domain=domain, name=dp_name)
            all_dcs = []
            for dp in dps:
                if not include_metadata:
                    all_dcs.extend([dc.specification for dc in self._svc.list_data_contracts(dp_id=dp.id)])
                else:
                    all_dcs.extend(self._svc.list_data_contracts(dp_id=dp.id))
            return all_dcs
        else:
            if not include_metadata:
                return [dc.specification for dc in self._svc.list_data_contracts()]
            else:
                return self._svc.list_data_contracts()

    def delete_dc(self, id: str) -> bool:
        """Delete a data contract by ID."""
        return self._svc.delete_data_contract(id)

    # Discovery Methods
    def discover(self, dp_id: Optional[str] = None, domain: Optional[str] = None, name: Optional[str] = None, include_metadata: Optional[bool] = False, include_metadata_in_response: Optional[bool] = False) -> List[Union[DataProduct, DataContract]]:
        """Discovery by ID OR by domain and name. Returns a flat list of DataProduct and DataContract objects."""
        results = []
        dps = []
        if dp_id:
            dp = self._svc.get_data_product(dp_id)
            if dp is not None:
                if not include_metadata_in_response:
                    dps.append(dp.specification)
                else:
                    dps.append(dp)
        elif domain and name:
            if not include_metadata:
                dps = [dp.specification for dp in self._svc.list_data_products(domain=domain, name=name)]
            else:
                dps = self._svc.list_data_products(domain=domain, name=name)
        
        for dp in dps:
            results.append(dp)
            if not include_metadata:
                dcs = []
                for dc in self._svc.list_data_contracts(dp_id=dp["id"]):
                    dcs.append(dc.specification)
            else:
                dcs = self._svc.list_data_contracts(dp_id=dp["id"])
            results.extend(dcs)
        return results

    def flush(self) -> None:
        """Flush the repository (if supported)."""
        self._svc.flush()

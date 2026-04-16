from __future__ import annotations
import jsonschema.exceptions
import copy
from typing import Any, List, Optional, Union
from uuid import UUID
from dmesh.sdk.models import (
    DataProduct, 
    DataContract, 
    DataProductValidationError, 
    DataContractValidationError
)
from dmesh.sdk.core.enricher import enrich_dp_spec, enrich_dc_spec
from dmesh.sdk.core.validator import validate_spec
from dmesh.sdk.core.id_generator import make_dc_id, IDGenerator, get_generator


class _RepoWrapper:
    """Internal helper to satisfy factory-based init from individual repos."""
    def __init__(self, dp_repo=None, dc_repo=None):
        self._dp = dp_repo
        self._dc = dc_repo
    def get_data_product_repository(self): return self._dp
    def get_data_contract_repository(self): return self._dc


class AsyncSDK:
    """Asynchronous SDK for Data Mesh operations."""
    
    def __init__(self, factory: Any, settings: Optional[Any] = None, id_generator: Optional[IDGenerator] = None):
        self.factory = factory
        self.settings = settings
        self.dp_repo = factory.get_data_product_repository()
        self.dc_repo = factory.get_data_contract_repository()
        self.id_generator = id_generator or get_generator()
        
        # Initialize configuration options
        self.single_data_contract_per_product = True
        self.dua_start_date_default = "2026-01-01"
        self.dua_purpose_default = "Unknown purpose"
        self.data_product_status_default = "active"
        self.data_contract_status_default = "active"
        self.expand_port_adapters = True
        self.enrich_output_ports = True
        if settings:
            sdk_settings = getattr(settings, "sdk", settings)
            self.single_data_contract_per_product = getattr(sdk_settings, "single_data_contract_per_product", self.single_data_contract_per_product)
            self.dua_start_date_default = getattr(sdk_settings, "dua_start_date_default", self.dua_start_date_default)
            self.dua_purpose_default = getattr(sdk_settings, "dua_purpose_default", self.dua_purpose_default)
            self.data_product_status_default = getattr(sdk_settings, "data_product_status_default", self.data_product_status_default)
            self.data_contract_status_default = getattr(sdk_settings, "data_contract_status_default", self.data_contract_status_default)
            self.expand_port_adapters = getattr(sdk_settings, "expand_port_adapters", self.expand_port_adapters)
            self.enrich_output_ports = getattr(sdk_settings, "enrich_output_ports", self.enrich_output_ports)

    async def __aenter__(self):
        if hasattr(self.factory, "open") and callable(getattr(self.factory, "open")):
            await self.factory.open()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self.factory, "close") and callable(getattr(self.factory, "close")):
            await self.factory.close()

    def _prepare_dp_spec(self, spec: dict[str, Any], dp_id: Optional[str] = None, validate: bool = True) -> dict[str, Any]:
        """Enrich and validate data product specification."""
        try:
            merged_spec = copy.deepcopy(spec)
            
            # 1. Expand port adapters if present
            self._expand_port_adapters(merged_spec)
            
            # 2. Basic enrichment (defaults, ID)
            enriched = enrich_dp_spec(
                merged_spec, 
                id_generator=self.id_generator,
                status_default=self.data_product_status_default
            )
            
            # 3. Enrich output ports (contractId, etc.)
            self._enrich_output_ports(enriched)
            
            if dp_id:
                enriched["id"] = dp_id
            if validate:
                validate_spec(enriched)
            return enriched
        except jsonschema.exceptions.ValidationError as e:
            raise DataProductValidationError(f"Invalid Data Product specification: {e.message}") from e

    def _expand_port_adapters(self, spec: dict[str, Any]) -> None:
        """Expand output ports based on portAdapters custom property on ports."""
        if not self.expand_port_adapters:
            return
            
        if "outputPorts" not in spec or not isinstance(spec["outputPorts"], list):
            return
            
        original_ports = [p for p in spec["outputPorts"]]
        for port in original_ports:
            if not isinstance(port, dict): continue
            
            # Look for portAdapters in port-level customProperties
            adapters = None
            custom_props = port.get("customProperties", [])
            for prop in custom_props:
                if prop.get("property") == "portAdapters":
                    adapters = prop.get("value")
                    break
            
            if not adapters or not isinstance(adapters, list):
                continue
                
            for adapter in adapters:
                new_port = port.copy()
                new_port["name"] = f"{port['name']}_{adapter}"
                
                # Add adaptedFrom custom property
                if "customProperties" not in new_port:
                    new_port["customProperties"] = []
                else:
                    # Avoid recursive expansion
                    new_port["customProperties"] = [cp for cp in new_port["customProperties"] if cp.get("property") != "portAdapters"]
                
                new_port["customProperties"].append({
                    "property": "adaptedFrom",
                    "value": port["name"]
                })
                
                spec["outputPorts"].append(new_port)

    def _enrich_output_ports(self, spec: dict[str, Any]) -> None:
        """Populate missing fields in output ports."""
        if not self.enrich_output_ports:
            return
            
        if "outputPorts" not in spec or not isinstance(spec["outputPorts"], list):
            return
            
        # Predict contract ID
        predicted_dc_id = None
        if self.single_data_contract_per_product:
            # Use dataProduct key for name as expected by default ID generator for contracts
            # Note: version is no longer part of DC ID calculation
            id_spec = {
                "domain": spec.get("domain", ""),
                "dataProduct": spec.get("name", ""),
                "_dc_index": 0
            }
            predicted_dc_id = self.id_generator.make_dc_id(id_spec)
            
        for port in spec["outputPorts"]:
            if not isinstance(port, dict): continue
            
            # Default version to "v1" if missing
            if "version" not in port:
                port["version"] = "v1"
                
            # contractId enrichment
            if predicted_dc_id and "contractId" not in port:
                port["contractId"] = predicted_dc_id

    def _prepare_dc_spec(self, spec: dict[str, Any], dc_id: str, dp_spec: Optional[dict] = None) -> dict[str, Any]:
        """Enrich and validate data contract specification."""
        try:
            enriched_dc = enrich_dc_spec(
                {**spec, "id": dc_id}, 
                dp_spec=dp_spec,
                status_default=self.data_contract_status_default
            )
            validate_spec(enriched_dc)
            return enriched_dc
        except jsonschema.exceptions.ValidationError as e:
            raise DataContractValidationError(f"Invalid Data Contract specification: {e.message}") from e

    def _apply_patch(self, current_spec: dict, patch_spec: dict) -> dict:
        """Apply patch to specification, merging customProperties."""
        updated = current_spec.copy()
        for key, value in patch_spec.items():
            if key == "customProperties" and key in updated:
                updated[key] = updated[key] + value
            else:
                updated[key] = value
        return updated

    async def _create_data_product(
        self, 
        enriched_spec: dict[str, Any], 
        include_metadata: bool = False
    ) -> Union[dict, DataProduct]:
        dp = DataProduct(id=enriched_spec["id"], specification=enriched_spec)
        await self.dp_repo.save(dp)
        return dp if include_metadata else dp.specification

    async def get_data_product(self, id: str, include_metadata: bool = False) -> Optional[Union[dict, DataProduct]]:
        try:
            dp = await self.dp_repo.get(id)
            if dp:
                return dp if include_metadata else dp.specification
            return None
        except (ValueError, AttributeError):
            return None

    async def list_data_products(self, domain: str = None, name: str = None, include_metadata: bool = False) -> List[Union[dict, DataProduct]]:
        results = await self.dp_repo.list(domain=domain, name=name)
        if include_metadata:
            return results
        return [dp.specification for dp in results]

    async def _update_data_product(self, id: str, enriched_spec: dict[str, Any], include_metadata: bool = False) -> Union[dict, DataProduct]:
        dp = DataProduct(id=id, specification=enriched_spec)
        await self.dp_repo.save(dp)
        return dp if include_metadata else dp.specification

    async def delete_data_product(self, id: str) -> bool:
        try:
            return await self.dp_repo.delete(id)
        except ValueError:
            return False

    async def enrich_data_product_spec(self, spec: dict[str, Any], validate: bool = False) -> dict[str, Any]:
        """Enrich data product spec with defaults and ID. Does not save to repo."""
        return self._prepare_dp_spec(spec, validate=validate)

    async def enrich_data_contract_spec(self, spec: dict[str, Any], dp_id: Optional[str] = None) -> dict[str, Any]:
        """Enrich data contract spec with defaults and ID. Does not save to repo."""
        return await self.enrich_data_contract(spec, dp_id=dp_id)

    async def enrich_data_contract(
        self, 
        spec: Optional[dict[str, Any]] = None, 
        dp_id: Optional[str] = None, 
        dp_spec: Optional[dict] = None
    ) -> dict[str, Any]:
        """Enrich a Data Contract specification. Does NOT save to repo."""
        merged_spec = copy.deepcopy(spec) if spec else {}
        
        # 1. Resolve parent DP context
        if not dp_spec and dp_id:
            dp = await self.get_data_product(dp_id, include_metadata=True)
            if not dp:
                raise ValueError(f"Parent Data Product {dp_id} not found")
            dp_spec = dp.specification

        # 2. Determine ID (must know index)
        # We need to know if we are in single mode or not
        if self.single_data_contract_per_product:
            dc_index = 0
        else:
            # Determine existing count for this DP
            target_dp_id = dp_id or (dp_spec.get("id") if dp_spec else None)
            if target_dp_id:
                existing_dcs = await self.dc_repo.list(dp_id=target_dp_id)
                dc_index = len(existing_dcs)
            else:
                dc_index = 0
            
        id_spec = {
            **merged_spec, 
            "domain": dp_spec.get("domain", "") if dp_spec else "", 
            "dataProduct": dp_spec.get("name", "") if dp_spec else "", 
            "version": dp_spec.get("version", "v1.0.0") if dp_spec else "v1.0.0",
            "_dc_index": dc_index
        }
        dc_id = self.id_generator.make_dc_id(id_spec)
        
        return self._prepare_dc_spec(merged_spec, dc_id, dp_spec=dp_spec)

    async def put_data_product(
        self, 
        spec: dict[str, Any], 
        domain: Optional[str] = None, 
        name: Optional[str] = None, 
        include_metadata: bool = False
    ) -> Union[dict, DataProduct]:
        merged_spec = {**spec}
        if domain: merged_spec["domain"] = domain
        if name: merged_spec["name"] = name
        
        enriched = self._prepare_dp_spec(merged_spec)
        dp_id = enriched["id"]
        
        existing = await self.get_data_product(dp_id, include_metadata=True)
        if existing:
            if existing.specification == enriched:
                return existing if include_metadata else existing.specification
            return await self._update_data_product(dp_id, enriched, include_metadata=include_metadata)
        else:
            return await self._create_data_product(enriched, include_metadata=include_metadata)

    async def patch_data_product(self, spec: dict[str, Any], id: Optional[str] = None, include_metadata: bool = False) -> Union[dict, DataProduct]:
        id = id or spec.get("id")
        if not id:
            # Try to derive ID if domain/name are provided in spec
            if spec.get("domain") and spec.get("name"):
                id = self.id_generator.make_dp_id(spec)
            else:
                raise ValueError("id must be provided or present in spec for patch")
            
        existing = await self.get_data_product(id, include_metadata=True)
        if not existing:
            raise ValueError(f"Data product {id} not found")
        
        updated_spec = self._apply_patch(existing.specification, spec)
        # We use put_data_product to ensure full enrichment/validation of the patched spec
        return await self.put_data_product(updated_spec, include_metadata=include_metadata)

    async def _create_data_contract(
        self, 
        dp_id: str, 
        spec: dict[str, Any], 
        include_metadata: bool = False
    ) -> Union[dict, DataContract]:
        dp = await self.get_data_product(dp_id, include_metadata=True)
        if not dp:
            raise ValueError(f"Parent Data Product {dp_id} not found")

        if self.single_data_contract_per_product:
            dc_index = 0
        else:
            existing_dcs = await self.dc_repo.list(dp_id=dp_id)
            dc_index = len(existing_dcs)
            
        # Generate ID based on spec (including parent context)
        id_spec = {
            **spec, 
            "domain": dp.domain, 
            "dataProduct": dp.name, 
            "version": dp.version,
            "_dc_index": dc_index
        }
        dc_id = self.id_generator.make_dc_id(id_spec)
        
        enriched_dc = self._prepare_dc_spec(spec, dc_id, dp_spec=dp.specification)
        dc = DataContract(id=dc_id, data_product_id=dp_id, specification=enriched_dc)
        await self.dc_repo.save(dc)
        return dc if include_metadata else dc.specification

    async def get_data_contract(self, id: str, include_metadata: bool = False) -> Optional[Union[dict, DataContract]]:
        try:
            dc = await self.dc_repo.get(id)
            if dc:
                return dc if include_metadata else dc.specification
            return None
        except (ValueError, AttributeError):
            return None

    async def list_data_contracts(self, dp_id: str = None, include_metadata: bool = False) -> List[Union[dict, DataContract]]:
        results = await self.dc_repo.list(dp_id=dp_id)
        if include_metadata:
            return results
        return [dc.specification for dc in results]

    async def _update_data_contract(self, id: str, spec: dict[str, Any], include_metadata: bool = False) -> Union[dict, DataContract]:
        existing = await self.get_data_contract(id, include_metadata=True)
        if not existing:
            raise ValueError(f"Data contract {id} not found")
            
        dp = await self.get_data_product(existing.data_product_id, include_metadata=True)
        dp_spec = dp.specification if dp else None
        
        enriched_dc = self._prepare_dc_spec(spec, id, dp_spec=dp_spec)
        dc = DataContract(id=id, data_product_id=existing.data_product_id, specification=enriched_dc)
        await self.dc_repo.save(dc)
        return dc if include_metadata else dc.specification

    async def patch_data_contract(self, spec: dict[str, Any], id: Optional[str] = None, include_metadata: bool = False) -> Union[dict, DataContract]:
        id = id or spec.get("id")
        if not id:
            raise ValueError("id must be provided or present in spec for patch")
            
        existing = await self.get_data_contract(id, include_metadata=True)
        if not existing:
            raise ValueError(f"Data contract {id} not found")
        
        updated_spec = self._apply_patch(existing.specification, spec)
        return await self._update_data_contract(id, updated_spec, include_metadata=include_metadata)

    async def put_data_contract(
        self, 
        spec: dict[str, Any], 
        dp_id: Optional[str] = None, 
        include_metadata: bool = False
    ) -> Union[dict, DataContract]:
        id = spec.get("id")
        
        # Resolve parent DP if we need it for ID or enrichment
        dp = None
        if dp_id:
            dp = await self.get_data_product(dp_id, include_metadata=True)
            if not dp:
                raise ValueError(f"Parent Data Product {dp_id} not found")

        # If no ID is provided but we are in single mode, we can determine what the ID should be
        if not id and dp and self.single_data_contract_per_product:
            id = self.id_generator.make_dc_id({
                **spec, 
                "domain": dp.domain, 
                "dataProduct": dp.name, 
                "version": dp.version,
                "_dc_index": 0
            })

        existing = await self.get_data_contract(id, include_metadata=True) if id else None
        
        if existing:
            # For enrichment, use the DP associated with the existing contract if parent not provided
            if not dp:
                dp = await self.get_data_product(existing.data_product_id, include_metadata=True)
            
            # Check for changes
            enriched = self._prepare_dc_spec(spec, id, dp_spec=dp.specification if dp else None)
            if existing.specification == enriched:
                return existing if include_metadata else existing.specification
            return await self._update_data_contract(id, spec, include_metadata=include_metadata)
        else:
            if not dp_id:
                raise ValueError("dp_id is required to create a new data contract")
            return await self._create_data_contract(dp_id, spec, include_metadata=include_metadata)

    async def delete_data_contract(self, id: str) -> bool:
        try:
            return await self.dc_repo.delete(id)
        except ValueError:
            return False

    async def discover(
        self,
        dp_id: Optional[str] = None,
        domain: Optional[str] = None,
        name: Optional[str] = None,
        include_metadata: bool = False
    ) -> List[Union[dict, DataProduct, DataContract]]:
        results = []
        dps = []
        
        if dp_id:
            dp = await self.dp_repo.get(dp_id)
            if dp: dps.append(dp)
        elif domain and name:
            dps = await self.dp_repo.list(domain=domain, name=name)
        elif domain:
            dps = await self.dp_repo.list(domain=domain)
        else:
            dps = await self.dp_repo.list()
        
        # Keep track of DPs for expansion (id -> domain)
        dp_map = {dp.id: dp.domain for dp in dps}
        
        # Collect all contracts and products to check for agreements
        to_check = [] # List of (spec, parent_dp_id, parent_dp_domain)
        
        for dp in dps:
            results.append(dp if include_metadata else dp.specification)
            to_check.append((dp.specification, dp.id, dp.domain))
            
            dcs = await self.dc_repo.list(dp_id=dp.id)
            if include_metadata:
                results.extend(dcs)
            else:
                results.extend([dc.specification for dc in dcs])
            
            for dc in dcs:
                to_check.append((dc.specification, dp.id, dp.domain))

        # Expansion logic for Data Usage Agreements
        expanded_duas = []
        for spec, parent_id, parent_domain in to_check:
            custom_props = spec.get("customProperties", [])
            for prop in custom_props:
                if prop.get("property") == "dataUsageAgreements":
                    agreements = prop.get("value", [])
                    for ag in agreements:
                        consumer_id = ag.get("consumer", {}).get("dataProductId")
                        
                        # Resolve consumer domain
                        consumer_domain = dp_map.get(consumer_id)
                        if not consumer_domain and consumer_id:
                            cons_dp = await self.get_data_product(consumer_id)
                            if cons_dp:
                                consumer_domain = cons_dp.get("domain")
                                dp_map[consumer_id] = consumer_domain

                        dua = {
                            "dataUsageAgreementSpecification": "0.0.1",
                            "info": {
                                "active": True,
                                "status": "approved",
                                "startDate": self.dua_start_date_default,
                                "purpose": self.dua_purpose_default,
                                **ag.get("info", {})
                            },
                            "provider": {
                                "teamId": parent_domain,
                                "outputPortId": "*",
                                "dataProductId": parent_id
                            },
                            "consumer": {
                                "teamId": consumer_domain,
                                "dataProductId": consumer_id
                            }
                        }
                        dua["id"] = self.id_generator.make_dua_id(dua)
                        expanded_duas.append(dua)
        
        results.extend(expanded_duas)
        return results

    async def flush(self) -> None:
        if hasattr(self.dp_repo, "flush") and callable(getattr(self.dp_repo, "flush")):
            await self.dp_repo.flush()

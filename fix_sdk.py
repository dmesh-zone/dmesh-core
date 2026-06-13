import re

with open("/Users/joao/code/dmesh-core/packages/dmesh-sdk/src/dmesh/sdk/sdk.py", "r") as f:
    content = f.read()

# Fix 273: dp_id type hint
content = content.replace("dp_id: Optional[str] = None", "dp_id: Optional[Union[str, UUID]] = None")

# Fix 331: Object of class `dict` has no attribute `specification`
content = content.replace(
    "res = existing if include_metadata else existing.specification",
    "res = existing if include_metadata else (existing.specification if isinstance(existing, DataProduct) else existing)"
)

# Fix 338: Argument dp_spec
content = content.replace(
    "await self._auto_create_data_source_dp(res if not include_metadata else res.specification if isinstance(res, DataProduct) else res.get('specification', res))",
    "await self._auto_create_data_source_dp(res.specification if isinstance(res, DataProduct) else res)"
)

# Fix 383: patch_data_product signature
content = content.replace(
    "async def patch_data_product(self, spec: dict[str, Any], id: Optional[str] = None, include_metadata: bool = False, enrich: bool = True, validate: bool = True) -> Union[dict, DataProduct]:",
    "async def patch_data_product(self, spec: dict[str, Any], id: Optional[Union[str, UUID]] = None, include_metadata: bool = False, enrich: bool = True, validate: bool = True) -> Union[dict, DataProduct]:"
)

# Fix 395: get_data_product id
# It's inside patch_data_product. We can change `id = id or spec.get("id")` to `id_val = id or spec.get("id")`
patch_dp = '''    async def patch_data_product(self, spec: dict[str, Any], id: Optional[Union[str, UUID]] = None, include_metadata: bool = False, enrich: bool = True, validate: bool = True) -> Union[dict, DataProduct]:
        id_val = id or spec.get("id")
        if id_val and isinstance(id_val, str):
            id_val = UUID(id_val)
            
        if not id_val:
            # Try to derive ID if domain/name are provided in spec
            if spec.get("domain") and spec.get("name"):
                id_val = self.id_generator.make_dp_id(spec)
            else:
                raise ValueError("id must be provided or present in spec for patch")
            
        existing = await self.get_data_product(id_val, include_metadata=True)
        if not existing:
            raise ValueError(f"Data product {id_val} not found")
        
        updated_spec = self._apply_patch(existing.specification if isinstance(existing, DataProduct) else existing, spec)
        # We use put_data_product to ensure full enrichment/validation of the patched spec
        return await self.put_data_product(updated_spec, include_metadata=include_metadata, enrich=enrich, validate=validate)'''

# We need to replace the body of patch_data_product
# Let's just use re.sub for patch_data_product
content = re.sub(
    r'async def patch_data_product.*?return await self.put_data_product\(updated_spec, include_metadata=include_metadata, enrich=enrich, validate=validate\)',
    patch_dp,
    content,
    flags=re.DOTALL
)

# Fix 432: _create_data_contract dp.id
create_dc = '''    async def _create_data_contract(
        self, 
        dp_id: Union[str, UUID], 
        spec: dict[str, Any], 
        include_metadata: bool = False
    ) -> Union[dict, DataContract]:
        if isinstance(dp_id, str):
            dp_id = UUID(dp_id)
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
            "domain": dp.domain if isinstance(dp, DataProduct) else dp.get('domain', ''), 
            "dataProduct": dp.name if isinstance(dp, DataProduct) else dp.get('name', ''), 
            "version": dp.version if isinstance(dp, DataProduct) else dp.get('version', 'v1.0.0'),
            "_dc_index": dc_index
        }
        dc_id = self.id_generator.make_dc_id(id_spec)
        
        enriched_dc = self._prepare_dc_spec(spec, dc_id, dp_spec=dp.specification if isinstance(dp, DataProduct) else dp)
        extracted_dp_id = dp.id if isinstance(dp, DataProduct) else dp.get('id')
        parsed_dp_id = UUID(extracted_dp_id) if isinstance(extracted_dp_id, str) else extracted_dp_id
        dc = DataContract(id=dc_id, data_product_id=parsed_dp_id, specification=enriched_dc)
        await self.dc_repo.save(dc)
        return dc if include_metadata else dc.specification'''

content = re.sub(
    r'async def _create_data_contract.*?return dc if include_metadata else dc.specification',
    create_dc,
    content,
    flags=re.DOTALL
)

# Fix 447: list_data_contracts dp_id
content = content.replace(
    "async def list_data_contracts(self, dp_id: Union[str, UUID] = None, include_metadata: bool = False) -> List[Union[dict, DataContract]]:",
    "async def list_data_contracts(self, dp_id: Optional[Union[str, UUID]] = None, include_metadata: bool = False) -> List[Union[dict, DataContract]]:"
)

# Fix 460, 464: _update_data_contract
update_dc = '''    async def _update_data_contract(self, id: Union[str, UUID], spec: dict[str, Any], include_metadata: bool = False) -> Union[dict, DataContract]:
        if isinstance(id, str):
            id = UUID(id)
        existing = await self.get_data_contract(str(id), include_metadata=True)
        if not existing:
            raise ValueError(f"Data contract {id} not found")
            
        existing_dp_id = existing.data_product_id if isinstance(existing, DataContract) else existing.get('data_product_id')
        parsed_existing_dp_id = UUID(existing_dp_id) if isinstance(existing_dp_id, str) else existing_dp_id
        dp = await self.get_data_product(parsed_existing_dp_id, include_metadata=True) if parsed_existing_dp_id else None
        dp_spec = dp.specification if isinstance(dp, DataProduct) else (dp.get('specification', dp) if dp else None)
        
        enriched_dc = self._prepare_dc_spec(spec, id, dp_spec=dp_spec)
        dc = DataContract(id=id, data_product_id=parsed_existing_dp_id, specification=enriched_dc)
        await self.dc_repo.save(dc)
        return dc if include_metadata else dc.specification'''

content = re.sub(
    r'async def _update_data_contract.*?return dc if include_metadata else dc.specification',
    update_dc,
    content,
    flags=re.DOTALL
)

# Fix 471: patch_data_contract
patch_dc = '''    async def patch_data_contract(self, spec: dict[str, Any], id: Optional[Union[str, UUID]] = None, include_metadata: bool = False) -> Union[dict, DataContract]:
        actual_id = id or spec.get("id")
        if actual_id and isinstance(actual_id, str):
            actual_id = UUID(actual_id)
            
        if not actual_id:
            raise ValueError("id must be provided or present in spec for patch")
            
        existing = await self.get_data_contract(actual_id, include_metadata=True)
        if not existing:
            raise ValueError(f"Data contract {actual_id} not found")
        
        updated_spec = self._apply_patch(existing.specification if isinstance(existing, DataContract) else existing, spec)
        return await self._update_data_contract(actual_id, updated_spec, include_metadata=include_metadata)'''

content = re.sub(
    r'async def patch_data_contract\(self, spec: dict\[str, Any\].*?return await self._update_data_contract\(.*?include_metadata=include_metadata\)',
    patch_dc,
    content,
    flags=re.DOTALL
)

# Fix 494: put_data_contract dp_id
put_dc = '''    async def put_data_contract(
        self, 
        spec: dict[str, Any], 
        dp_id: Optional[Union[str, UUID]] = None, 
        include_metadata: bool = False
    ) -> Union[dict, DataContract]:
        actual_id = spec.get("id")
        if actual_id and isinstance(actual_id, str):
            actual_id = UUID(actual_id)
            
        actual_dp_id = dp_id
        if actual_dp_id and isinstance(actual_dp_id, str):
            actual_dp_id = UUID(actual_dp_id)
        
        # Resolve parent DP if we need it for ID or enrichment
        dp = None
        if actual_dp_id:
            dp = await self.get_data_product(actual_dp_id, include_metadata=True)
            if not dp:
                raise ValueError(f"Parent Data Product {actual_dp_id} not found")

        # If no ID is provided but we are in single mode, we can determine what the ID should be
        if not actual_id and dp and self.single_data_contract_per_product:
            actual_id = self.id_generator.make_dc_id({
                **spec, 
                "domain": dp.domain if isinstance(dp, DataProduct) else dp.get('domain', ''), 
                "dataProduct": dp.name if isinstance(dp, DataProduct) else dp.get('name', ''), 
                "version": dp.version if isinstance(dp, DataProduct) else dp.get('version', 'v1.0.0'),
                "_dc_index": 0
            })

        existing = await self.get_data_contract(actual_id, include_metadata=True) if actual_id else None
        
        if existing:
            # For enrichment, use the DP associated with the existing contract if parent not provided
            if not dp:
                existing_dp_id = existing.data_product_id if isinstance(existing, DataContract) else existing.get('data_product_id')
                parsed_existing_dp_id = UUID(existing_dp_id) if isinstance(existing_dp_id, str) else existing_dp_id
                dp = await self.get_data_product(parsed_existing_dp_id, include_metadata=True) if parsed_existing_dp_id else None
            
            # Check for changes
            enriched = self._prepare_dc_spec(spec, actual_id, dp_spec=dp.specification if isinstance(dp, DataProduct) else dp if dp else None)
            if (existing.specification if isinstance(existing, DataContract) else existing) == enriched:
                return existing if include_metadata else (existing.specification if isinstance(existing, DataContract) else existing)
            return await self._update_data_contract(actual_id, spec, include_metadata=include_metadata)
        else:
            if not actual_dp_id:
                raise ValueError("dp_id is required to create a new data contract")
            return await self._create_data_contract(actual_dp_id, spec, include_metadata=include_metadata)'''

content = re.sub(
    r'async def put_data_contract\(.*?return await self._create_data_contract\(dp_id, spec, include_metadata=include_metadata\)',
    put_dc,
    content,
    flags=re.DOTALL
)

# Fix 539: discover dp_id
content = content.replace(
    "async def discover(\n        self,\n        dp_id: Optional[str] = None,",
    "async def discover(\n        self,\n        dp_id: Optional[Union[str, UUID]] = None,"
)

with open("/Users/joao/code/dmesh-core/packages/dmesh-sdk/src/dmesh/sdk/sdk.py", "w") as f:
    f.write(content)

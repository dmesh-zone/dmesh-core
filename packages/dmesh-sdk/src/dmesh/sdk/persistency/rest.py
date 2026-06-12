from anyio import lowlevel
import httpx
from typing import List, Optional, Any
from uuid import UUID
from datetime import datetime
import json
import dataclasses

from dmesh.sdk.models import DataProduct, DataContract
from dmesh.sdk.ports.repository import DataProductRepository, DataContractRepository

def _parse_datetime(dt_str: Optional[str]) -> Optional[datetime]:
    if not dt_str:
        return None
    try:
        return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    except Exception:
        return None

def _parse_uuid(val: Any) -> UUID:
    if isinstance(val, UUID):
        return val
    if isinstance(val, str):
        return UUID(val)
    raise ValueError(f"Cannot parse UUID from {val}")

class AsyncHttpDataProductRepository:
    def __init__(self, api_url: str, use_m2m: bool = False, ssl_verify: bool = False):
        self.api_url = api_url.rstrip("/")
        self.use_m2m = use_m2m
        self._dbx_config = None
        
        # Use a single shared client, increasing connection limits.
        limits = httpx.Limits(max_keepalive_connections=20, max_connections=100)
        self._client = httpx.AsyncClient(limits=limits, verify=ssl_verify)
        
        if self.use_m2m:
            from databricks.sdk.core import Config
            self._dbx_config = Config()

    def _get_headers(self) -> dict:
        headers = {"Accept": "application/json"}
        if self.use_m2m and self._dbx_config:
            auth_headers = self._dbx_config.authenticate()
            if callable(auth_headers):
                auth_headers = auth_headers()
            if isinstance(auth_headers, dict):
                headers.update(auth_headers)

        return headers

    def _to_dp(self, data: dict) -> DataProduct:
        if "specification" in data:
            return DataProduct(
                id=_parse_uuid(data.get("id")),
                specification=data["specification"],
                created_at=_parse_datetime(data.get("created_at")),
                updated_at=_parse_datetime(data.get("updated_at")),
            )
        else:
            return DataProduct(
                id=_parse_uuid(data.get("id")),
                specification=data
            )

    async def get(self, id: UUID) -> Optional[DataProduct]:
        response = await self._client.get(f"{self.api_url}/dps/{id}?include_metadata=true", headers=self._get_headers())
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return self._to_dp(response.json())

    async def save(self, product: DataProduct) -> None:
        class APIEncoder(json.JSONEncoder):
            def default(self, o):
                if isinstance(o, (UUID, datetime)):
                    return str(o)
                return super().default(o)

        payload = json.loads(json.dumps(dataclasses.asdict(product), cls=APIEncoder))
        
        response = await self._client.put(
            f"{self.api_url}/dps/{product.id}",
            json=payload,
            headers=self._get_headers()
        )
        response.raise_for_status()
        
        data = response.json()
        if data.get("created_at"):
            product.created_at = _parse_datetime(data["created_at"])
        if data.get("updated_at"):
            product.updated_at = _parse_datetime(data["updated_at"])

    async def list(self, domain: Optional[str] = None, name: Optional[str] = None) -> List[DataProduct]:
        params = {"include_metadata": "true"}
        if domain:
            params["domain"] = domain
        if name:
            params["name"] = name
            
        response = await self._client.get(f"{self.api_url}/dps", params=params, headers=self._get_headers())
        response.raise_for_status()
        data = response.json()
        return [self._to_dp(item) for item in data]

    async def delete(self, id: UUID) -> bool:
        response = await self._client.delete(f"{self.api_url}/dps/{id}", headers=self._get_headers())
        if response.status_code == 404:
            return False
        response.raise_for_status()
        return True

    async def truncate(self) -> None:
        response = await self._client.delete(f"{self.api_url}/admin/truncate_dps", headers=self._get_headers())
        response.raise_for_status()


class AsyncHttpDataContractRepository:
    def __init__(self, api_url: str, use_m2m: bool = False, ssl_verify: bool = False):
        self.api_url = api_url.rstrip("/")
        self.use_m2m = use_m2m
        self._dbx_config = None
        
        # Use a single shared client, increasing connection limits.
        limits = httpx.Limits(max_keepalive_connections=20, max_connections=100)
        self._client = httpx.AsyncClient(limits=limits, verify=ssl_verify)
        
        if self.use_m2m:
            from databricks.sdk.core import Config
            self._dbx_config = Config()

    def _get_headers(self) -> dict:
        headers = {"Accept": "application/json"}
        if self.use_m2m and self._dbx_config:
            auth_headers = self._dbx_config.authenticate()
            if callable(auth_headers):
                auth_headers = auth_headers()
            if isinstance(auth_headers, dict):
                headers.update(auth_headers)
        return headers

    def _to_dc(self, data: dict) -> DataContract:
        if "specification" in data:
            return DataContract(
                id=_parse_uuid(data.get("id")),
                data_product_id=_parse_uuid(data.get("data_product_id") or data.get("dataProductId")),
                specification=data["specification"],
                created_at=_parse_datetime(data.get("created_at")),
                updated_at=_parse_datetime(data.get("updated_at")),
            )
        else:
            return DataContract(
                id=_parse_uuid(data.get("id")),
                data_product_id=_parse_uuid(data.get("dataProductId") or data.get("data_product_id")),
                specification=data
            )

    async def get(self, id: UUID) -> Optional[DataContract]:
        response = await self._client.get(f"{self.api_url}/dcs/{id}?include_metadata=true", headers=self._get_headers())
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return self._to_dc(response.json())

    async def save(self, contract: DataContract) -> None:
        class APIEncoder(json.JSONEncoder):
            def default(self, o):
                if isinstance(o, (UUID, datetime)):
                    return str(o)
                return super().default(o)

        payload = json.loads(json.dumps(dataclasses.asdict(contract), cls=APIEncoder))
        
        response = await self._client.put(
            f"{self.api_url}/dcs/{contract.id}",
            json=payload,
            headers=self._get_headers()
        )
        response.raise_for_status()
        
        data = response.json()
        if data.get("created_at"):
            contract.created_at = _parse_datetime(data["created_at"])
        if data.get("updated_at"):
            contract.updated_at = _parse_datetime(data["updated_at"])

    async def list(self, dp_id: Optional[UUID] = None) -> List[DataContract]:
        params = {"include_metadata": "true"}
        if dp_id:
            params["dp_id"] = str(dp_id)
            
        response = await self._client.get(f"{self.api_url}/dcs", params=params, headers=self._get_headers())
        response.raise_for_status()
        data = response.json()
        return [self._to_dc(item) for item in data]

    async def delete(self, id: UUID) -> bool:
        response = await self._client.delete(f"{self.api_url}/dcs/{id}", headers=self._get_headers())
        if response.status_code == 404:
            return False
        response.raise_for_status()
        return True

    async def truncate(self) -> None:
        response = await self._client.delete(f"{self.api_url}/admin/truncate_dcs", headers=self._get_headers())
        response.raise_for_status()


class HttpRepositoryFactory:
    def __init__(self, api_url: str, use_m2m: bool = False, ssl_verify: bool = False):
        self._dp_repo = AsyncHttpDataProductRepository(api_url, use_m2m=use_m2m, ssl_verify=ssl_verify)
        self._dc_repo = AsyncHttpDataContractRepository(api_url, use_m2m=use_m2m, ssl_verify=ssl_verify)

    def get_data_product_repository(self) -> DataProductRepository:
        return self._dp_repo

    def get_data_contract_repository(self) -> DataContractRepository:
        return self._dc_repo

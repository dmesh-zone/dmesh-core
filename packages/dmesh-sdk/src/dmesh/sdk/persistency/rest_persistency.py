import httpx
from typing import List, Optional
from uuid import UUID
from datetime import datetime
import json
import dataclasses

from dmesh.sdk.models import DataProduct, DataContract
from dmesh.sdk.ports.repository import DataProductRepository, DataContractRepository

def _parse_datetime(dt_str: Optional[str]) -> Optional[datetime]:
    if not dt_str:
        return None
    # Assuming ISO format with potential Z at the end
    try:
        return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    except Exception:
        return None

class AsyncHttpDataProductRepository:
    def __init__(self, api_url: str):
        self.api_url = api_url.rstrip("/")

    def _to_dp(self, data: dict) -> DataProduct:
        if "specification" in data:
            return DataProduct(
                id=UUID(data["id"]) if isinstance(data["id"], str) else data["id"],
                specification=data["specification"],
                created_at=_parse_datetime(data.get("created_at")),
                updated_at=_parse_datetime(data.get("updated_at")),
            )
        else:
            dp_id = data.get("id")
            return DataProduct(
                id=UUID(dp_id) if isinstance(dp_id, str) else dp_id,
                specification=data
            )

    async def get(self, id: UUID) -> Optional[DataProduct]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.api_url}/dps/{id}?include_metadata=true")
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return self._to_dp(response.json())

    async def save(self, product: DataProduct) -> None:
        async with httpx.AsyncClient() as client:
            # We must serialize the UUIDs and Datetimes 
            class APIEncoder(json.JSONEncoder):
                def default(self, obj):
                    if isinstance(obj, (UUID, datetime)):
                        return str(obj)
                    return super().default(obj)

            payload = json.loads(json.dumps(dataclasses.asdict(product), cls=APIEncoder))
            
            response = await client.put(
                f"{self.api_url}/dps/{product.id}",
                json=payload
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
            
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.api_url}/dps", params=params)
            response.raise_for_status()
            data = response.json()
            return [self._to_dp(item) for item in data]

    async def delete(self, id: UUID) -> bool:
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{self.api_url}/dps/{id}")
            if response.status_code == 404:
                return False
            response.raise_for_status()
            return True

    async def truncate(self) -> None:
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{self.api_url}/admin/truncate_dps")
            response.raise_for_status()


class AsyncHttpDataContractRepository:
    def __init__(self, api_url: str):
        self.api_url = api_url.rstrip("/")

    def _to_dc(self, data: dict) -> DataContract:
        if "specification" in data:
            return DataContract(
                id=UUID(data["id"]) if isinstance(data["id"], str) else data["id"],
                data_product_id=UUID(data["data_product_id"]) if isinstance(data.get("data_product_id"), str) else data.get("data_product_id"),
                specification=data["specification"],
                created_at=_parse_datetime(data.get("created_at")),
                updated_at=_parse_datetime(data.get("updated_at")),
            )
        else:
            dc_id = data.get("id")
            dp_id = data.get("dataProductId") or data.get("data_product_id")
            return DataContract(
                id=UUID(dc_id) if isinstance(dc_id, str) else dc_id,
                data_product_id=UUID(dp_id) if isinstance(dp_id, str) else dp_id,
                specification=data
            )

    async def get(self, id: UUID) -> Optional[DataContract]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.api_url}/dcs/{id}?include_metadata=true")
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return self._to_dc(response.json())

    async def save(self, contract: DataContract) -> None:
        async with httpx.AsyncClient() as client:
            class APIEncoder(json.JSONEncoder):
                def default(self, obj):
                    if isinstance(obj, (UUID, datetime)):
                        return str(obj)
                    return super().default(obj)

            payload = json.loads(json.dumps(dataclasses.asdict(contract), cls=APIEncoder))
            
            response = await client.put(
                f"{self.api_url}/dcs/{contract.id}",
                json=payload
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
            
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.api_url}/dcs", params=params)
            response.raise_for_status()
            data = response.json()
            return [self._to_dc(item) for item in data]

    async def delete(self, id: UUID) -> bool:
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{self.api_url}/dcs/{id}")
            if response.status_code == 404:
                return False
            response.raise_for_status()
            return True

    async def truncate(self) -> None:
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{self.api_url}/admin/truncate_dcs")
            response.raise_for_status()


class HttpRepositoryFactory:
    def __init__(self, api_url: str):
        self._dp_repo = AsyncHttpDataProductRepository(api_url)
        self._dc_repo = AsyncHttpDataContractRepository(api_url)

    def get_data_product_repository(self) -> DataProductRepository:
        return self._dp_repo

    def get_data_contract_repository(self) -> DataContractRepository:
        return self._dc_repo

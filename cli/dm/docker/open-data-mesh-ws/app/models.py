from uuid import UUID
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict


class OdpsSpec(BaseModel):
    model_config = ConfigDict(extra="allow")

    apiVersion: str
    kind: str = "DataProduct"
    domain: str
    name: str
    version: str = "v1.0.0"


class OdcsSpec(BaseModel):
    model_config = ConfigDict(extra="allow")

    apiVersion: str = "v3.1.0"
    kind: str = "DataContract"
    status: str = "draft"


class DataProductCreate(BaseModel):
    specification: Optional[dict[str, Any]] = None


# GET /data-products/{id} — full record with DB metadata
class DataProductResponse(BaseModel):
    id: UUID
    specification: Optional[dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime


class DataContractCreate(BaseModel):
    specification: Optional[dict[str, Any]] = None


class DataContractResponse(BaseModel):
    id: UUID
    data_product_id: UUID
    specification: Optional[dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

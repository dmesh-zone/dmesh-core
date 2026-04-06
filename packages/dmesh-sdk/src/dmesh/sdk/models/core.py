from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class DataProduct:
    id: str
    specification: Dict[str, Any]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @property
    def domain(self) -> str:
        return self.specification.get("domain", "")

    @property
    def name(self) -> str:
        return self.specification.get("name", "")

    @property
    def version(self) -> str:
        return self.specification.get("version", "v1.0.0")


@dataclass
class DataContract:
    id: str
    data_product_id: str
    specification: Dict[str, Any]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

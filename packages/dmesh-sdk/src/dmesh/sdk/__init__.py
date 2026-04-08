from .models import (
    DataProduct,
    DataContract,
    OpenDataMeshError,
    DataProductValidationError,
    DataContractValidationError,
)
from .operations.data_product import create_dp, update_dp, get_dp, list_dps, delete_dp
from .operations.data_contract import create_dc, update_dc, patch_dc, get_dc, list_dcs, delete_dc
from .operations.discover import discover
from .operations.utils import flush

# Legacy support
from .core.service import DMeshService
from .persistency.in_memory import InMemoryRepository

__all__ = [
    "DataProduct",
    "DataContract",
    "OpenDataMeshError",
    "DataProductValidationError",
    "DataContractValidationError",
    "create_dp",
    "update_dp",
    "get_dp",
    "list_dps",
    "delete_dp",
    "create_dc",
    "update_dc",
    "patch_dc",
    "get_dc",
    "list_dcs",
    "delete_dc",
    "discover",
    "flush",
    "DataMeshService",
    "InMemoryRepository",
]

from dmesh.sdk import (
    DataProduct,
    DataContract,
    OpenDataMeshError,
    DataProductValidationError,
    DataContractValidationError,
)
from datetime import datetime

def test_instantiate_data_product():
    dp = DataProduct(
        id="dp-123",
        specification={"domain": "sales", "name": "orders", "version": "v1.0.0"},
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    assert dp.id == "dp-123"
    assert dp.domain == "sales"
    assert dp.name == "orders"
    assert dp.version == "v1.0.0"

def test_instantiate_data_contract():
    dc = DataContract(
        id="dc-456",
        data_product_id="dp-123",
        specification={"schema": "orders.json"}
    )
    assert dc.id == "dc-456"
    assert dc.data_product_id == "dp-123"
    assert dc.specification["schema"] == "orders.json"

def test_exceptions_available():
    assert issubclass(DataProductValidationError, OpenDataMeshError)
    assert issubclass(DataContractValidationError, OpenDataMeshError)

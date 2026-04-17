from uuid import UUID
from datetime import datetime
from dmesh.sdk import (
    DataProduct,
    DataContract,
    OpenDataMeshError,
    DataProductValidationError,
    DataContractValidationError,
)

def test_instantiate_data_product():
    dp_id = UUID("00000000-0000-0000-0000-000000000001")
    dp = DataProduct(
        id=dp_id,
        specification={"domain": "sales", "name": "orders", "version": "v1.0.0"},
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    assert dp.id == dp_id
    assert dp.domain == "sales"
    assert dp.name == "orders"
    assert dp.version == "v1.0.0"

def test_instantiate_data_contract():
    dc_id = UUID("00000000-0000-0000-0000-000000000002")
    dp_id = UUID("00000000-0000-0000-0000-000000000001")
    dc = DataContract(
        id=dc_id,
        data_product_id=dp_id,
        specification={"schema": "orders.json"}
    )
    assert dc.id == dc_id
    assert dc.data_product_id == dp_id
    assert dc.specification["schema"] == "orders.json"

def test_exceptions_available():
    assert issubclass(DataProductValidationError, OpenDataMeshError)
    assert issubclass(DataContractValidationError, OpenDataMeshError)

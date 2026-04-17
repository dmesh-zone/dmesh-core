# DMesh Design Guidelines

## SDK API Guidelines (sdk.py)

The SDK provides both asynchronous (`AsyncSDK`) and synchronous (`SyncSDK`) implementations. Both MUST maintain consistent method signatures and behavior.

### Method Naming Strategy
- **Data Product Operations**: `[operation]_data_product`
- **Data Contract Operations**: `[operation]_data_contract`

### Standard Signatures

#### Data Products
- `put_data_product(spec: dict, domain: str = None, name: str = None, include_metadata: bool = False)`
- `get_data_product(id: str, include_metadata: bool = False)`
- `list_data_products(domain: str = None, name: str = None, include_metadata: bool = False)`
- `delete_data_product(id: str) -> bool`

#### Data Contracts
- `put_data_contract(spec: dict, dp_id: str = None, include_metadata: bool = False)`
- `patch_data_contract(id: str, spec: dict, include_metadata: bool = False)`
- `get_data_contract(id: str, include_metadata: bool = False)`
- `list_data_contracts(dp_id: str = None, include_metadata: bool = False)`
- `delete_data_contract(id: str) -> bool`

### Behavior Rules
1. **Metadata vs Specification**: By default (`include_metadata=False`), methods return the specification dictionary. If `include_metadata=True`, they return the full Model object (`DataProduct` or `DataContract`).
2. **Error Handling**:
   - Validation errors should raise `DataProductValidationError` or `DataContractValidationError`.
   - Resource not found during creation/update dependencies should raise `ValueError` with a descriptive message.
   - Malformed IDs should be handled gracefully (e.g., return `None` for `get`).
3. **Consistency**: Sync and Async versions of the same method must accept the exact same arguments and perform the exact same business logic (enriching, validating, ID generation).

## API Signatures (FastAPI Routers)

The API routers should map directly to the SDK operations.

### Data Products (`/dps`)
- `POST /dps`: Calls `sdk.create_data_product(spec)`
- `GET /dps`: Calls `sdk.list_data_products(domain, name)`
- `GET /dps/{id}`: Calls `sdk.get_data_product(id)`
- `DELETE /dps/{id}`: Calls `sdk.delete_data_product(id)`

### Data Contracts (`/dcs`)
- `POST /dps/{dp_id}/dcs`: Calls `sdk.create_data_contract(dp_id, spec)`
- `PATCH /dcs/{id}`: Calls `sdk.patch_data_contract(id, spec)`
- `GET /dcs/{id}`: Calls `sdk.get_data_contract(id)`
- `GET /dcs`: Calls `sdk.list_data_contracts(dp_id)`
- `DELETE /dcs/{id}`: Calls `sdk.delete_data_contract(id)`

### Discover (`/discover`)
- `GET /discover`: Calls `sdk.discover(domain, name)`

## OS Portabilty
This SDK is designed so that it can be developed and used in both Windows, Linux and Mac
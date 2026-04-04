class OpenDataMeshError(Exception):
    """Base class for all SDK errors."""
    pass

class DataProductValidationError(OpenDataMeshError):
    """Raised when a Data Product specification is invalid according to ODPS schema."""
    pass

class DataContractValidationError(OpenDataMeshError):
    """Raised when a Data Contract specification is invalid according to ODCS schema."""
    pass

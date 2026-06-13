"""dm validate command."""
import typer
import asyncio
import sys
from jsonschema.exceptions import ValidationError

from dmesh.sdk.config import get_settings
from dmesh.sdk.persistency.filesystem import AsyncFilesystemDataProductRepository
from dmesh.sdk.lean_validator.validator import Validator

def validate() -> None:
    """Validate all data products in the filesystem."""
    try:
        asyncio.run(_validate_dps())
    except typer.Exit:
        raise
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

async def _validate_dps():
    settings = get_settings()
    
    if getattr(settings.sdk, "filesystem_persistency", False) is False:
        typer.echo("Error: Validation is only supported when filesystem_persistency is enabled.", err=True)
        raise typer.Exit(code=1)
        
    root_dir = getattr(settings.sdk, "data_products_filesystem_root", None) or "tmp/data_products_filesystem_root"
    repo = AsyncFilesystemDataProductRepository(root_dir)
    dps = await repo.list()
    
    if not dps:
        typer.echo(f"No data products found in {root_dir}.")
        return

    schema_path = getattr(settings.sdk, "lean_validation_data_product_schema", None)
    custom_props_dir = getattr(settings.sdk, "lean_validation_custom_properties_path", None)
    
    kwargs = {}
    if schema_path:
        kwargs["schema_path"] = schema_path
    if custom_props_dir:
        kwargs["custom_properties_dir"] = custom_props_dir
        
    validator = Validator(**kwargs)
    
    errors = False
    
    for dp in dps:
        name = getattr(dp, "name", dp.specification.get("name", "Unknown"))
        try:
            validator.validate_data(dp.specification)
            typer.echo(f"✅ Validation successful for data product: {name}")
        except ValidationError as e:
            errors = True
            
            # Formatting similar to standalone validator
            path_list = list(e.absolute_path)
            is_custom_property = False
            
            if "customProperties" in path_list:
                idx = path_list.index("customProperties")
                if len(path_list) > idx + 1 and isinstance(path_list[idx + 1], int):
                    curr = dp.specification
                    try:
                        for p in path_list[:idx + 2]:
                            curr = curr[p]  # type: ignore
                        property_name = curr.get("property", "unknown")
                        
                        path_list[idx + 1] = property_name
                        json_path = " -> ".join(str(p) for p in path_list)
                        
                        if e.validator == "enum":
                            field_name = path_list[-1]
                            invalid_val = e.instance
                            if isinstance(e.validator_value, (list, tuple)):
                                supported_vals = ", ".join(str(v) for v in e.validator_value)
                            else:
                                supported_vals = str(e.validator_value)
                            msg = f"❌ ERROR: Specification for data product {name} customProperty {property_name} {field_name} has an invalid value ({invalid_val}) supported values are ({supported_vals}). Please correct: {json_path}"
                            typer.echo(msg, err=True)
                            is_custom_property = True
                        else:
                            msg = f"❌ ERROR: Specification for data product {name} customProperty {property_name} error: {e.message}. Please correct: {json_path}"
                            typer.echo(msg, err=True)
                            is_custom_property = True
                    except Exception:
                        pass
                        
            if not is_custom_property:
                typer.echo(f"❌ Validation failed for data product: {name}", err=True)
                typer.echo(f"   Message: {e.message}", err=True)
                typer.echo(f"   Path: {' -> '.join(str(p) for p in e.absolute_path)}", err=True)
                
    if errors:
        raise typer.Exit(code=1)

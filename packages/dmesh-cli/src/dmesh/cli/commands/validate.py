"""dm validate command."""
import typer
import asyncio
from typing import Optional

from dmesh.sdk.config import get_settings
from dmesh.sdk.persistency.filesystem import AsyncFilesystemDataProductRepository
from dmesh.sdk.operations.data_product import validate_dps

app = typer.Typer(help="Validation commands.")

@app.command("dps")
def validate_dps_cmd(
    root: Optional[str] = typer.Option(None, "--root", "-r", help="Data products filesystem root path."),
    schema: Optional[str] = typer.Option(None, "--schema", "-s", help="Path to the JSON schema file."),
    custom_props: Optional[str] = typer.Option(None, "--custom-props", "-c", help="Path to the directory containing custom properties schemas.")
) -> None:
    """Validate all data products in the filesystem."""
    try:
        asyncio.run(_validate_dps(root, schema, custom_props))
    except typer.Exit:
        raise
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

async def _validate_dps(root: Optional[str] = None, schema: Optional[str] = None, custom_props: Optional[str] = None):
    settings = get_settings()
    
    if getattr(settings.sdk, "filesystem_persistency", False) is False and getattr(settings.sdk, "topology", "") != "docker-rest-pxy-filesystem":
        typer.echo("Error: Validation is only supported when filesystem_persistency is enabled or docker-rest-pxy-filesystem topology is used.", err=True)
        raise typer.Exit(code=1)
        
    root_dir = root or getattr(settings.sdk, "data_products_filesystem_root", None) or "tmp/data_products_filesystem_root"
    
    if root:
        settings.sdk.data_products_filesystem_root = root
    if schema:
        settings.sdk.custom_validation_data_product_schema = schema
    if custom_props:
        settings.sdk.custom_validation_properties_path = custom_props
        
    typer.echo(f"Validation settings:")
    typer.echo(f"  - root: {root_dir}")
    typer.echo(f"  - schema: {getattr(settings.sdk, 'custom_validation_data_product_schema', None)}")
    typer.echo(f"  - custom-props: {getattr(settings.sdk, 'custom_validation_properties_path', None)}")
    typer.echo("-" * 40)

    if getattr(settings.sdk, "topology", "") == "docker-rest-pxy-filesystem" or getattr(settings.sdk, "rest_persistency_proxy", False):
        from dmesh.sdk.persistency.factory import RepositoryFactory
        factory = RepositoryFactory().create_from_settings(settings)
        repo = factory.get_data_product_repository()
    else:
        repo = AsyncFilesystemDataProductRepository(root_dir)
        
    results = await validate_dps(repo)
    
    # We check if there are any results to know if we found products, 
    # but wait, the CLI used to list dps manually. If results is empty, it means no data products or error.
    if not results:
        typer.echo(f"No data products found in {root_dir}.")
        return
        
    errors = False
    
    for validity in results:
        if validity.valid:
            typer.echo(f"✅ Validation successful for data product: {validity.name}")
        else:
            errors = True
            typer.echo(f"❌ Validation failed for data product: {validity.name}", err=True)
            if validity.error:
                typer.echo(f"   {validity.error}", err=True)
                
    if errors:
        raise typer.Exit(code=1)

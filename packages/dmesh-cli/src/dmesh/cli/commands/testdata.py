import asyncio
import re
from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path
import typer
from dmesh.cli.utils import get_service

app = typer.Typer()

DEFAULT_MERMAID_SPEC = """
classDiagram
    class finance{
        <<domain>>
    }
    class sap_fi{
        <<data-product>>
        dataProductTier : sourceAligned
    }
    class accounting_document_line_items{
        <<data-contract-schema>>
        client_id : string
        amount : number
    }
    class account_receivables_ledger{
        <<data-product>>
        dataProductTier : curated
    }
    class customer_open_items {
        <<data-contract-schema>>
        ledger_id : string
        invoice_date : date
        debit_amount : number
        credit_amount : number
    }
    class 360_finance {
        <<data-product>>
        dataProductTier : application
    }
    finance --> sap_fi: owns
    sap_fi --> accounting_document_line_items : exposes
    finance --> account_receivables_ledger : owns
    account_receivables_ledger --> customer_open_items : exposes
    finance --> 360_finance: owns
    sap_fi --> account_receivables_ledger : provides
    account_receivables_ledger --> 360_finance : provides
"""

def parse_mermaid_mesh(spec: str):
    # New parser following SCRATCH.md specification
    domains = set()
    dps = {} # name -> { domain, tier, schemas: [], attributes: {} }
    schemas = {} # name -> { properties: [] }
    edges = [] # (from, to, type)
    
    # 0. Strip comments
    lines = [line for line in spec.split("\n") if not line.strip().startswith("#")]
    spec = "\n".join(lines)

    # 1. Parse Classes
    class_pattern = re.compile(r"class\s+([a-zA-Z0-9_.-]+)\s*\{([\s\S]*?)\}", re.MULTILINE)
    for class_match in class_pattern.finditer(spec):
        class_name = class_match.group(1)
        content = class_match.group(2)
        
        # Identify type by stereotype
        is_domain = "<<domain>>" in content
        is_dp = "<<data-product>>" in content or "<<dp>>" in content
        is_schema = "<<data-contract-schema>>" in content or "<<dc-schema>>" in content
        
        # Extract attributes/properties
        attrs = {}
        props = []
        for line in content.strip().split("\n"):
            line = line.strip()
            if not line or line.startswith("<<"): continue
            
            # Match attr: value or prop: type
            match = re.match(r"([a-zA-Z0-9_.-]+)\s*:\s*([a-zA-Z0-9_.-]+)", line)
            if match:
                k, v = match.group(1), match.group(2)
                attrs[k] = v
                props.append({"name": k, "type": v})
        
        if is_domain:
            domains.add(class_name)
        elif is_dp:
            dps[class_name] = {
                "name": class_name,
                "tier": attrs.get("dataProductTier", "sourceAligned"),
                "domain": None,
                "schemas": [],
                "attributes": attrs
            }
        elif is_schema:
            schemas[class_name] = {
                "name": class_name,
                "properties": props
            }

    # 2. Parse Edges
    # from --> to : type
    edge_pattern = re.compile(r"([a-zA-Z0-9_.-]+)\s*(?:-->|->)\s*([a-zA-Z0-9_.-]+)\s*(?::\s*([a-zA-Z0-9_.-]+))?")
    for edge_match in edge_pattern.finditer(spec):
        u, v, t = edge_match.group(1), edge_match.group(2), edge_match.group(3)
        edges.append((u, v, t))
        
        # Resolve relationships
        if t == "owns":
            if v in dps:
                dps[v]["domain"] = u
        elif t == "exposes":
            if u in dps and v in schemas:
                dps[u]["schemas"].append(v)
        elif t == "provides":
            # Consumption edge: u provides to v
            pass

    # Post-process: handle DPs with missing domains
    for name, info in dps.items():
        if not info["domain"]:
            info["domain"] = "default"

    return dps, schemas, edges

async def _generate_testdata(spec: str):
    dps_info, schemas_info, edges = parse_mermaid_mesh(spec)
    
    async with get_service() as sdk:
        dp_id_map = {} # name -> id
        
        # Step 1: Create Data Products
        for name, info in dps_info.items():
            typer.echo(f"Creating Data Product: {info['domain']}.{name} ({info['tier']})")
            
            dp_spec = {
                "domain": info["domain"],
                "name": name,
                "customProperties": [
                    {"property": "dataProductTier", "value": info["tier"]}
                ],
                "outputPorts": []
            }
            
            # Add other attributes to customProperties
            for k, v in info["attributes"].items():
                if k != "dataProductTier":
                    dp_spec["customProperties"].append({"property": k, "value": v})
            
            # Add output ports
            for schema_name in info["schemas"]:
                dp_spec["outputPorts"].append({
                    "name": schema_name,
                    "version": "v1"
                })
            
            dp_obj = await sdk.put_data_product(dp_spec, include_metadata=True)
            dp_id_map[name] = str(dp_obj.id)
            
            # Step 2: Create Data Contracts
            for schema_name in info["schemas"]:
                s_info = schemas_info.get(schema_name)
                if not s_info: continue
                
                typer.echo(f"  Creating Data Contract for schema: {schema_name}")
                dc_spec = {
                    "schema": [
                        {
                            "name": schema_name,
                            "physicalName": schema_name,
                            "physicalType": "table",
                            "properties": [
                                {
                                    "name": p["name"],
                                    "physicalName": p["name"],
                                    "logicalType": p["type"]
                                } for p in s_info["properties"]
                            ]
                        }
                    ]
                }
                await sdk.put_data_contract(dc_spec, dp_id=str(dp_obj.id))

        # Step 3: Create Data Usage Agreements (consumption)
        for u, v, t in edges:
            if t == "provides":
                # u provides to v. u is producer, v is consumer.
                prod_id = dp_id_map.get(u)
                cons_id = dp_id_map.get(v)
                
                if prod_id and cons_id:
                    typer.echo(f"Creating edge: {u} -> {v}")
                    patch_spec = {
                        "customProperties": [
                            {
                                "property": "dataUsageAgreements",
                                "value": [
                                    {
                                        "info": {"active": True},
                                        "consumer": {"dataProductId": cons_id}
                                    }
                                ]
                            }
                        ]
                    }
                    await sdk.patch_data_product(patch_spec, id=prod_id)

@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    file: Optional[Path] = typer.Option(None, "--file", "-f", help="Path to a mermaid spec file."),
):
    """Generate test data from a mermaid spec."""
    if ctx.invoked_subcommand:
        return

    spec = DEFAULT_MERMAID_SPEC
    if file:
        if not file.exists():
            typer.echo(f"Error: File {file} not found.", err=True)
            raise typer.Exit(1)
        spec = file.read_text()
    
    try:
        asyncio.run(_generate_testdata(spec))
        typer.echo("Test data generation complete.")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        import traceback
        traceback.print_exc()
        raise typer.Exit(1)

if __name__ == "__main__":
    app()

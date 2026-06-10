import asyncio
import re
from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path
import typer
from dmesh.cli.utils import get_service

app = typer.Typer()

TESTDATA_DIR = Path(__file__).parent / "testdata"
SPEC_FILE = TESTDATA_DIR / "testdata_finance_mermaid.md"

def get_available_files_text() -> str:
    if TESTDATA_DIR.exists():
        files = [f.name for f in TESTDATA_DIR.glob("*.md")]
        if files:
            return "Available testdata files in default directory:\n" + "\n".join(f"  - {f}" for f in files)
    return "No testdata files found in default directory."

def _strip_mermaid_markers(text: str) -> str:
    text = text.strip()
    if text.startswith("```mermaid"):
        text = text[len("```mermaid"):].strip()
    if text.endswith("```"):
        text = text[:-3].strip()
    return text

def get_default_spec() -> str:
    if SPEC_FILE.exists():
        return _strip_mermaid_markers(SPEC_FILE.read_text())
    return ""

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
            match = re.match(r"([a-zA-Z0-9_.-]+)\s*:\s*(.+)", line)
            if match:
                k, v = match.group(1), match.group(2).strip()
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
        semaphore = asyncio.Semaphore(20)
        
        async def create_dp(name, info):
            async with semaphore:
                typer.echo(f"Creating Data Product: {info['domain']}.{name} ({info['tier']})")
                
                dp_spec = {
                    "domain": info["domain"],
                    "name": name,
                    "customProperties": [
                        {"property": "dataProductTier", "value": info["tier"]}
                    ],
                    "outputPorts": []
                }
                
                for k, v in info["attributes"].items():
                    if k != "dataProductTier":
                        dp_spec["customProperties"].append({"property": k, "value": v})
                
                for schema_name in info["schemas"]:
                    dp_spec["outputPorts"].append({
                        "name": schema_name,
                        "version": "v1"
                    })
                
                dp_obj = await sdk.put_data_product(dp_spec, include_metadata=True)
                dp_id_str = str(dp_obj.id) if not isinstance(dp_obj, dict) else str(dp_obj.get("id"))
                
                dc_tasks = []
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
                    dc_tasks.append(sdk.put_data_contract(dc_spec, dp_id=dp_id_str))
                
                if dc_tasks:
                    await asyncio.gather(*dc_tasks)
                    
                return name, dp_id_str
                
        dp_tasks = [create_dp(name, info) for name, info in dps_info.items()]
        results = await asyncio.gather(*dp_tasks)
        for name, dp_id in results:
            dp_id_map[name] = dp_id

        async def create_edge(u, v, t):
            if t == "provides":
                prod_id = dp_id_map.get(u)
                cons_id = dp_id_map.get(v)
                
                if prod_id and cons_id:
                    async with semaphore:
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
                        
        edge_tasks = [create_edge(u, v, t) for u, v, t in edges]
        if edge_tasks:
            await asyncio.gather(*edge_tasks)

@app.callback(invoke_without_command=True, epilog=get_available_files_text())
def main(
    ctx: typer.Context,
    file: Optional[Path] = typer.Option(None, "--file", "-f", help="Path to a mermaid spec file. Can be a filename from the default testdata directory."),
):
    """Generate test data from a mermaid spec."""
    if ctx.invoked_subcommand:
        return

    spec = get_default_spec()
    if file:
        if not file.exists():
            testdata_file = TESTDATA_DIR / file.name
            if testdata_file.exists():
                file = testdata_file
            else:
                typer.echo(f"Error: File {file} not found.", err=True)
                raise typer.Exit(1)
        spec = _strip_mermaid_markers(file.read_text())
    
    try:
        import time
        start = time.perf_counter()
        asyncio.run(_generate_testdata(spec))
        elapsed = time.perf_counter() - start
        typer.echo(f"Test data generation complete in {elapsed:.4f} seconds.")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        import traceback
        traceback.print_exc()
        raise typer.Exit(1)

if __name__ == "__main__":
    app()

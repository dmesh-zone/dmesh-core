import asyncio
import os
import shutil
from pathlib import Path
from typing import List, Optional
from uuid import UUID

import yaml

from dmesh.sdk.models import DataProduct, DataContract


class AsyncFilesystemDataProductRepository:
    def __init__(self, root_dir: str | Path):
        self.root_dir = Path(root_dir)
        self.root_dir.mkdir(parents=True, exist_ok=True)

    async def save(self, product: DataProduct) -> None:
        folder_name = product.specification.pop("_folder_name", None)
        name = folder_name or product.specification.get("name") or str(product.id)
        
        dp_dir = self.root_dir / name
        dp_dir.mkdir(parents=True, exist_ok=True)
        
        spec_path = dp_dir / "data_product_specification.yaml"
        with spec_path.open("w") as f:
            yaml.dump(product.specification, f, default_flow_style=False, sort_keys=False)

    async def get(self, id: UUID) -> Optional[DataProduct]:
        id_str = str(id)
        # Scan through all directories to find matching ID in the spec
        for dp_dir in self.root_dir.iterdir():
            if dp_dir.is_dir():
                spec_path = dp_dir / "data_product_specification.yaml"
                if spec_path.exists():
                    try:
                        with spec_path.open("r") as f:
                            spec = yaml.safe_load(f)
                            if spec:
                                spec_id = spec.get("id")
                                if spec_id == id_str or (not spec_id and dp_dir.name == id_str):
                                    dp = DataProduct(id=id, specification=spec)
                                    object.__setattr__(dp, "_folder_name", dp_dir.name)
                                    return dp
                    except Exception:
                        pass
        return None

    async def list(self, domain: Optional[str] = None, name: Optional[str] = None, version: Optional[str] = None) -> List[DataProduct]:
        results = []
        for dp_dir in self.root_dir.iterdir():
            if dp_dir.is_dir():
                spec_path = dp_dir / "data_product_specification.yaml"
                if spec_path.exists():
                    try:
                        with spec_path.open("r") as f:
                            spec = yaml.safe_load(f)
                            if not spec:
                                continue
                            
                            folder_name = dp_dir.name
                            spec_name = spec.get("name", folder_name)
                                
                            if domain and spec.get("domain") != domain:
                                continue
                            if name and spec_name != name:
                                continue
                            if version and spec.get("version") != version:
                                continue
                            dp_id_str = spec.get("id")
                            if dp_id_str:
                                dp_id = UUID(dp_id_str)
                            else:
                                # Try to parse UUID from directory name
                                try:
                                    dp_id = UUID(dp_dir.name)
                                except ValueError:
                                    dp_id = UUID(int=0)
                            dp = DataProduct(id=dp_id, specification=spec)
                            object.__setattr__(dp, "_folder_name", dp_dir.name)
                            results.append(dp)
                    except Exception:
                        pass
        return results

    async def delete(self, id: UUID) -> bool:
        dp = await self.get(id)
        if dp:
            name = dp.specification.get("name")
            if name:
                dp_dir = self.root_dir / name
                if dp_dir.exists():
                    shutil.rmtree(dp_dir)
                    return True
        return False

    async def truncate(self) -> None:
        for dp_dir in self.root_dir.iterdir():
            if dp_dir.is_dir():
                shutil.rmtree(dp_dir)


class AsyncFilesystemDataContractRepository:
    def __init__(self, root_dir: str | Path):
        self.root_dir = Path(root_dir)
        self.root_dir.mkdir(parents=True, exist_ok=True)

    async def save(self, contract: DataContract) -> None:
        # Determine the directory based on the DP
        dp_name = contract.specification.get("dataProduct")
        if not dp_name:
            raise ValueError("Data Contract specification must have a 'dataProduct' to be saved to filesystem.")
        
        dp_dir = self.root_dir / dp_name
        dp_dir.mkdir(parents=True, exist_ok=True)
        
        spec_path = dp_dir / "data_contract_specification.yaml"
        with spec_path.open("w") as f:
            yaml.dump(contract.specification, f, default_flow_style=False, sort_keys=False)

    async def get(self, id: UUID) -> Optional[DataContract]:
        id_str = str(id)
        for dp_dir in self.root_dir.iterdir():
            if dp_dir.is_dir():
                spec_path = dp_dir / "data_contract_specification.yaml"
                if spec_path.exists():
                    try:
                        with spec_path.open("r") as f:
                            spec = yaml.safe_load(f)
                            if spec and spec.get("id") == id_str:
                                # We need data_product_id. Let's try to find it by loading DP
                                dp_spec_path = dp_dir / "data_product_specification.yaml"
                                dp_id = None
                                if dp_spec_path.exists():
                                    with dp_spec_path.open("r") as f_dp:
                                        dp_spec = yaml.safe_load(f_dp)
                                        if dp_spec and dp_spec.get("id"):
                                            dp_id = UUID(dp_spec.get("id"))
                                
                                # Fallback if we couldn't resolve parent id cleanly
                                if dp_id is None:
                                    # the id isn't explicitly required to be valid in all cases if parent isn't found
                                    dp_id = UUID(int=0)
                                    
                                return DataContract(id=id, data_product_id=dp_id, specification=spec)
                    except Exception:
                        pass
        return None

    async def list(self, dp_id: Optional[UUID] = None, domain: Optional[str] = None, data_product: Optional[str] = None, version: Optional[str] = None) -> List[DataContract]:
        results = []
        for dp_dir in self.root_dir.iterdir():
            if dp_dir.is_dir():
                spec_path = dp_dir / "data_contract_specification.yaml"
                if spec_path.exists():
                    try:
                        with spec_path.open("r") as f:
                            spec = yaml.safe_load(f)
                            if not spec:
                                continue
                            
                            # We need to filter based on criteria.
                            dp_spec_path = dp_dir / "data_product_specification.yaml"
                            current_dp_id = None
                            if dp_spec_path.exists():
                                with dp_spec_path.open("r") as f_dp:
                                    dp_spec = yaml.safe_load(f_dp)
                                    if dp_spec and dp_spec.get("id"):
                                        current_dp_id = UUID(dp_spec.get("id"))
                            
                            if dp_id and current_dp_id != (dp_id if isinstance(dp_id, UUID) else UUID(str(dp_id))):
                                continue
                            if domain and spec.get("domain") != domain:
                                continue
                            if data_product and spec.get("dataProduct") != data_product:
                                continue
                            if version and spec.get("version") != version:
                                continue
                                
                            dc_id = UUID(spec.get("id"))
                            results.append(DataContract(id=dc_id, data_product_id=current_dp_id or UUID(int=0), specification=spec))
                    except Exception:
                        pass
        return results

    async def delete(self, id: UUID) -> bool:
        dc = await self.get(id)
        if dc:
            dp_name = dc.specification.get("dataProduct")
            if dp_name:
                dc_path = self.root_dir / dp_name / "data_contract_specification.yaml"
                if dc_path.exists():
                    os.remove(dc_path)
                    return True
        return False

    async def truncate(self) -> None:
        for dp_dir in self.root_dir.iterdir():
            if dp_dir.is_dir():
                spec_path = dp_dir / "data_contract_specification.yaml"
                if spec_path.exists():
                    os.remove(spec_path)

import json
from typing import List, Optional, Any
from uuid import UUID
from psycopg.rows import dict_row
from dmesh.sdk.models import DataProduct, DataContract
from dmesh.sdk.ports.repository import DataProductRepository, DataContractRepository

# --- SQL Queries ---
class DPQueries:
    GET = "SELECT id, specification, created_at, updated_at FROM data_products WHERE id = %s"
    SAVE = """
        INSERT INTO data_products (id, specification)
        VALUES (%s, %s)
        ON CONFLICT (id) DO UPDATE SET
            specification = EXCLUDED.specification,
            updated_at = NOW()
    """
    LIST_BASE = "SELECT id, specification, created_at, updated_at FROM data_products"
    DELETE = "DELETE FROM data_products WHERE id = %s RETURNING id"

class DCQueries:
    GET = "SELECT id, data_product_id, specification, created_at, updated_at FROM data_contracts WHERE id = %s"
    SAVE = """
        INSERT INTO data_contracts (id, data_product_id, specification)
        VALUES (%s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            specification = EXCLUDED.specification,
            updated_at = NOW()
    """
    LIST_BASE = "SELECT id, data_product_id, specification, created_at, updated_at FROM data_contracts"
    DELETE = "DELETE FROM data_contracts WHERE id = %s RETURNING id"

# --- Mapping Mixins ---
class DPMapping:
    def _row_to_dp(self, row: dict) -> DataProduct:
        return DataProduct(
            id=str(row["id"]),
            specification=row["specification"],
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
        )

class DCMapping:
    def _row_to_dc(self, row: dict) -> DataContract:
        return DataContract(
            id=str(row["id"]),
            data_product_id=str(row["data_product_id"]),
            specification=row["specification"],
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
        )

# --- ASYNC Granular Repositories ---
class PostgresDataProductRepository(DataProductRepository, DPMapping):
    def __init__(self, pool):
        self.pool = pool

    async def get(self, id: UUID) -> Optional[DataProduct]:
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute(DPQueries.GET, (str(id),))
                row = await cur.fetchone()
                return self._row_to_dp(row) if row else None

    async def save(self, product: DataProduct) -> None:
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(DPQueries.SAVE, (product.id, json.dumps(product.specification)))

    async def list(self, domain: Optional[str] = None, name: Optional[str] = None) -> List[DataProduct]:
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                filters, params = [], []
                if domain: filters.append("dp_domain = %s"); params.append(domain)
                if name: filters.append("dp_name = %s"); params.append(name)
                where = f"WHERE {' AND '.join(filters)}" if filters else ""
                await cur.execute(f"{DPQueries.LIST_BASE} {where}", params)
                rows = await cur.fetchall()
                return [self._row_to_dp(row) for row in rows]

    async def delete(self, id: UUID) -> bool:
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(DPQueries.DELETE, (str(id),))
                row = await cur.fetchone()
                return row is not None

class PostgresDataContractRepository(DataContractRepository, DCMapping):
    def __init__(self, pool):
        self.pool = pool

    async def get(self, id: UUID) -> Optional[DataContract]:
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute(DCQueries.GET, (str(id),))
                row = await cur.fetchone()
                return self._row_to_dc(row) if row else None

    async def save(self, contract: DataContract) -> None:
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(DCQueries.SAVE, (contract.id, contract.data_product_id, json.dumps(contract.specification)))

    async def list(self, dp_id: Optional[str] = None) -> List[DataContract]:
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                query, params = DCQueries.LIST_BASE, []
                if dp_id: query += " WHERE data_product_id = %s"; params.append(dp_id)
                await cur.execute(query, params)
                rows = await cur.fetchall()
                return [self._row_to_dc(row) for row in rows]

    async def delete(self, id: UUID) -> bool:
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(DCQueries.DELETE, (str(id),))
                row = await cur.fetchone()
                return row is not None

# --- SYNC Granular Repositories ---
class SyncPostgresDataProductRepository(DataProductRepository, DPMapping):
    def __init__(self, pool):
        self.pool = pool

    def get(self, id: UUID) -> Optional[DataProduct]:
        with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(DPQueries.GET, (str(id),))
                row = cur.fetchone()
                return self._row_to_dp(row) if row else None

    def save(self, product: DataProduct) -> None:
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(DPQueries.SAVE, (product.id, json.dumps(product.specification)))

    def list(self, domain: Optional[str] = None, name: Optional[str] = None) -> List[DataProduct]:
        with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                filters, params = [], []
                if domain: filters.append("dp_domain = %s"); params.append(domain)
                if name: filters.append("dp_name = %s"); params.append(name)
                where = f"WHERE {' AND '.join(filters)}" if filters else ""
                cur.execute(f"{DPQueries.LIST_BASE} {where}", params)
                rows = cur.fetchall()
                return [self._row_to_dp(row) for row in rows]

    def delete(self, id: UUID) -> bool:
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(DPQueries.DELETE, (str(id),))
                row = cur.fetchone()
                return row is not None

class SyncPostgresDataContractRepository(DataContractRepository, DCMapping):
    def __init__(self, pool):
        self.pool = pool

    def get(self, id: UUID) -> Optional[DataContract]:
        with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(DCQueries.GET, (str(id),))
                row = cur.fetchone()
                return self._row_to_dc(row) if row else None

    def save(self, contract: DataContract) -> None:
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(DCQueries.SAVE, (contract.id, contract.data_product_id, json.dumps(contract.specification)))

    def list(self, dp_id: Optional[str] = None) -> List[DataContract]:
        with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                query, params = DCQueries.LIST_BASE, []
                if dp_id: query += " WHERE data_product_id = %s"; params.append(dp_id)
                cur.execute(query, params)
                rows = cur.fetchall()
                return [self._row_to_dc(row) for row in rows]

    def delete(self, id: UUID) -> bool:
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(DCQueries.DELETE, (str(id),))
                row = cur.fetchone()
                return row is not None

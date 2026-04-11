import json
from typing import List, Optional, Any
from uuid import UUID
from psycopg.rows import dict_row
from dmesh.sdk.models import DataProduct, DataContract
from dmesh.sdk.ports.repository import DataProductRepository, DataContractRepository

class PostgresSchema:
    CREATE_TABLES = """
        CREATE TABLE IF NOT EXISTS data_products (
            id          TEXT        PRIMARY KEY,
            specification JSONB,
            created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            dp_domain   TEXT        GENERATED ALWAYS AS (specification->>'domain')  STORED,
            dp_name     TEXT        GENERATED ALWAYS AS (specification->>'name')    STORED,
            dp_version  TEXT        GENERATED ALWAYS AS (specification->>'version') STORED
        );

        CREATE UNIQUE INDEX IF NOT EXISTS uq_data_products_domain_name_version
            ON data_products (dp_domain, dp_name, dp_version);

        CREATE TABLE IF NOT EXISTS data_contracts (
            id              TEXT        PRIMARY KEY,
            data_product_id TEXT        NOT NULL REFERENCES data_products(id) ON DELETE CASCADE,
            specification   JSONB,
            created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
    """

# --- SQL Queries ---
class DPQueries:
    GET = "SELECT id, specification, created_at, updated_at FROM data_products WHERE id = %s"
    SAVE = """
        INSERT INTO data_products (id, specification)
        VALUES (%s, %s)
        ON CONFLICT (id) DO UPDATE SET
            specification = EXCLUDED.specification,
            updated_at = NOW()
        RETURNING created_at, updated_at
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
        RETURNING created_at, updated_at
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

    async def get(self, id: str) -> Optional[DataProduct]:
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute(DPQueries.GET, (id,))
                row = await cur.fetchone()
                return self._row_to_dp(row) if row else None

    async def save(self, product: DataProduct) -> None:
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute(DPQueries.SAVE, (product.id, json.dumps(product.specification)))
                row = await cur.fetchone()
                if row:
                    product.created_at = row["created_at"]
                    product.updated_at = row["updated_at"]

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

    async def delete(self, id: str) -> bool:
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(DPQueries.DELETE, (id,))
                row = await cur.fetchone()
                return row is not None

class PostgresDataContractRepository(DataContractRepository, DCMapping):
    def __init__(self, pool):
        self.pool = pool

    async def get(self, id: str) -> Optional[DataContract]:
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute(DCQueries.GET, (id,))
                row = await cur.fetchone()
                return self._row_to_dc(row) if row else None

    async def save(self, contract: DataContract) -> None:
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute(DCQueries.SAVE, (contract.id, contract.data_product_id, json.dumps(contract.specification)))
                row = await cur.fetchone()
                if row:
                    contract.created_at = row["created_at"]
                    contract.updated_at = row["updated_at"]

    async def list(self, dp_id: Optional[str] = None) -> List[DataContract]:
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                query, params = DCQueries.LIST_BASE, []
                if dp_id: query += " WHERE data_product_id = %s"; params.append(dp_id)
                await cur.execute(query, params)
                rows = await cur.fetchall()
                return [self._row_to_dc(row) for row in rows]

    async def delete(self, id: str) -> bool:
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(DCQueries.DELETE, (id,))
                row = await cur.fetchone()
                return row is not None


import json
from typing import List, Optional
from uuid import UUID
import psycopg
from psycopg.rows import dict_row
from dmesh.sdk.models import DataProduct, DataContract
from dmesh.sdk.ports.repository import DataMeshRepository, DataProductRepository, DataContractRepository

class PostgresSyncRepository(DataMeshRepository):
    def __init__(self, pool):
        self.pool = pool

    def _row_to_dp(self, row: dict) -> DataProduct:
        return DataProduct(
            id=str(row["id"]),
            specification=row["specification"]
        )

    def get_data_product(self, dp_id: str) -> Optional[DataProduct]:
        with self.pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    "SELECT id, specification FROM data_products WHERE id = %s",
                    (dp_id,),
                )
                row = cur.fetchone()
                return self._row_to_dp(row) if row else None

    # Implement other methods similarly for legacy support
    # ... but for CLI/API, we'll mostly use the new domain repositories
    def flush(self) -> None:
        with self.pool.getconn() as conn:
            conn.execute("DELETE FROM data_products")


class PostgresDataProductRepository(DataProductRepository):
    def __init__(self, pool):
        self.pool = pool

    def _row_to_dp(self, row: dict) -> DataProduct:
        return DataProduct(
            id=str(row["id"]),
            specification=row["specification"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    async def get(self, id: UUID) -> Optional[DataProduct]:
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute(
                    "SELECT id, specification, created_at, updated_at FROM data_products WHERE id = %s",
                    (str(id),),
                )
                row = await cur.fetchone()
                return self._row_to_dp(row) if row else None

    async def save(self, product: DataProduct) -> None:
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """
                    INSERT INTO data_products (id, specification)
                    VALUES (%s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        specification = EXCLUDED.specification,
                        updated_at = NOW()
                    """,
                    (product.id, json.dumps(product.specification)),
                )

    async def list(self, domain: Optional[str] = None, name: Optional[str] = None) -> List[DataProduct]:
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                filters = []
                params = []
                if domain:
                    filters.append("dp_domain = %s")
                    params.append(domain)
                if name:
                    filters.append("dp_name = %s")
                    params.append(name)
                
                where = f"WHERE {' AND '.join(filters)}" if filters else ""
                await cur.execute(f"SELECT id, specification, created_at, updated_at FROM data_products {where}", params)
                rows = await cur.fetchall()
                return [self._row_to_dp(row) for row in rows]

    async def delete(self, id: UUID) -> bool:
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute("DELETE FROM data_products WHERE id = %s RETURNING id", (str(id),))
                row = await cur.fetchone()
                return row is not None


class PostgresDataContractRepository(DataContractRepository):
    def __init__(self, pool):
        self.pool = pool

    def _row_to_dc(self, row: dict) -> DataContract:
        return DataContract(
            id=str(row["id"]),
            data_product_id=str(row["data_product_id"]),
            specification=row["specification"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    async def get(self, id: UUID) -> Optional[DataContract]:
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute(
                    "SELECT id, data_product_id, specification, created_at, updated_at FROM data_contracts WHERE id = %s",
                    (str(id),),
                )
                row = await cur.fetchone()
                return self._row_to_dc(row) if row else None

    async def save(self, contract: DataContract) -> None:
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """
                    INSERT INTO data_contracts (id, data_product_id, specification)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        specification = EXCLUDED.specification,
                        updated_at = NOW()
                    """,
                    (contract.id, contract.data_product_id, json.dumps(contract.specification)),
                )

    async def list(self, dp_id: Optional[str] = None) -> List[DataContract]:
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                query = "SELECT id, data_product_id, specification, created_at, updated_at FROM data_contracts"
                params = []
                if dp_id:
                    query += " WHERE data_product_id = %s"
                    params.append(dp_id)
                await cur.execute(query, params)
                rows = await cur.fetchall()
                return [self._row_to_dc(row) for row in rows]

    async def delete(self, id: UUID) -> bool:
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute("DELETE FROM data_contracts WHERE id = %s RETURNING id", (str(id),))
                row = await cur.fetchone()
                return row is not None


class SyncPostgresDataProductRepository(DataProductRepository):
    def __init__(self, pool):
        self.pool = pool

    def _row_to_dp(self, row: dict) -> DataProduct:
        return DataProduct(
            id=str(row["id"]),
            specification=row["specification"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    async def get(self, id: UUID) -> Optional[DataProduct]:
        with self.pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    "SELECT id, specification, created_at, updated_at FROM data_products WHERE id = %s",
                    (str(id),),
                )
                row = cur.fetchone()
                return self._row_to_dp(row) if row else None

    async def save(self, product: DataProduct) -> None:
        with self.pool.getconn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO data_products (id, specification)
                    VALUES (%s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        specification = EXCLUDED.specification,
                        updated_at = NOW()
                    """,
                    (product.id, json.dumps(product.specification)),
                )

    async def list(self, domain: Optional[str] = None, name: Optional[str] = None) -> List[DataProduct]:
        with self.pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                filters = []
                params = []
                if domain:
                    filters.append("dp_domain = %s")
                    params.append(domain)
                if name:
                    filters.append("dp_name = %s")
                    params.append(name)
                
                where = f"WHERE {' AND '.join(filters)}" if filters else ""
                cur.execute(f"SELECT id, specification, created_at, updated_at FROM data_products {where}", params)
                rows = cur.fetchall()
                return [self._row_to_dp(row) for row in rows]

    async def delete(self, id: UUID) -> bool:
        with self.pool.getconn() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM data_products WHERE id = %s RETURNING id", (str(id),))
                row = cur.fetchone()
                return row is not None


class SyncPostgresDataContractRepository(DataContractRepository):
    def __init__(self, pool):
        self.pool = pool

    def _row_to_dc(self, row: dict) -> DataContract:
        return DataContract(
            id=str(row["id"]),
            data_product_id=str(row["data_product_id"]),
            specification=row["specification"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    async def get(self, id: UUID) -> Optional[DataContract]:
        with self.pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    "SELECT id, data_product_id, specification, created_at, updated_at FROM data_contracts WHERE id = %s",
                    (str(id),),
                )
                row = cur.fetchone()
                return self._row_to_dc(row) if row else None

    async def save(self, contract: DataContract) -> None:
        with self.pool.getconn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO data_contracts (id, data_product_id, specification)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        specification = EXCLUDED.specification,
                        updated_at = NOW()
                    """,
                    (contract.id, contract.data_product_id, json.dumps(contract.specification)),
                )

    async def list(self, dp_id: Optional[str] = None) -> List[DataContract]:
        with self.pool.getconn() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                query = "SELECT id, data_product_id, specification, created_at, updated_at FROM data_contracts"
                params = []
                if dp_id:
                    query += " WHERE data_product_id = %s"
                    params.append(dp_id)
                cur.execute(query, params)
                rows = cur.fetchall()
                return [self._row_to_dc(row) for row in rows]

    async def delete(self, id: UUID) -> bool:
        with self.pool.getconn() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM data_contracts WHERE id = %s RETURNING id", (str(id),))
                row = cur.fetchone()
                return row is not None

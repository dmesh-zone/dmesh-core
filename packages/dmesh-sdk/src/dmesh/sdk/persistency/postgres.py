import json
from typing import List, Optional
from uuid import UUID
import psycopg
from psycopg.rows import dict_row
from dmesh.sdk.models import DataProduct, DataContract
from dmesh.sdk.ports.repository import DataMeshRepository

class PostgresRepository(DataMeshRepository):
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

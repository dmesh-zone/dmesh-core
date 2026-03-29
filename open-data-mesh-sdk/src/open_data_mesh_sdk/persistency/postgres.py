import json
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from open_data_mesh_sdk.core.models import DataProduct, DataContract
from open_data_mesh_sdk.core.repository import DataMeshRepository

class PostgresRepository(DataMeshRepository):
    def __init__(self, pool):
        self.pool = pool

    def _row_to_dp(self, row: dict) -> DataProduct:
        return DataProduct(
            id=str(row["id"]),
            specification=row["specification"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def _row_to_dc(self, row: dict) -> DataContract:
        return DataContract(
            id=str(row["id"]),
            data_product_id=str(row["data_product_id"]),
            specification=row["specification"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def create_data_product(self, dp: DataProduct) -> DataProduct:
        conn = self.pool.getconn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    INSERT INTO data_products (id, specification)
                    VALUES (%s, %s)
                    RETURNING id, specification, created_at, updated_at
                    """,
                    (dp.id, json.dumps(dp.specification)),
                )
                row = cur.fetchone()
                conn.commit()
                return self._row_to_dp(row)
        finally:
            self.pool.putconn(conn)

    def get_data_product(self, dp_id: str) -> Optional[DataProduct]:
        conn = self.pool.getconn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT id, specification, created_at, updated_at FROM data_products WHERE id = %s",
                    (dp_id,),
                )
                row = cur.fetchone()
                return self._row_to_dp(row) if row else None
        finally:
            self.pool.putconn(conn)

    def list_data_products(self, domain: str = None, name: str = None, version: str = None) -> List[DataProduct]:
        conn = self.pool.getconn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                filters = []
                params = []
                if domain:
                    filters.append("dp_domain = %s")
                    params.append(domain)
                if name:
                    filters.append("dp_name = %s")
                    params.append(name)
                if version:
                    filters.append("dp_version = %s")
                    params.append(version)
                
                where = f"WHERE {' AND '.join(filters)}" if filters else ""
                cur.execute(f"SELECT id, specification, created_at, updated_at FROM data_products {where}", params)
                rows = cur.fetchall()
                return [self._row_to_dp(row) for row in rows]
        finally:
            self.pool.putconn(conn)

    def update_data_product(self, dp: DataProduct) -> DataProduct:
        conn = self.pool.getconn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    UPDATE data_products
                    SET specification = %s, updated_at = NOW()
                    WHERE id = %s
                    RETURNING id, specification, created_at, updated_at
                    """,
                    (json.dumps(dp.specification), dp.id),
                )
                row = cur.fetchone()
                conn.commit()
                if not row:
                    raise ValueError(f"Data product {dp.id} not found")
                return self._row_to_dp(row)
        finally:
            self.pool.putconn(conn)

    def delete_data_product(self, dp_id: str) -> bool:
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM data_products WHERE id = %s RETURNING id", (dp_id,))
                row = cur.fetchone()
                conn.commit()
                return row is not None
        finally:
            self.pool.putconn(conn)

    def create_data_contract(self, dc: DataContract) -> DataContract:
        conn = self.pool.getconn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    INSERT INTO data_contracts (id, data_product_id, specification)
                    VALUES (%s, %s, %s)
                    RETURNING id, data_product_id, specification, created_at, updated_at
                    """,
                    (dc.id, dc.data_product_id, json.dumps(dc.specification)),
                )
                row = cur.fetchone()
                conn.commit()
                return self._row_to_dc(row)
        finally:
            self.pool.putconn(conn)

    def get_data_contract(self, dc_id: str) -> Optional[DataContract]:
        conn = self.pool.getconn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT id, data_product_id, specification, created_at, updated_at FROM data_contracts WHERE id = %s",
                    (dc_id,),
                )
                row = cur.fetchone()
                return self._row_to_dc(row) if row else None
        finally:
            self.pool.putconn(conn)

    def list_data_contracts(self, dp_id: str = None) -> List[DataContract]:
        conn = self.pool.getconn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                query = "SELECT id, data_product_id, specification, created_at, updated_at FROM data_contracts"
                params = []
                if dp_id:
                    query += " WHERE data_product_id = %s"
                    params.append(dp_id)
                cur.execute(query, params)
                rows = cur.fetchall()
                return [self._row_to_dc(row) for row in rows]
        finally:
            self.pool.putconn(conn)

    def update_data_contract(self, dc: DataContract) -> DataContract:
        conn = self.pool.getconn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    UPDATE data_contracts
                    SET specification = %s, updated_at = NOW()
                    WHERE id = %s
                    RETURNING id, data_product_id, specification, created_at, updated_at
                    """,
                    (json.dumps(dc.specification), dc.id),
                )
                row = cur.fetchone()
                conn.commit()
                if not row:
                    raise ValueError(f"Data contract {dc.id} not found")
                return self._row_to_dc(row)
        finally:
            self.pool.putconn(conn)

    def delete_data_contract(self, dc_id: str) -> bool:
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM data_contracts WHERE id = %s RETURNING id", (dc_id,))
                row = cur.fetchone()
                conn.commit()
                return row is not None
        finally:
            self.pool.putconn(conn)

    def flush(self) -> None:
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM data_products")
                conn.commit()
        finally:
            self.pool.putconn(conn)

import json
import sqlite3
from typing import List, Optional
from datetime import datetime
from open_data_mesh_sdk.core.models import DataProduct, DataContract
from open_data_mesh_sdk.core.repository import DataMeshRepository

class SQLiteRepository(DataMeshRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        conn = self._get_conn()
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS data_products (
                    id TEXT PRIMARY KEY,
                    specification TEXT,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    dp_domain TEXT GENERATED ALWAYS AS (json_extract(specification, '$.domain')) STORED,
                    dp_name TEXT GENERATED ALWAYS AS (json_extract(specification, '$.name')) STORED,
                    dp_version TEXT GENERATED ALWAYS AS (json_extract(specification, '$.version')) STORED
                )
            """)
            conn.execute("""
                CREATE UNIQUE INDEX IF NOT EXISTS uq_data_products_domain_name_version
                ON data_products (dp_domain, dp_name, dp_version)
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS data_contracts (
                    id TEXT PRIMARY KEY,
                    data_product_id TEXT NOT NULL,
                    specification TEXT,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (data_product_id) REFERENCES data_products (id) ON DELETE CASCADE
                )
            """)
            conn.commit()
        finally:
            conn.close()

    def _row_to_dp(self, row: sqlite3.Row) -> DataProduct:
        return DataProduct(
            id=row["id"],
            specification=json.loads(row["specification"]),
            created_at=datetime.fromisoformat(row["created_at"]) if isinstance(row["created_at"], str) else row["created_at"],
            updated_at=datetime.fromisoformat(row["updated_at"]) if isinstance(row["updated_at"], str) else row["updated_at"],
        )

    def _row_to_dc(self, row: sqlite3.Row) -> DataContract:
        return DataContract(
            id=row["id"],
            data_product_id=row["data_product_id"],
            specification=json.loads(row["specification"]),
            created_at=datetime.fromisoformat(row["created_at"]) if isinstance(row["created_at"], str) else row["created_at"],
            updated_at=datetime.fromisoformat(row["updated_at"]) if isinstance(row["updated_at"], str) else row["updated_at"],
        )

    def create_data_product(self, dp: DataProduct) -> DataProduct:
        conn = self._get_conn()
        try:
            conn.execute(
                "INSERT INTO data_products (id, specification) VALUES (?, ?)",
                (dp.id, json.dumps(dp.specification)),
            )
            conn.commit()
            return self.get_data_product(dp.id)
        finally:
            conn.close()

    def get_data_product(self, dp_id: str) -> Optional[DataProduct]:
        conn = self._get_conn()
        try:
            row = conn.execute(
                "SELECT id, specification, created_at, updated_at FROM data_products WHERE id = ?",
                (dp_id,),
            ).fetchone()
            return self._row_to_dp(row) if row else None
        finally:
            conn.close()

    def list_data_products(self, domain: str = None, name: str = None, version: str = None) -> List[DataProduct]:
        conn = self._get_conn()
        try:
            query = "SELECT id, specification, created_at, updated_at FROM data_products"
            conditions = []
            params = []
            if domain:
                conditions.append("dp_domain = ?")
                params.append(domain)
            if name:
                conditions.append("dp_name = ?")
                params.append(name)
            if version:
                conditions.append("dp_version = ?")
                params.append(version)
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            rows = conn.execute(query, params).fetchall()
            return [self._row_to_dp(row) for row in rows]
        finally:
            conn.close()

    def update_data_product(self, dp: DataProduct) -> DataProduct:
        conn = self._get_conn()
        try:
            cur = conn.execute(
                "UPDATE data_products SET specification = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (json.dumps(dp.specification), dp.id),
            )
            if cur.rowcount == 0:
                raise ValueError(f"Data product {dp.id} not found")
            conn.commit()
            return self.get_data_product(dp.id)
        finally:
            conn.close()

    def delete_data_product(self, dp_id: str) -> bool:
        conn = self._get_conn()
        try:
            cur = conn.execute("DELETE FROM data_products WHERE id = ?", (dp_id,))
            conn.commit()
            return cur.rowcount > 0
        finally:
            conn.close()

    def create_data_contract(self, dc: DataContract) -> DataContract:
        conn = self._get_conn()
        try:
            conn.execute(
                "INSERT INTO data_contracts (id, data_product_id, specification) VALUES (?, ?, ?)",
                (dc.id, dc.data_product_id, json.dumps(dc.specification)),
            )
            conn.commit()
            return self.get_data_contract(dc.id)
        finally:
            conn.close()

    def get_data_contract(self, dc_id: str) -> Optional[DataContract]:
        conn = self._get_conn()
        try:
            row = conn.execute(
                "SELECT id, data_product_id, specification, created_at, updated_at FROM data_contracts WHERE id = ?",
                (dc_id,),
            ).fetchone()
            return self._row_to_dc(row) if row else None
        finally:
            conn.close()

    def list_data_contracts(self, dp_id: str = None) -> List[DataContract]:
        conn = self._get_conn()
        try:
            query = "SELECT id, data_product_id, specification, created_at, updated_at FROM data_contracts"
            params = []
            if dp_id:
                query += " WHERE data_product_id = ?"
                params.append(dp_id)
            rows = conn.execute(query, params).fetchall()
            return [self._row_to_dc(row) for row in rows]
        finally:
            conn.close()

    def update_data_contract(self, dc: DataContract) -> DataContract:
        conn = self._get_conn()
        try:
            cur = conn.execute(
                "UPDATE data_contracts SET specification = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (json.dumps(dc.specification), dc.id),
            )
            if cur.rowcount == 0:
                raise ValueError(f"Data contract {dc.id} not found")
            conn.commit()
            return self.get_data_contract(dc.id)
        finally:
            conn.close()

    def delete_data_contract(self, dc_id: str) -> bool:
        conn = self._get_conn()
        try:
            cur = conn.execute("DELETE FROM data_contracts WHERE id = ?", (dc_id,))
            conn.commit()
            return cur.rowcount > 0
        finally:
            conn.close()

    def flush(self) -> None:
        conn = self._get_conn()
        try:
            conn.execute("DELETE FROM data_contracts")
            conn.execute("DELETE FROM data_products")
            conn.commit()
        finally:
            conn.close()

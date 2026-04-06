import sqlite3
import json
from typing import List, Optional
from dmesh.sdk.models import DataProduct, DataContract
from dmesh.sdk.ports.repository import DataMeshRepository

class SQLiteRepository(DataMeshRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS data_products (
                    id TEXT PRIMARY KEY,
                    specification TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS data_contracts (
                    id TEXT PRIMARY KEY,
                    data_product_id TEXT,
                    specification TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (data_product_id) REFERENCES data_products (id)
                )
            """)

    def create_data_product(self, dp: DataProduct) -> DataProduct:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO data_products (id, specification) VALUES (?, ?)",
                (dp.id, json.dumps(dp.specification))
            )
        return dp

    def get_data_product(self, dp_id: str) -> Optional[DataProduct]:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("SELECT specification FROM data_products WHERE id = ?", (dp_id,))
            row = cur.fetchone()
            if row:
                return DataProduct(id=dp_id, specification=json.loads(row[0]))
        return None

    def list_data_products(self, domain: str = None, name: str = None, version: str = None) -> List[DataProduct]:
        # Minimal filter for brevity
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("SELECT id, specification FROM data_products")
            rows = cur.fetchall()
            dps = [DataProduct(id=r[0], specification=json.loads(r[1])) for r in rows]
            if domain: dps = [d for d in dps if d.domain == domain]
            if name: dps = [d for d in dps if d.name == name]
            return dps

    def update_data_product(self, dp: DataProduct) -> DataProduct:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE data_products SET specification = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (json.dumps(dp.specification), dp.id)
            )
        return dp

    def delete_data_product(self, dp_id: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("DELETE FROM data_products WHERE id = ?", (dp_id,))
            return cur.rowcount > 0

    def create_data_contract(self, dc: DataContract) -> DataContract:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO data_contracts (id, data_product_id, specification) VALUES (?, ?, ?)",
                (dc.id, dc.data_product_id, json.dumps(dc.specification))
            )
        return dc

    def get_data_contract(self, dc_id: str) -> Optional[DataContract]:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("SELECT data_product_id, specification FROM data_contracts WHERE id = ?", (dc_id,))
            row = cur.fetchone()
            if row:
                return DataContract(id=dc_id, data_product_id=row[0], specification=json.loads(row[1]))
        return None

    def list_data_contracts(self, dp_id: str = None) -> List[DataContract]:
        with sqlite3.connect(self.db_path) as conn:
            query = "SELECT id, data_product_id, specification FROM data_contracts"
            params = []
            if dp_id:
                query += " WHERE data_product_id = ?"
                params.append(dp_id)
            cur = conn.execute(query, params)
            rows = cur.fetchall()
            return [DataContract(id=r[0], data_product_id=r[1], specification=json.loads(r[2])) for r in rows]

    def update_data_contract(self, dc: DataContract) -> DataContract:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE data_contracts SET specification = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (json.dumps(dc.specification), dc.id)
            )
        return dc

    def delete_data_contract(self, dc_id: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("DELETE FROM data_contracts WHERE id = ?", (dc_id,))
            return cur.rowcount > 0

    def flush(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM data_products")
            conn.execute("DELETE FROM data_contracts")

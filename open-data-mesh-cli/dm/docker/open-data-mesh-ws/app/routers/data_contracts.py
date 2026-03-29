import json
import uuid
from typing import Any, List, Optional

import jsonschema
import psycopg2
import psycopg2.errors
import requests as req_lib
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from psycopg2.extras import RealDictCursor

from app.db import get_pool
from app.id_generator import make_dc_id
from app.models import DataContractCreate, DataContractResponse, OdcsSpec

router = APIRouter()

_pool = None

ODCS_SCHEMA_URL = (
    "https://raw.githubusercontent.com/bitol-io/open-data-contract-standard"
    "/main/schema/odcs-json-schema-{api_version}.json"
)

DC_DEFAULTS = {
    "apiVersion": "v3.1.0",
    "kind": "DataContract",
    "status": "draft",
    "version": "v1.0.0",
}


def _get_pool():
    global _pool
    if _pool is None:
        _pool = get_pool()
    return _pool


def _enrich_dc(spec: dict, dp_domain: str, dp_name: str, dp_version: str, dc_index: int) -> dict:
    enriched = {**DC_DEFAULTS, **spec}
    enriched["id"] = make_dc_id(dp_domain, dp_name, dp_version, dc_index)
    return enriched


def _validate_dc(spec: dict) -> None:
    api_version = spec.get("apiVersion", "v3.1.0")
    url = ODCS_SCHEMA_URL.format(api_version=api_version)
    try:
        resp = req_lib.get(url, timeout=10)
    except req_lib.RequestException as e:
        raise HTTPException(status_code=422, detail=f"Cannot fetch ODCS schema: {e} URL={url}")
    if resp.status_code != 200:
        raise HTTPException(status_code=422, detail=f"Schema not found for odcs apiVersion={api_version} URL={url}")
    schema = resp.json()
    try:
        jsonschema.validate(spec, schema)
    except jsonschema.ValidationError as e:
        raise HTTPException(status_code=422, detail=e.message)


@router.post("/data-products/{dp_id}/data-contracts", status_code=201)
@router.post("/dps/{dp_id}/dcs", status_code=201, include_in_schema=False)
def create_data_contract(
    dp_id: uuid.UUID,
    payload: OdcsSpec,
):
    pool = _get_pool()
    conn = pool.getconn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT id, dp_domain, dp_name, dp_version FROM data_products WHERE id = %s",
                (str(dp_id),),
            )
            dp_row = cur.fetchone()
            if dp_row is None:
                raise HTTPException(status_code=404, detail=f"Data product {dp_id} not found.")

            # Count existing DCs for this DP to determine dc_index
            cur.execute(
                "SELECT COUNT(*) AS cnt FROM data_contracts WHERE data_product_id = %s",
                (str(dp_id),),
            )
            dc_index = cur.fetchone()["cnt"]

            enriched = _enrich_dc(
                payload.model_dump(),
                dp_row["dp_domain"] or "",
                dp_row["dp_name"] or "",
                dp_row["dp_version"] or "v1.0.0",
                dc_index,
            )
            _validate_dc(enriched)

            cur.execute(
                """
                INSERT INTO data_contracts (id, data_product_id, specification)
                VALUES (%s, %s, %s)
                RETURNING id, data_product_id, specification, created_at, updated_at
                """,
                (enriched["id"], str(dp_id), json.dumps(enriched)),
            )
            row = cur.fetchone()
            conn.commit()
        return row["specification"]
    except HTTPException:
        raise
    except psycopg2.Error:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Database error.")
    finally:
        pool.putconn(conn)


@router.get("/data-products/{dp_id}/data-contracts", status_code=200)
@router.get("/dps/{dp_id}/dcs", status_code=200, include_in_schema=False)
def list_data_contracts(dp_id: uuid.UUID):
    pool = _get_pool()
    conn = pool.getconn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT id FROM data_products WHERE id = %s", (str(dp_id),))
            if cur.fetchone() is None:
                raise HTTPException(status_code=404, detail=f"Data product {dp_id} not found.")
            cur.execute(
                "SELECT specification FROM data_contracts WHERE data_product_id = %s",
                (str(dp_id),),
            )
            rows = cur.fetchall()
        return [r["specification"] for r in rows]
    except HTTPException:
        raise
    except psycopg2.Error:
        raise HTTPException(status_code=500, detail="Database error.")
    finally:
        pool.putconn(conn)


@router.get("/data-contracts", status_code=200)
@router.get("/dcs", status_code=200, include_in_schema=False)
def list_all_data_contracts(
    domain: Optional[str] = Query(default=None),
    dp_name: Optional[str] = Query(default=None),
    dp_version: Optional[str] = Query(default=None),
):
    """List data contracts with optional DP filters. Returns rows with DP and DC info."""
    pool = _get_pool()
    conn = pool.getconn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            filters = []
            params = []
            if domain is not None:
                filters.append("dp.dp_domain = %s")
                params.append(domain)
            if dp_name is not None:
                filters.append("dp.dp_name = %s")
                params.append(dp_name)
            if dp_version is not None:
                filters.append("dp.dp_version = %s")
                params.append(dp_version)
            where = f"WHERE {' AND '.join(filters)}" if filters else ""
            cur.execute(
                f"""
                SELECT dp.id AS dp_id, dp.dp_domain, dp.dp_name, dp.dp_version,
                       dp.specification->>'status' AS dp_status,
                       dc.id AS dc_id
                FROM data_contracts dc
                JOIN data_products dp ON dc.data_product_id = dp.id
                {where}
                ORDER BY dp.dp_domain, dp.dp_name, dp.dp_version, dc.id
                """,
                params,
            )
            rows = cur.fetchall()
        return [dict(r) for r in rows]
    except psycopg2.Error:
        raise HTTPException(status_code=500, detail="Database error.")
    finally:
        pool.putconn(conn)


@router.get("/data-contracts/{id}", status_code=200)
@router.get("/dcs/{id}", status_code=200, include_in_schema=False)
def get_data_contract(id: uuid.UUID):
    pool = _get_pool()
    conn = pool.getconn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT dc.id, dc.data_product_id, dc.specification, dc.created_at, dc.updated_at,
                       dp.dp_domain, dp.dp_name, dp.dp_version
                FROM data_contracts dc
                JOIN data_products dp ON dc.data_product_id = dp.id
                WHERE dc.id = %s
                """,
                (str(id),),
            )
            row = cur.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail=f"Data contract {id} not found.")
        return JSONResponse(
            content=row["specification"],
            headers={
                "X-DC-ID": str(row["id"]),
                "X-DC-DP-ID": str(row["data_product_id"]),
                "X-DC-DP-Domain": row["dp_domain"] or "",
                "X-DC-DP-Name": row["dp_name"] or "",
                "X-DC-DP-Version": row["dp_version"] or "",
                "X-DC-Created-At": row["created_at"].isoformat(),
                "X-DC-Updated-At": row["updated_at"].isoformat(),
            },
        )
    except HTTPException:
        raise
    except psycopg2.Error:
        raise HTTPException(status_code=500, detail="Database error.")
    finally:
        pool.putconn(conn)


@router.put("/data-contracts/{id}", status_code=200)
@router.put("/dcs/{id}", status_code=200, include_in_schema=False)
def update_data_contract(id: uuid.UUID, payload: OdcsSpec):
    spec = {**payload.model_dump(), "id": str(id)}
    _validate_dc(spec)

    pool = _get_pool()
    conn = pool.getconn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                UPDATE data_contracts
                SET specification = %s, updated_at = NOW()
                WHERE id = %s
                RETURNING id, data_product_id, specification, created_at, updated_at
                """,
                (json.dumps(spec), str(id)),
            )
            row = cur.fetchone()
            conn.commit()
        if row is None:
            raise HTTPException(status_code=404, detail=f"Data contract {id} not found.")
        return row["specification"]
    except HTTPException:
        raise
    except psycopg2.Error:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Database error.")
    finally:
        pool.putconn(conn)


@router.delete("/data-contracts/{id}", status_code=204)
@router.delete("/dcs/{id}", status_code=204, include_in_schema=False)
def delete_data_contract(id: uuid.UUID):
    pool = _get_pool()
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM data_contracts WHERE id = %s RETURNING id", (str(id),))
            deleted = cur.fetchone()
            conn.commit()
        if deleted is None:
            raise HTTPException(status_code=404, detail=f"Data contract {id} not found.")
    except HTTPException:
        raise
    except psycopg2.Error:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Database error.")
    finally:
        pool.putconn(conn)

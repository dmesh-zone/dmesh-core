import json
import uuid
from typing import Any, List

import jsonschema
import psycopg2
import psycopg2.errors
from fastapi import APIRouter, HTTPException, Query
from psycopg2.extras import RealDictCursor

from app.db import get_pool
from app.models import DataProductCreate, DataProductResponse, OdpsSpec
from app.odps_enricher import enrich_spec
from app.odps_validator import SchemaFetchError, validate_spec

router = APIRouter()

_pool = None


def _get_pool():
    global _pool
    if _pool is None:
        _pool = get_pool()
    return _pool


def _row_to_response(row: dict) -> DataProductResponse:
    return DataProductResponse(
        id=row["id"],
        specification=row["specification"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


@router.post("/data-products", response_model=DataProductResponse, status_code=201)
@router.post("/dps", response_model=DataProductResponse, status_code=201, include_in_schema=False)
def create_data_product(spec: OdpsSpec):
    enriched = enrich_spec(spec.model_dump())

    try:
        validate_spec(enriched)
    except SchemaFetchError as e:
        raise HTTPException(status_code=422, detail=f"Cannot fetch ODPS schema: {e}")
    except jsonschema.ValidationError as e:
        raise HTTPException(status_code=422, detail=e.message)

    pool = _get_pool()
    conn = pool.getconn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO data_products (id, specification)
                VALUES (%s, %s)
                RETURNING id, specification, created_at, updated_at
                """,
                (enriched["id"], json.dumps(enriched),),
            )
            row = cur.fetchone()
            conn.commit()
        return _row_to_response(row)
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        raise HTTPException(
            status_code=409,
            detail="A data product with this domain/name/version already exists.",
        )
    except psycopg2.Error:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Database error.")
    finally:
        pool.putconn(conn)


@router.get("/data-products", response_model=List[Any], status_code=200)
@router.get("/dps", response_model=List[Any], status_code=200, include_in_schema=False)
def list_data_products(
    domain: str = Query(default=None),
    name: str = Query(default=None),
    version: str = Query(default=None),
):
    pool = _get_pool()
    conn = pool.getconn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            filters = []
            params = []
            if domain is not None:
                filters.append("dp_domain = %s")
                params.append(domain)
            if name is not None:
                filters.append("dp_name = %s")
                params.append(name)
            if version is not None:
                filters.append("dp_version = %s")
                params.append(version)
            where = f"WHERE {' AND '.join(filters)}" if filters else ""
            cur.execute(
                f"SELECT specification FROM data_products {where}",
                params,
            )
            rows = cur.fetchall()
        return [row["specification"] for row in rows]
    except psycopg2.Error:
        raise HTTPException(status_code=500, detail="Database error.")
    finally:
        pool.putconn(conn)


@router.get("/data-products/{id}", response_model=None, status_code=200)
@router.get("/dps/{id}", response_model=None, status_code=200, include_in_schema=False)
def get_data_product(id: uuid.UUID):
    pool = _get_pool()
    conn = pool.getconn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT id, specification, created_at, updated_at FROM data_products WHERE id = %s",
                (str(id),),
            )
            row = cur.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail=f"Data product {id} not found.")
        from fastapi.responses import JSONResponse
        return JSONResponse(
            content=row["specification"],
            headers={
                "X-DP-ID": str(row["id"]),
                "X-DP-Created-At": row["created_at"].isoformat(),
                "X-DP-Updated-At": row["updated_at"].isoformat(),
            },
        )
    except psycopg2.Error:
        raise HTTPException(status_code=500, detail="Database error.")
    finally:
        pool.putconn(conn)


@router.put("/data-products/{id}", response_model=DataProductResponse, status_code=200)
@router.put("/dps/{id}", response_model=DataProductResponse, status_code=200, include_in_schema=False)
def update_data_product(id: uuid.UUID, spec: OdpsSpec):
    enriched = enrich_spec({**spec.model_dump(), "id": str(id)})

    try:
        validate_spec(enriched)
    except SchemaFetchError as e:
        raise HTTPException(status_code=422, detail=f"Cannot fetch ODPS schema: {e}")
    except jsonschema.ValidationError as e:
        raise HTTPException(status_code=422, detail=e.message)

    pool = _get_pool()
    conn = pool.getconn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                UPDATE data_products
                SET specification = %s, updated_at = NOW()
                WHERE id = %s
                RETURNING id, specification, created_at, updated_at
                """,
                (json.dumps(enriched), str(id)),
            )
            row = cur.fetchone()
            conn.commit()
        if row is None:
            raise HTTPException(status_code=404, detail=f"Data product {id} not found.")
        return _row_to_response(row)
    except psycopg2.Error:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Database error.")
    finally:
        pool.putconn(conn)


@router.delete("/data-products/{id}", status_code=204)
@router.delete("/dps/{id}", status_code=204, include_in_schema=False)
def delete_data_product(id: uuid.UUID):
    pool = _get_pool()
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM data_products WHERE id = %s RETURNING id", (str(id),))
            deleted = cur.fetchone()
            conn.commit()
        if deleted is None:
            raise HTTPException(status_code=404, detail=f"Data product {id} not found.")
    except psycopg2.Error:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Database error.")
    finally:
        pool.putconn(conn)

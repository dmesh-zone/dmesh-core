"""Publishes an ODPS data product spec to the WS layer."""
from typing import Any, Optional

import httpx

from dmesh.cli.put.errors import DpPublishError

DEFAULT_VERSION = "v1.0.0"


class DpPublisher:
    def publish(self, spec: dict[str, Any], ws_base_url: str) -> str:
        """Create or update a data product.

        Resolution order:
        1. spec has 'id'                          → PUT /dps/{id}
        2. spec has 'domain' + 'name' (no 'id')  → lookup by domain/name/version → PUT /dps/{id}
        3. neither                                → POST /dps (create)

        Returns the data product id.
        """
        dp_id = spec.get("id")

        if not dp_id:
            domain = spec.get("domain")
            name = spec.get("name")
            if domain and name:
                version = spec.get("version", DEFAULT_VERSION)
                dp_id = self._lookup_id(ws_base_url, domain, name, version)

        try:
            if dp_id:
                url = f"{ws_base_url}/dps/{dp_id}"
                response = httpx.put(url, json=spec, timeout=30)
            else:
                url = f"{ws_base_url}/dps"
                response = httpx.post(url, json=spec, timeout=30)
        except httpx.RequestError as e:
            raise DpPublishError(f"WS layer is unreachable at {ws_base_url}: {e}") from e

        if response.status_code in (200, 201):
            body = response.json()
            # spec.id == data_products.id — they are always the same
            return body["id"]
        elif response.status_code == 404:
            raise DpPublishError(f"Data product {dp_id} not found.")
        elif response.status_code == 409:
            raise DpPublishError(
                "A data product with the same domain/name/version already exists."
            )
        elif response.status_code == 422:
            detail = response.json().get("detail", "Validation error")
            raise DpPublishError(f"Validation error: {detail}")
        else:
            raise DpPublishError(
                f"Unexpected response from WS layer: HTTP {response.status_code}"
            )

    def _lookup_id(self, ws_base_url: str, domain: str, name: str, version: str) -> Optional[str]:
        """Return the id of an existing data product by domain/name/version, or None."""
        try:
            resp = httpx.get(
                f"{ws_base_url}/dps",
                params={"domain": domain, "name": name, "version": version},
                timeout=30,
            )
        except httpx.RequestError:
            return None
        if resp.status_code == 200:
            results = resp.json()
            if results:
                return results[0].get("id")  # list returns specs directly
        return None

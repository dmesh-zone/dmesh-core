# 📓 Release Notes

All notable changes to the **Data Mesh SDK & CLI** will be documented in this file.

---

## 🚀 [v0.11.3] - 2026-10-06

### 🛡️ Security & Dependencies
- **Security Patch**: Upgraded `urllib3` dependency to `>=2.8.0` to resolve High Severity vulnerabilities reported by Snyk regarding Improper Certificate Validation (SNYK-PYTHON-URLLIB3-20302844) and Allocation of Resources Without Limits or Throttling (SNYK-PYTHON-URLLIB3-20302846).

### 🐛 Bug Fixes
- **Data Product Catalog Validation:** Fixed custom schema validation issuses

---
## 🚀 [v0.11.2] - 2026-10-03

### 🐛 Bug Fixes
- **Data Contract ID Generation Regression:** Fixed a critical issue in `put_data_contract` where the parent Data Product's `customProperties` (like `domainDataProductId`) were inadvertently being overwritten by the auto-injected `dataProductId` property during ID generation. The SDK now safely appends `dataProductId` to the existing properties, ensuring proper downstream propagation to ID generator hooks.

### 🖥️ CLI Enhancements
- **Output Alignment (`dmesh list dps`)**: Increased the `DP_NAME` column width to cleanly fit longer catalog names (e.g., `account_receivables_ledger`) and prevent subsequent columns from breaking alignment. Reordered columns to `DP_ID`, `DP_DOMAIN`, `DP_VERSION`, `DP_STATUS`, `DP_NAME`.
- **Simplified Output (`dmesh list dcs`)**: Streamlined Data Contract listing output columns to display `DC_ID`, `DP_ID`, `DP_DOMAIN`, `DP_VERSION`, `DP_STATUS`, and `DP_NAME`.

---
## 🚀 [v0.11.1] - 2026-09-30

### 🛡️ Security & Dependencies
- **Security Patch**: Upgraded `anyio` dependency to `v4.14.2` to resolve a critical security vulnerability regarding improper certificate validation (SNYK-PYTHON-ANYIO-19958324).

---
## 🚀 [v0.11.0] - 2026-09-29

### ✨ Highlights
This release updates the project to support the latest Open Data Product Standard (ODPS) and Open Data Contract Standard (ODCS) schema versions, along with naming convention alignments in the SDK and codebase.

### ⚙️ SDK & Core Logic
- **Schema Upgrades**: Upgraded the default SDK schemas to `odps-1.1.0.json` and `odcs-3.2.0.json`.
- **Property Transition**: Fully deprecated the custom property `dataProductTier` across the SDK in favor of the newly introduced native `.type` property in ODPS 1.1.0 for Data Products. Auto-generation logic and metadata lookups have been updated accordingly.
- **Naming Conventions**: Refactored internal codebase terminology by replacing usages of the `tier` nomenclature with `type` and `dp_type` across core SDK logic, testing methods, and lifecycle management scripts.

### 🖥️ CLI Enhancements & DX
- **Testdata CLI Generator**: Re-wired testdata mock generation scripts to inject and map data product architectural configurations via `.type` rather than falling back to `dataProductTier` custom properties.

---
## 🚀 [v0.10.2] - 2026-09-28

### ✨ Highlights
This release brings stability and compliance improvements for generating and identifying data products and contracts.

### ⚙️ SDK & Core Logic
- **Data Source Naming**: Auto-generated data source products now properly append `_data_source` to the `dp.name` instead of ` data source` to comply with snake_case naming convention
- **REST Connectivity**: Modified the default `rest_persistency_proxy_url` configuration to use `localhost` instead of `0.0.0.0` to resolve local CLI connectivity issues.

### 🖥️ CLI Enhancements & DX
- **Testdata CLI Generator**: Overhauled the generated Data Contract spec payloads for compliance with the Architecture Fitness rules (`v3.0.1`):
  - Injects fully populated `servers` and `roles` arrays into the data contracts.
  - Dynamically populates `physicalType` from `logicalType` for properties.
  - Automatically extracts and maps `description.purpose` from `dataProductBusinessName` in mermaid layouts.
  - Fixes schema validation errors by properly restricting unevaluated `physicalName` properties on the properties object.

---

## 🚀 [v0.10.1] - 2026-09-16

### 🛡️ Security & Bug Fixes
- **Vulnerability Patching**: Upgraded `cryptography` to `50.0.1` and `pyasn1` to `0.6.4` to resolve High Severity vulnerabilities reported by Snyk (e.g. SNYK-PYTHON-CRYPTOGRAPHY-18516621, SNYK-PYTHON-PYASN1-17972379).

---

## 🚀 [v0.10.0] - 2026-09-16

### ✨ Highlights
This release introduces Multi-Environment Discovery capabilities and extends filesystem topology configuration options for more flexible persistence structures.

### 🔍 Discovery & API
- **Multi-Environment Discovery**: Added `GET /discover-multi-environment` API endpoint to aggregate data product and contract discoveries across various target environments (e.g., Dev, QA, Prod), configurable via `api.environments` settings.
- **Robust Error Handling**: Standardized API error responses and implemented graceful fallback handling for cross-environment discovery failures.

### 💾 Filesystem & Topology
- **Nested Filesystem Paths**: Introduced the `sdk.data_products_filesystem_extra_path` setting (and `--spec-extra-path` CLI setup argument). This enables nesting data product specifications inside custom intermediate folders (e.g. `foo/bar`) under the main filesystem root.

---

## 🚀 [v0.9.0] - 2026-06-15

### ✨ Highlights
This release consolidates the deployment strategy for Databricks Apps, migrates the default application port, and brings numerous stability and type-safety fixes to the SDK and CLI tools.

### ☁️ Infrastructure & Deployment
- **Consolidated Databricks Apps Deployment**: Added a new deployment script (`deploy-api-and-viewer-as-databricks-app.sh`) that automatically builds the `dmesh-viewer` UI and bundles it with the `dmesh-api` to be served by a single Databricks App. 

### ⚙️ SDK & Core Logic
- **JSON Schema Validation Robustness**: Addressed deprecation warnings for `jsonschema` and integrated the `referencing` library to properly handle schema validation dependencies and registries, resolving `ModuleNotFoundError` and `Validator` runtime errors.
- **Dependency Management**: Fixed missing package declarations by explicitly including `httpx` and `referencing` dependencies into the SDK requirements.

### 🖥️ CLI Enhancements & DX
- **CLI Setup Modules**: Resolved missing module import errors for `errors` and `feedback` during the CLI's `container_manager` initialization.
- **Type Safety**: Addressed type-incompatibility and attribute errors in the `list` and `put` SDK/CLI commands, ensuring optional arguments (like `domain`, `dp_name`) are properly cast to strings and properties are safely accessed.

---

## 🚀 [v0.8.0] - 2026-06-14

### ✨ Highlights
This major release introduces the **Filesystem Persistency** mode, allowing users to read data product and data contract data from the filestystem 

### 💾 Filesystem & Topology
- **Filesystem Persistency**: Added a fully functioning filesystem-backed repository implementation for Data Products and Data Contracts, managed via the `DMESH_SDK__FILESYSTEM_PERSISTENCY` configuration flag.
- **Configurable Topology**: Replaced hardcoded proxy logic with a unified and configurable topology setting in the SDK and CLI.

### 🖥️ CLI Enhancements & DX
- **Setup Command Flags**: Added convenient short flags `-r` (rest proxy) and `-t` (topology type) to the `dmesh setup` command.
- **Logging Visibility**: Improved logging by enabling configurable log levels, significantly reducing operational noise, and natively displaying the active persistency mode in the CLI upon startup.

### ☁️ Infrastructure & Security
- **REST SSL Verification**: Added support for SSL certificate verification (`DMESH_SDK__REST_PERSISTENCY_PROXY_SSL_VERIFY`) when operating the REST persistency proxy.
- **Proxy Environment Injection**: Proxy environment variables and build arguments are now transparently injected into all `docker-compose` services.

### ⚡ Performance & Stability
- **PostgreSQL Connection Pool Sizing**: Fine-tuned the connection pool size in `PostgresRepositoryFactory` to prevent starvation and improve throughput.
- **Database Indexing**: Added a database index to the `data_product_id` column in the `data_contracts` table to speed up lookup operations.

---

## 🚀 [v0.7.0] - 2026-06-10

### ✨ Highlights
This release introduces support for deploying the API with a Lakebase/Postgres database backend on Databricks Apps, along with usability improvements to the CLI testdata generation tool.

### 🖥️ CLI Enhancements & DX
- **Testdata Discovery & Convenience**: The `dmesh testdata` command's help text now automatically lists the default test specification files available out-of-the-box. Additionally, the `--file` argument now seamlessly resolves plain filenames against the default `testdata` directory without requiring full absolute paths.

### ☁️ Infrastructure & Deployment
- **Databricks Apps Dual-Backend Support**: Upgraded the automated Databricks deployment script (`deploy-api-as-databricks-app.sh`) to support multiple target environments (`mem` and `lakebase`).
- **Lakebase/Postgres Configurations**: Segmented the base `app.yaml` configuration into dedicated `app-mem.yaml` and `app-lakebase.yaml` manifests. The Lakebase manifest is configured to wire `postgres` as the `DB_TYPE` and inject database credentials directly from Databricks Apps secrets (e.g., `DB_HOST`, `DB_USER`, etc.).

---
## 🚀 [v0.6.1] - 2026-06-09

### ✨ Highlights
This release focuses on massive performance improvements and concurrency bug fixes for the SDK and CLI tools, particularly when interacting with remote Databricks Apps.

### ⚙️ SDK & Core Logic
- **HTTP Connection Pooling**: Refactored the HTTP REST proxy repository to utilize a single shared `httpx.AsyncClient` with custom limits (`max_keepalive_connections=20`, `max_connections=100`). This completely resolves "TCP connection exhaustion" errors during high-throughput workloads.

### 🖥️ CLI Enhancements & DX
- **Parallel Test Data Generation**: Overhauled the `dmesh testdata` command. It now uses asynchronous gathering and a concurrency semaphore (up to 20 concurrent requests) to parallelize Data Product, Contract creation. This results in a >10x speedup when inserting large mock workloads.
- **Type Safety**: Addressed type-safety and linting issues around SDK return signatures, guaranteeing safer ID extraction when interacting with the REST proxy.

---

## 🚀 [v0.6.0] - 2026-06-07

### ✨ Highlights
This release introduces configurable setup topologies, optional REST proxy persistency, and logging enhancements.

### ⚙️ SDK & Core Logic
- **REST proxy persistency**: Added support for REST as a persistency proxy, supporting local as well as Databricks apps using M2M authentication.
  - Requires setting `sdk.rest_persistency_proxy=true`, `sdk.rest_persistency_proxy_url`, and `sdk.rest_persistency_proxy_uses_databricks_m2m=true` (or their `DMESH_SDK__` environment variable equivalents), alongside standard Databricks credentials.
- **Business Name Propagation**: Propagate `dataProductBusinessName` in SDK 
- **Data Source Injection**: Data source technology injection using `dataSourceTechnology`.
- **Data Source Suppression**: Added `dataSourceSuppressed` data product config.

### 🏛️ Database & Schema Security
- **Schema Usage**: Fixed `dmesh` schema not being used. Database tables now under `dmesh` schema and `dp_version` no longer a column of `data_products`.

### 🛠️ Developer Experience (DX) & Chores
- **Logging**: Enhancements to logging.

---

## 🚀 [v0.5.0] - 2026-05-27

### ✨ Highlights
This release improves the SDK and CLI by introducing automatic propagation of data product business names, enhancing the `testdata` command's parsing capabilities, and streamlining local testing experiences for macOS developers.

### ⚙️ SDK & Core Logic
- **Business Name Propagation**: Automated the propagation of the `dataProductBusinessName` custom property when the system auto-generates a Data Source Data Product from a Source-Aligned Data Product (the auto-generated product gets the business name with a " data source" suffix).

### 🖥️ CLI Enhancements & DX
- **Robust Mermaid Parsing**: Improved the `dmesh testdata` command to correctly parse custom properties (like `dataProductBusinessName`) that contain spaces, while preserving their exact casing.

### 🛠️ Developer Experience (DX) & Testing
- **Colima Docker Socket Fallback**: Implemented an automated fallback in the test suite for macOS users running Colima, seamlessly detecting `~/.colima/default/docker.sock` and setting `TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE` to resolve Ryuk mount errors without requiring manual IDE run configuration.

---

## 🚀 [v0.4.0] - 2026-05-20

### ✨ Highlights
This release strengthens relational isolation at the database layer by enforcing strict schema-level routing, simplifies CLI fetching by completely deprecating legacy `dp_version` qualifiers, and introduces selective suppression controls for automated data source replication.

### 🏛️ Database & Schema Security
- **Enforced Session Schema Routing**: Configured default `search_path` options at the `psycopg` connection pool level and permanently altered database role search paths. Any unqualified queries or third-party connections now resolve cleanly to the `dmesh` schema, completely preventing table-level leakage to the `public` schema.
- **Unified Test Schema Defaults**: Upgraded all API and SDK integration test suite connection parameters to match session-level routing standards.

### ⚙️ SDK & Core Logic
- **Selective Data Source Suppression**: Introduced the `dataSourceSupressed` (and `dataSourceSuppressed`) custom property flag on source-aligned data products, giving developers the ability to cleanly opt-out of automated data source generation.

### 🖥️ CLI Enhancements & DX
- **Deprecation of legacy `dp_version`**: Fully purged `dp_version` parameters, options, and filters across `get`, `get_dc`, `put`, and `list` commands.
- **Refined Filename Formats**: Fetching commands now save configurations to clean, versionless filename layouts in the format `{domain}_{dp_name}_{dc_id}.yaml`.

---

## 🚀 [v0.3.0] - 2026-05-13

### ✨ Highlights
This release advances architectural maturity through automated data source creation, rigorous SQL namespace isolation, streamlined schema configuration, and a fast-path performance testing suite.

### ⚙️ SDK & Core Logic
- Automated Data Source Generation: Introduced auto-creation of "Data Source Data Product" whenever a new "Source-Aligned Data Product" is registered (leveraging the `dataSourceTechnology` spec property).
Database Schema Unification: Completely eliminated the redundant embedded SQL string literal. Python's persistency layer now loads the single SQL source of truth (init.sql) dynamically at runtime.
- **Database Schema Unification**: Completely eliminated the redundant embedded SQL string literal. Python's persistency layer now loads the single SQL source of truth (`init.sql`) dynamically at runtime.
- **Schema Consolidation**: Cleaned up legacy database structures by removing the redundant `dp_version` column from the physical `data_products` table (with version supported only inside specification JSONB column)

### 🏛️ Infrastructure & Security
- **Isolated SQL Namespaces**: Migrated all database persistence and integration test suites into a dedicated Postgres `dmesh` schema, enabling clean multi-tenant hosting and stricter access controls.
- **Consolidated Docker Setup**: Streamlined Docker layouts by removing duplicate DB initialization folders in the API module in favor of a shared volume pointing to the core SDK asset.

### 🛠️ Developer Experience (DX)
- **Opt-in Performance Testing**: Heavy performance testing suites (`test_sdk_performance.py`) are now **skipped by default** using global pytest hooks. High-scale runs can be toggled via a new `--run-perf` CLI argument.
- **Global Testing Configuration**: Promoted performance testing and external database CLI flags to the root test fixtures for global execution flexibility.

---

## 🚀 [v0.2.0] - 2026-05-04

### ✨ Highlights
This release introduces significant enhancements to the CLI experience, SDK extensibility via custom ID hooks, and advanced discovery capabilities.

### 🖥️ CLI Enhancements
- **Interactive Mode**: Introduced `-i` / `--interactive` flag, launching a REPL environment with command history support for seamless mesh management.
- **Visual Spec Generation**: Added `dmesh testdata` command to instantly generate mesh components from [Mermaid](https://mermaid.js.org/) specifications.
- **Environment Management**: Added `dmesh clean` to quickly reset the local environment by truncating data product and contract tables.

### ⚙️ SDK & Core Logic
- **Extensible ID Generation**: Introduced `id_generator_hook`. Developers can now provide custom interfaces for `make_dp_id` and `make_dc_id`, working directly off the specification dictionaries.
- **Smart Enrichment**:
    - **Port Adapter Expansion**: Automatically populates new ports (e.g., OData) with `adaptedFrom` metadata.
    - **Contract Auto-linking**: Automatically links `contractId` and `contractVersion` during the enrichment phase.
- **Multi-Contract Support**: New `sdk.singleDataContractPerProduct` configuration (defaults to `True`) to control contract cardinality per product.
- **Deep Patching**: Enhanced `patch_data_product` to support selective updates within `customProperties` without overwriting existing metadata.

### 🔍 Discovery & Integration
- **Unified Discover API**: New `GET /discover` endpoint in the API and corresponding SDK methods for domain and name-based filtering.
- **Metadata Transformation**: SDK now automatically converts `dataUsageAgreements` custom properties into structured specification objects upon discovery.
- **UUID Standardization**: Internally migrated `data_products` and `data_contracts` keys to standard UUID types for better interoperability.

### 🛠️ Configuration & DX
- **Smart Defaults**: Added `DMESH_SDK__DATA_PRODUCT_STATUS_DEFAULT` and `DMESH_SDK__DATA_CONTRACT_STATUS_DEFAULT` (both defaulting to `active`).
- **Test Hardening**: Standardized ID assertions across the test suite and added comprehensive SDK client lifecycle tests.


# 📓 Release Notes

All notable changes to the **Data Mesh SDK & CLI** will be documented in this file.

---

## 🚀 [v0.3.0] - 2026-05-13

### ✨ Highlights
This release advances architectural maturity through automated data source creation, rigorous SQL namespace isolation, streamlined schema configuration, and a fast-path performance testing suite.

### ⚙️ SDK & Core Logic
- **Automated Data Source Generation**: Introduced auto-creation of "Application Data Products" whenever a new "Source-Aligned Data Product" is registered (leveraging the `dataProductTier` spec property).
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


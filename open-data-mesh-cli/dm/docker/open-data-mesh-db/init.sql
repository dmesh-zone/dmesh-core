CREATE TABLE IF NOT EXISTS data_products (
    id          UUID        PRIMARY KEY,
    specification JSONB,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    dp_domain   TEXT        GENERATED ALWAYS AS (specification->>'domain')  STORED,
    dp_name     TEXT        GENERATED ALWAYS AS (specification->>'name')    STORED,
    dp_version  TEXT        GENERATED ALWAYS AS (specification->>'version') STORED
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_data_products_domain_name_version
    ON data_products (dp_domain, dp_name, dp_version);

CREATE TABLE IF NOT EXISTS data_contracts (
    id              UUID        PRIMARY KEY,
    data_product_id UUID        NOT NULL REFERENCES data_products(id) ON DELETE CASCADE,
    specification   JSONB,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

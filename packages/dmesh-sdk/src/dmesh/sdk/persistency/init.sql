CREATE SCHEMA IF NOT EXISTS dmesh;

-- Set search_path to dmesh schema for subsequent operations
SET search_path TO dmesh, public;
ALTER ROLE CURRENT_USER SET search_path TO dmesh, public;

CREATE TABLE IF NOT EXISTS dmesh.data_products (
    id UUID PRIMARY KEY,
    specification JSONB NOT NULL,
    dp_domain TEXT GENERATED ALWAYS AS (specification->>'domain') STORED,
    dp_name TEXT GENERATED ALWAYS AS (specification->>'name') STORED,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_data_products_domain_name
    ON dmesh.data_products (dp_domain, dp_name);


CREATE TABLE IF NOT EXISTS dmesh.data_contracts (
    id UUID PRIMARY KEY,
    data_product_id UUID REFERENCES dmesh.data_products(id) ON DELETE CASCADE,
    specification JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_data_contracts_data_product_id 
    ON dmesh.data_contracts (data_product_id);

CREATE SCHEMA IF NOT EXISTS dmesh;

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

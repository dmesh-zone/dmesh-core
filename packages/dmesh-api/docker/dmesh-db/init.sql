CREATE TABLE IF NOT EXISTS data_products (
    id UUID PRIMARY KEY,
    specification JSONB NOT NULL,
    dp_domain TEXT GENERATED ALWAYS AS (specification->>'domain') STORED,
    dp_name TEXT GENERATED ALWAYS AS (specification->>'name') STORED,
    dp_version TEXT GENERATED ALWAYS AS (specification->>'version') STORED,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS data_contracts (
    id UUID PRIMARY KEY,
    data_product_id UUID REFERENCES data_products(id) ON DELETE CASCADE,
    specification JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

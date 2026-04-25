-- CXN Treasury Oracle Schema (public-safe stub template)
-- Treat this repository as public for boundary purposes.
-- Sensitive/internal financial schema details have been migrated to the Linear Virtual Office.
-- See: https://linear.app/conxian-labs
-- See: https://linear.app/conxian-labs/issue/CON-530/replace-sensitive-files-with-safe-examples-and-docs
-- See: https://linear.app/conxian-labs/issue/CON-256
--
-- How to work locally (public-safe):
-- 1) Use disposable local databases only.
-- 2) Keep credentials and operational values in local secret storage.
-- 3) Treat this file as a shape/example reference, not production DDL.

CREATE SCHEMA IF NOT EXISTS cxn_oracle_example;

CREATE TABLE IF NOT EXISTS cxn_oracle_example.asset_position_example (
    id UUID PRIMARY KEY,
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    asset_symbol TEXT NOT NULL,
    quantity_atomic NUMERIC NOT NULL CHECK (quantity_atomic >= 0),
    source_reference TEXT NOT NULL,
    environment_label TEXT NOT NULL DEFAULT 'local-dev'
);

CREATE TABLE IF NOT EXISTS cxn_oracle_example.yield_event_example (
    id UUID PRIMARY KEY,
    position_id UUID NOT NULL REFERENCES cxn_oracle_example.asset_position_example(id),
    event_type TEXT NOT NULL,
    amount_atomic NUMERIC NOT NULL,
    observed_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    note TEXT
);

CREATE INDEX IF NOT EXISTS idx_yield_event_example_observed_at
    ON cxn_oracle_example.yield_event_example (observed_at DESC);

-- Internal: search Linear Virtual Office for "CXN Treasury Oracle Schema".
-- This file is intentionally kept as a stub so existing links continue to resolve.

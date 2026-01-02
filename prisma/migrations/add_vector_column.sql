-- Vector Column Migration for pgvector
-- Run this AFTER running: prisma migrate dev
--
-- This migration adds the vector column and index that Prisma cannot manage
-- because it doesn't natively support the PostgreSQL vector type.

-- Ensure pgvector extension is enabled (should be done in init-db.sql)
CREATE EXTENSION IF NOT EXISTS vector;

-- Add the vector column for embeddings (1536 dimensions for text-embedding-3-small)
ALTER TABLE embeddings ADD COLUMN IF NOT EXISTS embedding vector(1536);

-- Create IVFFlat index for efficient cosine similarity search
-- The 'lists' parameter should be adjusted based on your data size:
-- - For < 1M rows: lists = rows / 1000
-- - For > 1M rows: lists = sqrt(rows)
CREATE INDEX IF NOT EXISTS embeddings_embedding_idx
ON embeddings USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Optional: Create index for L2 distance if needed
-- CREATE INDEX IF NOT EXISTS embeddings_embedding_l2_idx
-- ON embeddings USING ivfflat (embedding vector_l2_ops)
-- WITH (lists = 100);

-- Migration: Add entity_types column to shareable_links table
-- Date: 2025-10-15
-- Description: Adds entity_types JSON column to support filtering shared content (movies, restaurants, or both)

-- Add entity_types column with default value
ALTER TABLE shareable_links 
ADD COLUMN IF NOT EXISTS entity_types JSONB DEFAULT '["movies", "restaurants"]'::jsonb NOT NULL;

-- Update existing rows to have the default value (in case IF NOT EXISTS doesn't set default)
UPDATE shareable_links 
SET entity_types = '["movies", "restaurants"]'::jsonb 
WHERE entity_types IS NULL;

-- Verify the migration
SELECT column_name, data_type, column_default 
FROM information_schema.columns 
WHERE table_name = 'shareable_links' AND column_name = 'entity_types';


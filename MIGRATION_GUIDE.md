# 🚨 Quick Fix: Production Database Migration

## Problem
Your production Render database is missing the `entity_types` column in the `shareable_links` table, causing errors when users try to access shareable links.

## Solution
Run the migration script to add the missing column.

---

## ⚡ Quick Fix (Recommended)

### Step 1: Get Your Database Connection String

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click on **`binger-db`** (your PostgreSQL database)
3. Go to **"Connect"** tab
4. Copy the **"External Connection String"**
   - It looks like: `postgresql://binger_db_user:xxxxx@xxxxx.render.com/binger_db`

### Step 2: Run the Migration Script

Open your terminal and run:

```bash
cd /Users/dgolani/Documents/Binger_Backend
python migrations/run_migration.py
```

When prompted, paste your database connection string.

Type `yes` to confirm and run the migration.

---

## 🔧 Alternative: Manual SQL (If Script Fails)

### Using Render Dashboard SQL Shell:

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click on **`binger-db`**
3. Go to **"Shell"** tab (or "Connect" > "Shell")
4. Copy and paste this SQL:

```sql
-- Add entity_types column
ALTER TABLE shareable_links 
ADD COLUMN IF NOT EXISTS entity_types JSONB DEFAULT '["movies", "restaurants"]'::jsonb NOT NULL;

-- Update existing rows
UPDATE shareable_links 
SET entity_types = '["movies", "restaurants"]'::jsonb 
WHERE entity_types IS NULL;

-- Verify
SELECT column_name, data_type, column_default 
FROM information_schema.columns 
WHERE table_name = 'shareable_links' AND column_name = 'entity_types';
```

5. Press Enter and verify it shows the new column

---

## ✅ Verification

After running the migration, test your production app:

1. Try creating a shareable link
2. Try accessing an existing shareable link
3. Check the Render logs - the error should be gone

---

## 📝 What This Migration Does

- Adds `entity_types` column to `shareable_links` table
- Sets default value as `["movies", "restaurants"]` for all existing links
- Uses `IF NOT EXISTS` to be safe (won't break if column already exists)
- Works with PostgreSQL JSONB type for efficient querying

---

## 🆘 Need Help?

If you encounter any issues:
1. Check Render logs for error messages
2. Verify your database connection string is correct
3. Make sure you have database access permissions
4. Try the manual SQL option instead of the Python script


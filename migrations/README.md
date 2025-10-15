# Database Migrations

This folder contains database migration scripts for the Binger backend.

## How to Run Migrations on Render

### Option 1: Using Render Dashboard (SQL Shell)

1. Go to your [Render Dashboard](https://dashboard.render.com/)
2. Click on your **`binger-db`** PostgreSQL database
3. Go to the **"Shell"** tab (or "Connect" > "Shell")
4. Copy the SQL from the migration file (e.g., `001_add_entity_types_to_shareable_links.sql`)
5. Paste it into the shell and press Enter
6. Verify the output shows success

### Option 2: Using psql Command Line

1. Get your database connection string from Render:
   - Dashboard > `binger-db` > "Connections" > "External Connection String"
   
2. Connect using psql:
   ```bash
   psql "postgresql://binger_db_user:xxxxx@xxxxx.render.com/binger_db"
   ```

3. Run the migration:
   ```sql
   \i /path/to/001_add_entity_types_to_shareable_links.sql
   ```

### Option 3: Using Python Script (Automated)

Run the migration script from your local machine (requires production DATABASE_URL):

```bash
cd /Users/dgolani/Documents/Binger_Backend
python migrations/run_migration.py
```

---

## Migration History

| # | File | Description | Date | Status |
|---|------|-------------|------|--------|
| 001 | `001_add_entity_types_to_shareable_links.sql` | Add entity_types column for shared content filtering | 2025-10-15 | ✅ Ready |

---

## Creating New Migrations

1. Create a new `.sql` file with format: `NNN_description.sql`
2. Write idempotent SQL (use `IF NOT EXISTS`, `IF EXISTS`, etc.)
3. Update this README with the migration details
4. Test locally first, then run on production
5. Commit to git after successful deployment


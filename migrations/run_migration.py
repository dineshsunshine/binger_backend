"""
Database Migration Runner for Production
Run this script to apply database migrations to Render PostgreSQL
"""
import os
import sys
from pathlib import Path

# Add parent directory to path so we can import from app
sys.path.insert(0, str(Path(__file__).parent.parent))

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def get_database_url():
    """Get production database URL from environment or user input"""
    # Try to get from Render environment variable format
    db_url = os.getenv("DATABASE_URL")
    
    if not db_url:
        print("\n🔐 DATABASE_URL not found in environment.")
        print("Please get your PostgreSQL connection string from:")
        print("  Render Dashboard > binger-db > Connections > External Connection String")
        print()
        db_url = input("Enter DATABASE_URL: ").strip()
    
    return db_url


def run_migration(migration_file: str):
    """Run a SQL migration file on the production database"""
    
    # Get database URL
    db_url = get_database_url()
    
    if not db_url:
        print("❌ No database URL provided. Exiting.")
        return False
    
    # Read migration SQL
    migration_path = Path(__file__).parent / migration_file
    
    if not migration_path.exists():
        print(f"❌ Migration file not found: {migration_file}")
        return False
    
    with open(migration_path, 'r') as f:
        sql = f.read()
    
    print(f"\n📄 Running migration: {migration_file}")
    print(f"🗂️  File: {migration_path}")
    print(f"\n--- SQL Preview ---")
    print(sql[:500] + "..." if len(sql) > 500 else sql)
    print("--- End Preview ---\n")
    
    # Confirm before running
    confirm = input("⚠️  Run this migration on PRODUCTION? (yes/no): ").strip().lower()
    
    if confirm != "yes":
        print("❌ Migration cancelled.")
        return False
    
    try:
        # Connect to database
        print("\n🔌 Connecting to database...")
        conn = psycopg2.connect(db_url)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Run migration
        print("⚙️  Executing SQL...")
        cursor.execute(sql)
        
        # Fetch results if any (for verification query)
        if cursor.description:
            results = cursor.fetchall()
            print("\n✅ Migration completed successfully!")
            print("\n📊 Verification Results:")
            for row in results:
                print(f"  {row}")
        else:
            print("\n✅ Migration completed successfully!")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 All done! The entity_types column has been added to shareable_links table.")
        return True
        
    except psycopg2.Error as e:
        print(f"\n❌ Database error: {e}")
        print(f"   Error code: {e.pgcode}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("🔧 Binger Backend - Database Migration Runner")
    print("=" * 60)
    
    # Run the migration
    success = run_migration("001_add_entity_types_to_shareable_links.sql")
    
    if success:
        print("\n✨ Migration successful! Your production database is now up to date.")
        sys.exit(0)
    else:
        print("\n❌ Migration failed. Please check the error messages above.")
        sys.exit(1)


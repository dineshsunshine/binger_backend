"""
Temporary Admin Endpoints for Database Migrations
⚠️ DELETE THIS FILE AFTER MIGRATION IS COMPLETE
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from ....core.database import get_db
from ....core.auth import get_current_user
from ....models.user import User

router = APIRouter()


@router.post("/migrate-entity-types", tags=["Admin - Temporary"])
async def migrate_entity_types_column(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ⚠️ TEMPORARY MIGRATION ENDPOINT ⚠️
    
    Adds the entity_types column to shareable_links table.
    This endpoint should be called ONCE and then removed.
    
    **Steps:**
    1. Call this endpoint via Swagger UI
    2. Verify the response shows success
    3. Delete backend/app/api/v1/endpoints/admin.py
    4. Remove the import from router.py
    5. Commit and push the cleanup
    
    **This endpoint will be removed after migration is complete.**
    """
    try:
        # Check if column already exists
        check_sql = text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'shareable_links' 
            AND column_name = 'entity_types'
        """)
        
        result = db.execute(check_sql).fetchone()
        
        if result:
            return {
                "status": "already_exists",
                "message": "✅ entity_types column already exists! No migration needed.",
                "column_name": result[0]
            }
        
        # Add the column
        migration_sql = text("""
            ALTER TABLE shareable_links 
            ADD COLUMN entity_types JSONB DEFAULT '["movies", "restaurants"]'::jsonb NOT NULL
        """)
        
        db.execute(migration_sql)
        
        # Update existing rows
        update_sql = text("""
            UPDATE shareable_links 
            SET entity_types = '["movies", "restaurants"]'::jsonb 
            WHERE entity_types IS NULL
        """)
        
        db.execute(update_sql)
        
        # Commit the changes
        db.commit()
        
        # Verify
        verify_sql = text("""
            SELECT column_name, data_type, column_default 
            FROM information_schema.columns 
            WHERE table_name = 'shareable_links' 
            AND column_name = 'entity_types'
        """)
        
        verification = db.execute(verify_sql).fetchone()
        
        return {
            "status": "success",
            "message": "🎉 Migration completed successfully!",
            "column_details": {
                "name": verification[0],
                "type": verification[1],
                "default": str(verification[2])
            },
            "next_steps": [
                "✅ Migration complete!",
                "🗑️  Now delete backend/app/api/v1/endpoints/admin.py",
                "🗑️  Remove admin import from router.py",
                "📤 Commit and push the cleanup"
            ]
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Migration failed: {str(e)}"
        )


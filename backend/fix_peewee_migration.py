"""
Fix the peewee migration conflict by marking the problematic migration as complete.
This handles the case where SQLAlchemy migrations have already created the tag table
with a composite primary key, but peewee migrations try to create it with a unique id.
"""

import sqlite3
import sys
from pathlib import Path

# Database path
DB_PATH = Path(__file__).parent / "data" / "webui.db"

def fix_peewee_migration():
    """Mark peewee migrations as complete to avoid conflicts."""
    
    if not DB_PATH.exists():
        print(f"Database not found at {DB_PATH}")
        sys.exit(1)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if migratehistory table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='migratehistory'
        """)
        
        if not cursor.fetchone():
            print("migratehistory table not found. Creating it...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS migratehistory (
                    id INTEGER NOT NULL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    migrated_at DATETIME NOT NULL
                )
            """)
            conn.commit()
            print("✓ Created migratehistory table")
        
        # Check current migration status
        cursor.execute("SELECT name FROM migratehistory ORDER BY id")
        existing_migrations = [row[0] for row in cursor.fetchall()]
        
        print(f"\nCurrent peewee migrations:")
        if existing_migrations:
            for migration in existing_migrations:
                print(f"  ✓ {migration}")
        else:
            print("  (none)")
        
        # List of migrations that should be marked as complete
        # This includes all peewee migrations up to the point where SQLAlchemy takes over
        required_migrations = [
            "001_initial_schema",
            "002_add_local_sharing",
            "003_add_auth_api_key",
            "004_add_archived",
            "005_add_updated_at",
            "006_migrate_timestamps_and_charfields",
            "007_add_user_last_active_at",
            "008_add_memory",
            "009_add_models",
            "010_migrate_modelfiles_to_models",
            "011_add_user_settings",
            "012_add_tools",
            "013_add_user_info",
            "014_add_files",
            "015_add_functions",
            "016_add_valves_and_is_active",
            "017_add_user_oauth_sub",
            "018_add_function_is_global",
        ]
        
        # Add missing migrations
        added_count = 0
        for migration in required_migrations:
            if migration not in existing_migrations:
                cursor.execute("""
                    INSERT INTO migratehistory (name, migrated_at)
                    VALUES (?, datetime('now'))
                """, (migration,))
                print(f"  + Added: {migration}")
                added_count += 1
        
        if added_count > 0:
            conn.commit()
            print(f"\n✓ Marked {added_count} peewee migrations as complete!")
        else:
            print("\n✓ All peewee migrations already marked as complete!")
        
        # Verify tag table schema
        print("\nVerifying tag table schema...")
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='tag'")
        schema = cursor.fetchone()
        
        if schema:
            print("Current tag table schema:")
            print(schema[0])
            
            if "PRIMARY KEY (id, user_id)" in schema[0] or "pk_id_user_id" in schema[0]:
                print("\n✓ Tag table has correct composite primary key!")
            else:
                print("\n⚠ Warning: Tag table may not have the correct schema!")
                print("  Expected: Composite primary key on (id, user_id)")
        else:
            print("⚠ Tag table not found in database!")
        
    except Exception as e:
        conn.rollback()
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        conn.close()

if __name__ == "__main__":
    print("=" * 70)
    print("Fixing Peewee Migration Conflicts")
    print("=" * 70)
    fix_peewee_migration()
    print("=" * 70)
    print("Done! You can now restart the application.")
    print("=" * 70)

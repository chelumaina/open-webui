#!/usr/bin/env python3
"""
Fix NULL created_at and updated_at values in the chat table before running migrations.
This script is needed because Alembic migrations may fail if there are NULL values
when trying to set NOT NULL constraints.
"""

import sqlite3
import time
import sys
from pathlib import Path

# Database path
DB_PATH = Path(__file__).parent / "data" / "webui.db"

def fix_null_timestamps():
    """Fix NULL created_at and updated_at values in the chat table."""
    
    if not DB_PATH.exists():
        print(f"❌ Database not found at: {DB_PATH}")
        return False
    
    print(f"📂 Using database: {DB_PATH}")
    
    try:
        # Connect to the database
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        # Check for NULL values
        cursor.execute("""
            SELECT id, user_id, COALESCE(SUBSTR(title, 1, 50), 'No title'), created_at, updated_at
            FROM chat 
            WHERE created_at IS NULL OR updated_at IS NULL
        """)
        
        null_rows = cursor.fetchall()
        
        if not null_rows:
            print("✅ No NULL timestamp values found in chat table")
            conn.close()
            return True
        
        print(f"\n⚠️  Found {len(null_rows)} rows with NULL timestamps:\n")
        for row in null_rows:
            chat_id, user_id, title, created_at, updated_at = row
            print(f"  Chat ID: {chat_id}")
            print(f"    User: {user_id}")
            print(f"    Title: {title}")
            print(f"    created_at: {created_at}")
            print(f"    updated_at: {updated_at}\n")
        
        # Get current timestamp
        current_time = int(time.time())
        print(f"Current timestamp to use: {current_time}\n")
        
        # Update NULL created_at values
        cursor.execute("""
            UPDATE chat 
            SET created_at = ? 
            WHERE created_at IS NULL
        """, (current_time,))
        created_at_updated = cursor.rowcount
        
        # Update NULL updated_at values  
        cursor.execute("""
            UPDATE chat 
            SET updated_at = ? 
            WHERE updated_at IS NULL
        """, (current_time,))
        updated_at_updated = cursor.rowcount
        
        # Commit the changes
        conn.commit()
        
        print(f"✅ Fixed {created_at_updated} NULL created_at value(s)")
        print(f"✅ Fixed {updated_at_updated} NULL updated_at value(s)")
        
        # Verify the fix
        cursor.execute("""
            SELECT COUNT(*) 
            FROM chat 
            WHERE created_at IS NULL OR updated_at IS NULL
        """)
        remaining = cursor.fetchone()[0]
        
        if remaining == 0:
            print(f"\n✅ Verification passed: No NULL timestamps remaining")
        else:
            print(f"\n⚠️  Warning: Still {remaining} NULL timestamps remaining")
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"\n❌ SQLite error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("Fix NULL Timestamps in Chat Table")
    print("=" * 70 + "\n")
    
    success = fix_null_timestamps()
    
    if success:
        print("\n" + "=" * 70)
        print("✅ Script completed successfully!")
        print("=" * 70)
        print("\nYou can now run: alembic upgrade head")
        sys.exit(0)
    else:
        print("\n" + "=" * 70)
        print("❌ Script failed!")
        print("=" * 70)
        sys.exit(1)

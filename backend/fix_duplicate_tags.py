"""
Script to fix duplicate tag entries in the database.
This should be run before migrations to clean up any duplicate tag IDs.
"""

import sqlite3
import sys
from pathlib import Path

# Database path
DB_PATH = Path(__file__).parent / "data" / "webui.db"

def fix_duplicate_tags():
    """Remove duplicate tag entries, keeping only unique (id, user_id) combinations."""
    
    if not DB_PATH.exists():
        print(f"Database not found at {DB_PATH}")
        sys.exit(1)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Find all duplicates
        cursor.execute("""
            SELECT id, COUNT(*) as count 
            FROM tag 
            GROUP BY id 
            HAVING COUNT(*) > 1
        """)
        
        duplicates = cursor.fetchall()
        
        if not duplicates:
            print("No duplicate tags found!")
            return
        
        print(f"Found {len(duplicates)} duplicate tag IDs:")
        for tag_id, count in duplicates:
            print(f"  - '{tag_id}': {count} occurrences")
        
        # For each duplicate, keep only unique (id, user_id) combinations
        for tag_id, _ in duplicates:
            # Get all entries for this tag_id
            cursor.execute("""
                SELECT rowid, id, name, user_id, meta
                FROM tag
                WHERE id = ?
                ORDER BY rowid
            """, (tag_id,))
            
            entries = cursor.fetchall()
            seen_combinations = set()
            to_delete = []
            
            for rowid, id_val, name, user_id, meta in entries:
                combination = (id_val, user_id)
                if combination in seen_combinations:
                    to_delete.append(rowid)
                    print(f"  Marking for deletion: rowid={rowid}, id='{id_val}', user_id='{user_id}'")
                else:
                    seen_combinations.add(combination)
                    print(f"  Keeping: rowid={rowid}, id='{id_val}', user_id='{user_id}'")
            
            # Delete duplicates
            for rowid in to_delete:
                cursor.execute("DELETE FROM tag WHERE rowid = ?", (rowid,))
                print(f"  Deleted rowid={rowid}")
        
        conn.commit()
        print(f"\nSuccessfully removed {sum(len(to_delete) for _ in duplicates)} duplicate entries!")
        
    except Exception as e:
        conn.rollback()
        print(f"Error fixing duplicates: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("Fixing duplicate tag entries...")
    print("=" * 60)
    fix_duplicate_tags()
    print("=" * 60)
    print("Done! You can now run migrations.")
    print("=" * 60)

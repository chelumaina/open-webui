"""
Comprehensive script to diagnose and fix tag table issues.
"""

import sqlite3
import sys
from pathlib import Path

# Database path
DB_PATH = Path(__file__).parent / "data" / "webui.db"

def diagnose_and_fix():
    """Diagnose and fix tag table issues."""
    
    if not DB_PATH.exists():
        print(f"Database not found at {DB_PATH}")
        sys.exit(1)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        print("=" * 60)
        print("1. Current tag table schema:")
        print("=" * 60)
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='tag'")
        schema = cursor.fetchone()
        if schema:
            print(schema[0])
        else:
            print("Tag table not found!")
            return
        
        print("\n" + "=" * 60)
        print("2. Current indexes on tag table:")
        print("=" * 60)
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='index' AND tbl_name='tag'")
        indexes = cursor.fetchall()
        for idx in indexes:
            if idx[0]:  # Skip None (auto-created indexes)
                print(idx[0])
        
        print("\n" + "=" * 60)
        print("3. Checking for duplicate tag IDs:")
        print("=" * 60)
        cursor.execute("""
            SELECT id, COUNT(*) as count 
            FROM tag 
            GROUP BY id 
            HAVING COUNT(*) > 1
        """)
        
        duplicates = cursor.fetchall()
        
        if duplicates:
            print(f"Found {len(duplicates)} duplicate tag IDs:")
            for tag_id, count in duplicates:
                print(f"  - '{tag_id}': {count} occurrences")
                
                # Show details of duplicates
                cursor.execute("""
                    SELECT rowid, id, name, user_id
                    FROM tag
                    WHERE id = ?
                """, (tag_id,))
                entries = cursor.fetchall()
                for entry in entries:
                    print(f"      rowid={entry[0]}, id='{entry[1]}', name='{entry[2]}', user_id='{entry[3]}'")
        else:
            print("No duplicate tag IDs found.")
        
        print("\n" + "=" * 60)
        print("4. Checking for duplicate (id, user_id) combinations:")
        print("=" * 60)
        cursor.execute("""
            SELECT id, user_id, COUNT(*) as count 
            FROM tag 
            GROUP BY id, user_id 
            HAVING COUNT(*) > 1
        """)
        
        duplicates_combo = cursor.fetchall()
        
        if duplicates_combo:
            print(f"Found {len(duplicates_combo)} duplicate (id, user_id) combinations:")
            for tag_id, user_id, count in duplicates_combo:
                print(f"  - id='{tag_id}', user_id='{user_id}': {count} occurrences")
                
                # Delete all but one
                cursor.execute("""
                    SELECT rowid FROM tag
                    WHERE id = ? AND user_id = ?
                    ORDER BY rowid
                """, (tag_id, user_id))
                rowids = [r[0] for r in cursor.fetchall()]
                
                # Keep the first, delete the rest
                for rowid in rowids[1:]:
                    cursor.execute("DELETE FROM tag WHERE rowid = ?", (rowid,))
                    print(f"      Deleted duplicate rowid={rowid}")
            
            conn.commit()
            print("\n✓ Deleted duplicate (id, user_id) combinations!")
        else:
            print("No duplicate (id, user_id) combinations found.")
        
        print("\n" + "=" * 60)
        print("5. Checking if 'tag_id' index exists:")
        print("=" * 60)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='tag_id'")
        tag_id_index = cursor.fetchone()
        
        if tag_id_index:
            print(f"Found index: {tag_id_index[0]}")
            print("Attempting to drop it...")
            try:
                cursor.execute("DROP INDEX IF EXISTS tag_id")
                conn.commit()
                print("✓ Successfully dropped 'tag_id' index!")
            except Exception as e:
                print(f"✗ Error dropping index: {e}")
        else:
            print("'tag_id' index not found.")
        
        print("\n" + "=" * 60)
        print("6. All tags in database:")
        print("=" * 60)
        cursor.execute("SELECT id, user_id, name FROM tag ORDER BY id, user_id")
        all_tags = cursor.fetchall()
        print(f"Total tags: {len(all_tags)}")
        for tag in all_tags[:20]:  # Show first 20
            print(f"  id='{tag[0]}', user_id='{tag[1]}', name='{tag[2]}'")
        if len(all_tags) > 20:
            print(f"  ... and {len(all_tags) - 20} more")
        
    except Exception as e:
        conn.rollback()
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    diagnose_and_fix()
    print("\n" + "=" * 60)
    print("Diagnosis complete!")
    print("=" * 60)

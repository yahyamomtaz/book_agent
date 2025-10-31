#!/usr/bin/env python3
"""
Database Migration Script
Creates the book_descriptions table if it doesn't exist
"""

import sqlite3
import sys
import os

def create_book_descriptions_table(db_path):
    """Create the book_descriptions table"""
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return False
    
    print(f"📊 Connecting to database: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if table already exists
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='book_descriptions'"
    )
    
    if cursor.fetchone():
        print("ℹ️  Table 'book_descriptions' already exists")
        print("   Checking schema...")
        
        cursor.execute("PRAGMA table_info(book_descriptions)")
        columns = {row[1]: row[2] for row in cursor.fetchall()}
        
        print(f"   Found {len(columns)} columns")
        
        # List existing columns
        for col_name, col_type in columns.items():
            print(f"      - {col_name} ({col_type})")
        
        conn.close()
        return True
    
    print("📝 Creating 'book_descriptions' table...")
    
    # Create the table
    cursor.execute("""
        CREATE TABLE book_descriptions (
            description_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            collection_id INTEGER NOT NULL,
            number TEXT NOT NULL,
            language TEXT DEFAULT 'it',
            
            -- Metadata fields (Italian labels)
            author TEXT,
            second_author TEXT,
            title TEXT,
            publication TEXT,
            dimensions TEXT,
            weight TEXT,
            thickness TEXT,
            location TEXT,
            signature TEXT,
            imprint TEXT,
            text_layout TEXT,
            lines TEXT,
            requests TEXT,
            binding TEXT,
            language_info TEXT,
            significant_names TEXT,
            condition_info TEXT,
            decoration TEXT,
            physical_description TEXT,
            
            -- Timestamps
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            -- Foreign key constraint
            FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE,
            
            -- Unique constraint: one description per book per language
            UNIQUE(book_id, language)
        )
    """)
    
    print("✅ Table created successfully")
    
    # Create indexes for faster queries
    print("📇 Creating indexes...")
    
    cursor.execute("""
        CREATE INDEX idx_book_descriptions_book_id 
        ON book_descriptions(book_id)
    """)
    print("   ✅ Index on book_id")
    
    cursor.execute("""
        CREATE INDEX idx_book_descriptions_collection_id 
        ON book_descriptions(collection_id)
    """)
    print("   ✅ Index on collection_id")
    
    cursor.execute("""
        CREATE INDEX idx_book_descriptions_number 
        ON book_descriptions(number)
    """)
    print("   ✅ Index on number")
    
    # Create trigger to update timestamp
    print("⚙️  Creating update trigger...")
    cursor.execute("""
        CREATE TRIGGER update_book_descriptions_timestamp 
        AFTER UPDATE ON book_descriptions
        FOR EACH ROW
        BEGIN
            UPDATE book_descriptions 
            SET updated_at = CURRENT_TIMESTAMP 
            WHERE description_id = NEW.description_id;
        END
    """)
    print("   ✅ Trigger created")
    
    # Commit changes
    conn.commit()
    
    # Verify table was created
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='book_descriptions'")
    if cursor.fetchone():
        print("\n✅ Migration completed successfully!")
        
        # Show table info
        cursor.execute("PRAGMA table_info(book_descriptions)")
        columns = cursor.fetchall()
        
        print(f"\n📊 Table schema ({len(columns)} columns):")
        print(f"{'Column Name':<25} {'Type':<15} {'Nullable':<10} {'Default':<15}")
        print("-" * 70)
        for col in columns:
            col_name = col[1]
            col_type = col[2]
            not_null = "NOT NULL" if col[3] else "NULL"
            default = col[4] if col[4] else ""
            print(f"{col_name:<25} {col_type:<15} {not_null:<10} {default:<15}")
        
        conn.close()
        return True
    else:
        print("\n❌ Migration failed - table not found after creation")
        conn.close()
        return False


def check_books_table(db_path):
    """Verify the books table exists"""
    print("\n🔍 Checking 'books' table...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='books'")
    if cursor.fetchone():
        print("   ✅ 'books' table exists")
        
        # Count books by collection
        cursor.execute("""
            SELECT collection_id, COUNT(*) 
            FROM books 
            GROUP BY collection_id
        """)
        
        collections = cursor.fetchall()
        print(f"\n   📚 Books by collection:")
        collection_names = {3: "Incunaboli", 4: "Cinquecentine"}
        for coll_id, count in collections:
            name = collection_names.get(coll_id, f"Unknown (ID {coll_id})")
            print(f"      - {name}: {count} books")
        
        conn.close()
        return True
    else:
        print("   ❌ 'books' table not found")
        print("      This table must exist before creating book_descriptions")
        conn.close()
        return False


def main():
    """Main migration script"""
    print("="*70)
    print("Database Migration - Create book_descriptions Table")
    print("="*70)
    print()
    
    # Get database path from command line or use default
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    else:
        # Try to import from config
        try:
            from mcp_server_enhanced import DB_PATH
            db_path = DB_PATH
            print(f"Using database path from config: {db_path}")
        except ImportError:
            print("Usage: python3 migrate_database.py <path_to_database.db>")
            print("   or: Configure DB_PATH in mcp_server_enhanced.py first")
            return 1
    
    print(f"Database: {db_path}\n")
    
    # Check books table first
    if not check_books_table(db_path):
        print("\n⚠️  Cannot proceed without 'books' table")
        return 1
    
    # Create book_descriptions table
    print()
    success = create_book_descriptions_table(db_path)
    
    if success:
        print("\n" + "="*70)
        print("✅ Migration completed successfully!")
        print("="*70)
        print("\nNext steps:")
        print("1. Run: python3 test_setup.py")
        print("2. Run: python3 example_usage.py")
        print("3. Start processing: python3 mcp_server_enhanced.py")
        print()
        return 0
    else:
        print("\n" + "="*70)
        print("❌ Migration failed")
        print("="*70)
        return 1


if __name__ == "__main__":
    sys.exit(main())
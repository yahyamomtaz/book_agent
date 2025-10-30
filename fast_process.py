#!/usr/bin/env python3
"""
Book Agent - Simple Interactive Processor
Use this to easily process your books!
"""
import os
import sys

def show_menu():
    print("\n" + "=" * 60)
    print("Book Agent - What would you like to do?")
    print("=" * 60)
    print("\n1. Process ALL books in 'books/' folder")
    print("2. Process ONE specific book folder")
    print("3. List all book folders")
    print("4. Exit")
    print()

def list_books():
    """Show all book folders"""
    books_dir = "books"
    
    if not os.path.exists(books_dir):
        print(f"\n❌ '{books_dir}' folder doesn't exist!")
        print(f"   Current directory: {os.getcwd()}")
        return
    
    folders = [d for d in os.listdir(books_dir) 
               if os.path.isdir(os.path.join(books_dir, d))]
    
    if not folders:
        print(f"\n📁 No book folders found in '{books_dir}'")
        return
    
    print(f"\n📚 Found {len(folders)} book folder(s) in '{books_dir}':")
    for i, folder in enumerate(folders, 1):
        path = os.path.join(books_dir, folder)
        files = os.listdir(path)
        jpg_count = len([f for f in files if f.endswith('.jpg')])
        has_manifest = 'manifest.json' in files
        
        status = "✅ PROCESSED" if has_manifest else "⏳ NOT PROCESSED"
        print(f"  {i}. {folder:<20} {status}  ({jpg_count} images)")

def process_all():
    """Process all book folders"""
    from generator import process_book_folder
    
    books_dir = "books"
    
    if not os.path.exists(books_dir):
        print(f"\n❌ '{books_dir}' folder doesn't exist!")
        return
    
    folders = [d for d in os.listdir(books_dir) 
               if os.path.isdir(os.path.join(books_dir, d))]
    
    if not folders:
        print(f"\n⚠️  No book folders found!")
        return
    
    print(f"\n📚 Processing {len(folders)} book folder(s)...")
    print("=" * 60)
    
    success_count = 0
    error_count = 0
    
    for folder in folders:
        path = os.path.join(books_dir, folder)
        print(f"\n📖 {folder}...")
        
        try:
            process_book_folder(path)
            success_count += 1
        except Exception as e:
            print(f"   ❌ Error: {e}")
            error_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ Successfully processed: {success_count}")
    if error_count > 0:
        print(f"❌ Errors: {error_count}")
    print("=" * 60)

def process_one():
    """Process one specific book folder"""
    from generator import process_book_folder
    
    books_dir = "books"
    
    # Show available folders
    if os.path.exists(books_dir):
        folders = [d for d in os.listdir(books_dir) 
                   if os.path.isdir(os.path.join(books_dir, d))]
        
        if folders:
            print("\nAvailable book folders:")
            for folder in folders:
                print(f"  - {folder}")
    
    print("\nEnter the book folder name (e.g., '5d23'):")
    folder_name = input("> ").strip()
    
    if not folder_name:
        print("❌ No folder name entered")
        return
    
    # Try both with and without 'books/' prefix
    if os.path.exists(folder_name):
        path = folder_name
    elif os.path.exists(os.path.join(books_dir, folder_name)):
        path = os.path.join(books_dir, folder_name)
    else:
        print(f"\n❌ Folder not found: {folder_name}")
        print(f"   Tried: {folder_name}")
        print(f"   Tried: {os.path.join(books_dir, folder_name)}")
        return
    
    print(f"\n📖 Processing: {path}")
    print("=" * 60)
    
    try:
        process_book_folder(path)
        print("\n" + "=" * 60)
        print("✅ Success!")
        print("=" * 60)
        print(f"\nCheck {path}/ for:")
        print("  - manifest.json")
        print("  - Viewer*.js")
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ Error!")
        print("=" * 60)
        print(f"{e}")
        import traceback
        traceback.print_exc()

def main():
    print("\n" + "=" * 60)
    print("Book Agent - Simple Book Processor")
    print("=" * 60)
    print(f"\nCurrent directory: {os.getcwd()}")
    
    # Check if we're in the right place
    if not os.path.exists("generator.py"):
        print("\n⚠️  Warning: Can't find generator.py")
        print("   Make sure you're in the book_agent directory")
        print(f"\n   Run: cd ~/projects/book_agent")
        return
    
    while True:
        show_menu()
        choice = input("Your choice (1-4): ").strip()
        
        if choice == "1":
            process_all()
        elif choice == "2":
            process_one()
        elif choice == "3":
            list_books()
        elif choice == "4":
            print("\n👋 Goodbye!")
            break
        else:
            print(f"\n❌ Invalid choice: {choice}")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
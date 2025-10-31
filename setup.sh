#!/bin/bash

# Enhanced Book Agent MCP Server - Setup Script
# This script helps you set up the MCP server with all dependencies

set -e

echo "🚀 Book Agent MCP Server Setup"
echo "================================"
echo ""

# Check Python version
echo "📋 Checking Python version..."
python3 --version || {
    echo "❌ Python 3 is required but not found"
    exit 1
}

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip install watchdog python-docx modelcontextprotocol pandas openpyxl --break-system-packages || {
    echo "❌ Failed to install Python dependencies"
    exit 1
}

echo "✅ Python dependencies installed"

# Check for required files
echo ""
echo "📁 Checking for required files..."

required_files=("generator.py" "watcher.py" "utils.py")
missing_files=()

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -gt 0 ]; then
    echo "⚠️  Missing files:"
    printf '   - %s\n' "${missing_files[@]}"
    echo ""
    echo "Please ensure all required files are in the current directory:"
    echo "   - generator.py"
    echo "   - watcher.py"
    echo "   - utils.py"
    echo "   - mcp_server_enhanced.py"
else
    echo "✅ All required files present"
fi

# Create example configuration
echo ""
echo "📝 Configuration Setup"
echo "----------------------"
echo "The server needs to know where your files are located."
echo ""

read -p "Enter path to books folder [/path/to/books]: " WATCH_PATH
WATCH_PATH=${WATCH_PATH:-/path/to/books}

read -p "Enter path to database [/path/to/collections.db]: " DB_PATH
DB_PATH=${DB_PATH:-/path/to/collections.db}

read -p "Enter path to DOCX descriptions folder [/path/to/descriptions]: " DOCX_FOLDER
DOCX_FOLDER=${DOCX_FOLDER:-/path/to/descriptions}

read -p "Enter path to Excel file [/path/to/newbooks.xlsx]: " EXCEL_PATH
EXCEL_PATH=${EXCEL_PATH:-/path/to/newbooks.xlsx}

# Create config file
cat > config.json <<EOF
{
  "watch_path": "$WATCH_PATH",
  "db_path": "$DB_PATH",
  "docx_folder": "$DOCX_FOLDER",
  "excel_path": "$EXCEL_PATH"
}
EOF

echo ""
echo "✅ Configuration saved to config.json"

# Update mcp_server_enhanced.py with paths
if [ -f "mcp_server_enhanced.py" ]; then
    echo ""
    echo "📝 Updating mcp_server_enhanced.py with your paths..."
    
    sed -i "s|WATCH_PATH = \"/path/to/books\"|WATCH_PATH = \"$WATCH_PATH\"|g" mcp_server_enhanced.py
    sed -i "s|DB_PATH = \"/path/to/collections.db\"|DB_PATH = \"$DB_PATH\"|g" mcp_server_enhanced.py
    sed -i "s|DOCX_FOLDER = \"/path/to/descriptions\"|DOCX_FOLDER = \"$DOCX_FOLDER\"|g" mcp_server_enhanced.py
    sed -i "s|EXCEL_PATH = \"/path/to/newbooks.xlsx\"|EXCEL_PATH = \"$EXCEL_PATH\"|g" mcp_server_enhanced.py
    
    echo "✅ Paths updated in mcp_server_enhanced.py"
fi

# Test database connection
echo ""
echo "🔍 Testing database connection..."
if [ -f "$DB_PATH" ]; then
    sqlite3 "$DB_PATH" "SELECT name FROM sqlite_master WHERE type='table' AND name='books';" > /dev/null 2>&1 && {
        echo "✅ Database connection successful"
    } || {
        echo "⚠️  Database exists but may be missing required tables"
    }
else
    echo "⚠️  Database file not found at: $DB_PATH"
    echo "   The server will fail when trying to access it"
fi

# Check folder existence
echo ""
echo "🔍 Checking folders..."

[ -d "$WATCH_PATH" ] && echo "✅ Books folder exists: $WATCH_PATH" || echo "⚠️  Books folder not found: $WATCH_PATH"
[ -d "$DOCX_FOLDER" ] && echo "✅ DOCX folder exists: $DOCX_FOLDER" || echo "⚠️  DOCX folder not found: $DOCX_FOLDER"
[ -f "$EXCEL_PATH" ] && echo "✅ Excel file exists: $EXCEL_PATH" || echo "⚠️  Excel file not found: $EXCEL_PATH"

# Final instructions
echo ""
echo "================================"
echo "✅ Setup Complete!"
echo "================================"
echo ""
echo "📚 Next Steps:"
echo ""
echo "1. Start the MCP server:"
echo "   python3 mcp_server_enhanced.py"
echo ""
echo "2. Or test individual components:"
echo "   python3 -c 'from mcp_server_enhanced import extract_data_from_docx; print(extract_data_from_docx(\"test.docx\"))'"
echo ""
echo "3. Read the documentation:"
echo "   cat README_ENHANCED.md"
echo ""
echo "📝 Configuration saved in:"
echo "   - config.json"
echo "   - mcp_server_enhanced.py (paths updated)"
echo ""
echo "⚙️  Your configuration:"
echo "   Books:        $WATCH_PATH"
echo "   Database:     $DB_PATH"
echo "   DOCX folder:  $DOCX_FOLDER"
echo "   Excel file:   $EXCEL_PATH"
echo ""
echo "🎉 Happy book processing!"
# Book Agent MCP Server - Setup Guide

## Overview
This MCP server automates the processing of book collections by:
- Monitoring a folder for new book additions
- Extracting metadata from Word documents
- Generating IIIF manifests for image collections
- Creating Next.js viewer components with Mirador

## Installation

### 1. Install Dependencies

In your virtual environment:

```bash
# Activate your virtual environment
source agentenv/bin/activate  # or: conda activate agentenv

# Install required packages
pip install watchdog python-docx mcp
```

### 2. Configure the Server

Edit `mcp_server.py` and update the `WATCH_PATH` variable:

```python
WATCH_PATH = "/path/to/books"  # Change to your actual books directory
```

### 3. Set Up MCP Configuration

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on Mac, or `%APPDATA%\Claude\claude_desktop_config.json` on Windows):

```json
{
  "mcpServers": {
    "book-agent": {
      "command": "python3",
      "args": ["/home/yahya/projects/book_agent/mcp_server.py"],
      "env": {
        "PYTHONPATH": "/home/yahya/projects/book_agent"
      }
    }
  }
}
```

## Usage

### Running Standalone

To test the server standalone:

```bash
python3 mcp_server.py
```

### Through Claude Desktop

1. Restart Claude Desktop after updating the config
2. The server will appear in the MCP tools menu
3. Use the following tools:
   - `process_new_books`: Process all books in the watched folder
   - `start_auto_watch`: Start monitoring for new book folders

## Folder Structure

Each book folder should contain:
```
book-folder-name/
├── metadata.docx          (contains "Author: Name" line)
├── image001.jpg
├── image002.jpg
└── ...
```

After processing, the folder will also have:
```
book-folder-name/
├── manifest.json          (IIIF manifest)
└── ViewerBookIDAuthor.js  (Next.js component)
```

## Customization

### Author Extraction

Modify `utils.py` `extract_author_from_docx()` to match your document format:

```python
def extract_author_from_docx(docx_path):
    document = Document(docx_path)
    # Add your custom logic here
    # Examples:
    # - Check document properties: document.core_properties.author
    # - Look for specific patterns in text
    # - Parse structured metadata
```

### Image Dimensions

Update `generator.py` if your images have different dimensions:

```python
"height": 3933,  # Change to your image height
"width": 2645,   # Change to your image width
```

### Manifest URL

Update the URL prefix in `generator.py`:

```python
image_url_prefix = f"https://www.magic.unina.it/collections/incunaboli/{book_id}-{author.replace(' ', '-').lower()}"
```

## Troubleshooting

### ModuleNotFoundError

If you get import errors:
```bash
pip install --upgrade watchdog python-docx mcp
```

### Path Not Found

Ensure the `WATCH_PATH` directory exists:
```bash
mkdir -p /path/to/books
```

### Permission Issues

Make sure the script has write permissions to the book folders:
```bash
chmod -R u+w /path/to/books
```

## Development

### Testing

Create a test book folder:
```bash
mkdir test-book
echo "Author: Test Author" > test-book/metadata.docx
cp sample.jpg test-book/image001.jpg
```

Then process it:
```bash
python3 -c "from generator import process_book_folder; process_book_folder('test-book')"
```

### Debugging

Add verbose logging in `mcp_server.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## License

Update this section with your license information.
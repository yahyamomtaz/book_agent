import asyncio
import os
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio
from watcher import start_watching
from generator import process_book_folder

# Initialize the MCP server
server = Server("book-agent")

WATCH_PATH = "books"  # Update this to your actual path

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="process_new_books",
            description="Process all books in the watched folder and generate IIIF manifests and viewer components",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="start_auto_watch",
            description="Start automatically watching the books folder for new additions",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    if name == "process_new_books":
        try:
            await asyncio.to_thread(process_book_folder, WATCH_PATH)
            return [TextContent(
                type="text",
                text=f"Successfully processed books in {WATCH_PATH}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error processing books: {str(e)}"
            )]
    
    elif name == "start_auto_watch":
        try:
            # Start watching in a background task
            asyncio.create_task(asyncio.to_thread(start_watching, WATCH_PATH))
            return [TextContent(
                type="text",
                text=f"Started watching folder: {WATCH_PATH}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error starting watcher: {str(e)}"
            )]
    
    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]

async def main():
    """Run the MCP server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
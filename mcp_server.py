import asyncio
import os
from modelcontextprotocol.server import Server
from watcher import start_watching
from generator import process_book_folder

server = Server("book-agent", "1.0.0")

WATCH_PATH = "/path/to/books"

@server.tool()
async def process_new_books():
    await process_book_folder(WATCH_PATH)
    return {"success": True}

@server.tool()
async def start_auto_watch():
    asyncio.create_task(start_watching(WATCH_PATH))
    return {"watching": WATCH_PATH}

if __name__ == "__main__":
    asyncio.run(server.run_stdio())

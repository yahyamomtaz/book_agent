from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from generator import process_book_folder
import time

class BookHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            print(f"📁 New book folder detected: {event.src_path}")
            process_book_folder(event.src_path)

def start_watching(path):
    observer = Observer()
    event_handler = BookHandler()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    print(f"👀 Watching folder: {path}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

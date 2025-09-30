import os
import time
import logging
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Configuration
WATCH_DIRECTORY = os.getenv("WATCH_DIRECTORY")
API_ENDPOINT = os.getenv("API_ENDPOINT", "http://localhost:8000/upload")
SUPPORTED_FORMATS = ["pdf", "docx", "json", "txt"]
POLLING_INTERVAL = int(os.getenv("POLLING_INTERVAL", "5"))  # seconds

class DocumentHandler(FileSystemEventHandler):
    """Handler for document file events."""
    
    def __init__(self):
        self.processed_files = set()
        # Create the watch directory if it doesn't exist
        os.makedirs(WATCH_DIRECTORY, exist_ok=True)
        
    def on_created(self, event):
        """Called when a file or directory is created."""
        if event.is_directory:
            return
        self._process_file(event.src_path)
    
    def on_modified(self, event):
        """Called when a file or directory is modified."""
        if event.is_directory:
            return
        self._process_file(event.src_path)
    
    def _process_file(self, file_path):
        """Process a new or modified file."""
        # Skip files that are not in supported formats
        file_extension = file_path.split('.')[-1].lower()
        if file_extension not in SUPPORTED_FORMATS:
            logging.info(f"Skipping unsupported file format: {file_path}")
            return
        
        # Skip if file was already processed (to avoid duplicate processing)
        if file_path in self.processed_files:
            return
        
        logging.info(f"New document detected: {file_path}")
        
        # Upload the file to our API
        try:
            with open(file_path, 'rb') as file:
                filename = os.path.basename(file_path)
                files = {'file': (filename, file)}
                response = requests.post(API_ENDPOINT, files=files)
                
                if response.status_code == 200:
                    logging.info(f"Successfully processed: {filename}")
                    self.processed_files.add(file_path)
                    
                    # Delete the file after successful upload
                    try:
                        os.remove(file_path)
                        logging.info(f"Deleted file after successful upload: {filename}")
                    except Exception as e:
                        logging.error(f"Error deleting file {filename}: {str(e)}")
                else:
                    logging.error(f"Error processing {filename}: {response.text}")
        except Exception as e:
            logging.error(f"Error uploading {file_path}: {str(e)}")
    
    def scan_directory(self):
        """Scan the directory for existing files that haven't been processed yet."""
        for filename in os.listdir(WATCH_DIRECTORY):
            file_path = os.path.join(WATCH_DIRECTORY, filename)
            if os.path.isfile(file_path) and file_path not in self.processed_files:
                self._process_file(file_path)

def main():
    """Run the document watcher service."""
    logging.info(f"Starting document watcher service on directory: {WATCH_DIRECTORY}")
    
    # Set up event handler and observer
    event_handler = DocumentHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIRECTORY, recursive=False)
    observer.start()
    
    try:
        # Initial scan for existing files
        event_handler.scan_directory()
        
        # Keep the service running
        while True:
            # Periodically scan directory for new files
            time.sleep(POLLING_INTERVAL)
            event_handler.scan_directory()
            
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()
    logging.info("Document watcher service stopped")

if __name__ == "__main__":
    main()
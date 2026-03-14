#!/usr/bin/env python3
"""
File System Watcher for AI Employee
Monitors a drop folder and creates action files in Needs_Action
"""

import os
import sys
import time
import logging
import json
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
VAULT_PATH = Path(__file__).parent.parent / "AI_Employee_Vault"
DROP_FOLDER = Path.home() / "AI_Employee_Drop"
NEEDS_ACTION = VAULT_PATH / "Needs_Action"
PROCESSED_FILE = VAULT_PATH / ".processed_files"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(VAULT_PATH / "Logs" / "watcher.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("FileSystemWatcher")


class DropFolderHandler(FileSystemEventHandler):
    """Handles file system events in the drop folder"""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.needs_action = vault_path / "Needs_Action"
        self.processed_files = self._load_processed_files()

    def _load_processed_files(self) -> set:
        """Load set of already processed files"""
        if PROCESSED_FILE.exists():
            try:
                with open(PROCESSED_FILE, 'r') as f:
                    return set(json.load(f))
            except Exception as e:
                logger.warning(f"Could not load processed files: {e}")
        return set()

    def _save_processed_files(self):
        """Save processed files to avoid duplicates"""
        try:
            with open(PROCESSED_FILE, 'w') as f:
                json.dump(list(self.processed_files), f)
        except Exception as e:
            logger.error(f"Could not save processed files: {e}")

    def on_created(self, event):
        """Handle file creation events"""
        if event.is_directory:
            return

        source_path = Path(event.src_path)

        # Skip hidden files and system files
        if source_path.name.startswith('.'):
            return

        # Skip if already processed
        if str(source_path) in self.processed_files:
            return

        try:
            # Wait a moment for file to be fully written
            time.sleep(0.5)

            if not source_path.exists():
                return

            logger.info(f"New file detected: {source_path.name}")
            self._create_action_file(source_path)

            # Mark as processed
            self.processed_files.add(str(source_path))
            self._save_processed_files()

        except Exception as e:
            logger.error(f"Error processing file {source_path}: {e}")

    def _create_action_file(self, source_path: Path):
        """Create a markdown action file for the dropped file"""

        # Get file info
        file_size = source_path.stat().st_size
        file_ext = source_path.suffix
        timestamp = datetime.now().isoformat()

        # Create action file name
        action_filename = f"FILE_{source_path.stem}_{int(time.time())}.md"
        action_filepath = self.needs_action / action_filename

        # Create markdown content
        content = f"""---
type: file_drop
original_name: {source_path.name}
file_path: {source_path}
size_bytes: {file_size}
file_type: {file_ext if file_ext else 'unknown'}
detected_at: {timestamp}
status: pending
priority: medium
---

# File Drop Detected

A new file has been dropped for processing.

## File Details

- **Name:** {source_path.name}
- **Size:** {file_size:,} bytes
- **Type:** {file_ext if file_ext else 'Unknown'}
- **Path:** {source_path}
- **Detected:** {timestamp}

## Actions

- [ ] Review file contents
- [ ] Determine action needed
- [ ] Process or archive
- [ ] Move to /Done when complete

## Notes

Add any processing notes here.
"""

        # Write action file
        action_filepath.write_text(content)
        logger.info(f"Created action file: {action_filename}")

        # Log to audit
        self._log_action(source_path, action_filepath)

    def _log_action(self, source_path: Path, action_filepath: Path):
        """Log the file drop event"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action_type": "file_drop_detected",
            "actor": "filesystem_watcher",
            "source_file": str(source_path),
            "action_file": str(action_filepath),
            "file_size": source_path.stat().st_size,
            "status": "pending"
        }

        # Append to daily log
        log_date = datetime.now().strftime("%Y-%m-%d")
        log_file = self.vault_path / "Logs" / f"{log_date}.json"

        try:
            if log_file.exists():
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            else:
                logs = []

            logs.append(log_entry)

            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)
        except Exception as e:
            logger.error(f"Could not write log: {e}")


def ensure_drop_folder():
    """Ensure drop folder exists"""
    DROP_FOLDER.mkdir(parents=True, exist_ok=True)
    logger.info(f"Drop folder ready: {DROP_FOLDER}")


def run_watcher():
    """Start the file system watcher"""

    ensure_drop_folder()

    logger.info("=" * 60)
    logger.info("File System Watcher Started")
    logger.info("=" * 60)
    logger.info(f"Monitoring: {DROP_FOLDER}")
    logger.info(f"Vault: {VAULT_PATH}")
    logger.info(f"Action folder: {NEEDS_ACTION}")
    logger.info("=" * 60)

    event_handler = DropFolderHandler(VAULT_PATH)
    observer = Observer()
    observer.schedule(event_handler, str(DROP_FOLDER), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping watcher...")
        observer.stop()
    observer.join()

    logger.info("File System Watcher Stopped")


if __name__ == "__main__":
    run_watcher()

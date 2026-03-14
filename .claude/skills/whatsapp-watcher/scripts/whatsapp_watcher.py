#!/usr/bin/env python3
"""
WhatsApp Watcher for AI Employee
Monitors WhatsApp Web for urgent messages using Playwright automation
"""

import os
import sys
import time
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# Playwright imports
try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("Error: Playwright not installed.")
    print("Run: pip install playwright")
    print("Then: playwright install chromium")
    sys.exit(1)

# Configuration
VAULT_PATH = Path(__file__).parent / "AI_Employee_Vault"
NEEDS_ACTION = VAULT_PATH / "Needs_Action"
LOGS = VAULT_PATH / "Logs"
SESSION_PATH = Path(__file__).parent / "whatsapp_session"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOGS / "whatsapp_watcher.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("WhatsAppWatcher")


class WhatsAppWatcher:
    """Monitors WhatsApp Web for urgent messages"""

    def __init__(self, vault_path: Path = VAULT_PATH, check_interval: int = 30):
        self.vault_path = vault_path
        self.needs_action = vault_path / "Needs_Action"
        self.check_interval = check_interval
        self.session_path = SESSION_PATH

        # Urgent keywords to monitor
        self.keywords = ['urgent', 'asap', 'invoice', 'payment', 'help', 'emergency', 'critical']

        # Track processed messages
        self.processed_messages = set()

        # Ensure folders exist
        self.needs_action.mkdir(parents=True, exist_ok=True)
        LOGS.mkdir(parents=True, exist_ok=True)
        self.session_path.mkdir(parents=True, exist_ok=True)

    def check_for_updates(self, page) -> List[Dict]:
        """Check WhatsApp Web for urgent messages"""
        try:
            # Wait for chat list to load
            page.wait_for_selector('[data-testid="chat-list"]', timeout=10000)

            # Find unread chats
            unread_chats = page.query_selector_all('[aria-label*="unread"]')

            urgent_messages = []

            for chat in unread_chats[:10]:  # Check max 10 unread chats
                try:
                    # Get chat name
                    chat_name_elem = chat.query_selector('[dir="auto"]')
                    chat_name = chat_name_elem.inner_text() if chat_name_elem else "Unknown"

                    # Click to open chat
                    chat.click()
                    time.sleep(1)

                    # Get last message
                    messages = page.query_selector_all('[data-testid="msg-container"]')
                    if messages:
                        last_message = messages[-1]
                        message_text_elem = last_message.query_selector('.copyable-text span')
                        message_text = message_text_elem.inner_text() if message_text_elem else ""

                        # Check for urgent keywords
                        message_lower = message_text.lower()
                        matched_keywords = [kw for kw in self.keywords if kw in message_lower]

                        if matched_keywords:
                            # Create unique ID for this message
                            msg_id = f"{chat_name}_{message_text[:20]}_{int(time.time())}"

                            if msg_id not in self.processed_messages:
                                urgent_messages.append({
                                    'contact': chat_name,
                                    'message': message_text,
                                    'keywords': matched_keywords,
                                    'timestamp': datetime.now().isoformat(),
                                    'id': msg_id
                                })
                                self.processed_messages.add(msg_id)
                                logger.info(f"Urgent message from {chat_name}: {matched_keywords}")

                    # Go back to chat list
                    page.keyboard.press('Escape')
                    time.sleep(0.5)

                except Exception as e:
                    logger.warning(f"Error processing chat: {e}")
                    continue

            if urgent_messages:
                logger.info(f"Found {len(urgent_messages)} urgent message(s)")

            return urgent_messages

        except PlaywrightTimeout:
            logger.error("Timeout waiting for WhatsApp Web to load")
            return []
        except Exception as e:
            logger.error(f"Error checking for updates: {e}")
            return []

    def create_action_file(self, message: Dict) -> Optional[Path]:
        """Create action file for urgent WhatsApp message"""
        try:
            contact = message['contact']
            text = message['message']
            keywords = message['keywords']
            timestamp = int(time.time())

            # Create safe filename
            safe_contact = "".join(c for c in contact if c.isalnum() or c in (' ', '-', '_'))[:30]
            filename = f"WHATSAPP_{safe_contact.replace(' ', '_')}_{timestamp}.md"
            filepath = self.needs_action / filename

            # Create markdown content
            content = f"""---
type: whatsapp
from: {contact}
received: {message['timestamp']}
priority: high
status: pending
keywords_matched: {', '.join(keywords)}
---

# WhatsApp Message Received

## Message Content

{text}

## Suggested Actions

- [ ] Reply to sender
- [ ] Process request
- [ ] Create invoice/payment if needed
- [ ] Archive after handling

## Contact Details

- **From:** {contact}
- **Time:** {message['timestamp']}
- **Keywords:** {', '.join(keywords)}
- **Priority:** high

## Notes

Add processing notes here.

## ⚠️ Important

WhatsApp replies must be sent manually. This watcher is read-only.
"""

            filepath.write_text(content, encoding='utf-8')
            logger.info(f"Created action file: {filename}")

            # Log to audit trail
            self._log_action(message, filepath)

            return filepath

        except Exception as e:
            logger.error(f"Error creating action file: {e}")
            return None

    def _log_action(self, message: Dict, filepath: Path):
        """Log WhatsApp message detection to audit trail"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action_type": "whatsapp_message_detected",
            "actor": "whatsapp_watcher",
            "contact": message['contact'],
            "keywords": message['keywords'],
            "action_file": str(filepath),
            "status": "pending"
        }

        log_date = datetime.now().strftime("%Y-%m-%d")
        log_file = LOGS / f"{log_date}.json"

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

    def setup_session(self):
        """Initial setup - scan QR code"""
        logger.info("=" * 60)
        logger.info("WhatsApp Web Setup")
        logger.info("=" * 60)
        logger.info("Opening WhatsApp Web for QR code scan...")
        logger.info("Please scan the QR code with your phone")
        logger.info("=" * 60)

        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=str(self.session_path),
                headless=False
            )
            page = browser.pages[0]
            page.goto('https://web.whatsapp.com')

            # Wait for user to scan QR code
            logger.info("Waiting for QR code scan...")
            try:
                page.wait_for_selector('[data-testid="chat-list"]', timeout=120000)
                logger.info("✓ Successfully logged in!")
                logger.info("Session saved. You can now run the watcher.")
                time.sleep(3)
            except PlaywrightTimeout:
                logger.error("Timeout waiting for login. Please try again.")

            browser.close()

    def run(self, headless: bool = True):
        """Main watcher loop"""
        logger.info("=" * 60)
        logger.info("WhatsApp Watcher Started")
        logger.info("=" * 60)
        logger.info(f"Vault: {self.vault_path}")
        logger.info(f"Check interval: {self.check_interval} seconds")
        logger.info(f"Keywords: {', '.join(self.keywords)}")
        logger.info(f"Headless: {headless}")
        logger.info("=" * 60)

        with sync_playwright() as p:
            try:
                browser = p.chromium.launch_persistent_context(
                    user_data_dir=str(self.session_path),
                    headless=headless
                )
                page = browser.pages[0]
                page.goto('https://web.whatsapp.com')

                # Wait for initial load
                logger.info("Waiting for WhatsApp Web to load...")
                page.wait_for_selector('[data-testid="chat-list"]', timeout=30000)
                logger.info("✓ WhatsApp Web loaded successfully")

                # Main monitoring loop
                while True:
                    logger.info("Checking for urgent messages...")

                    # Check for urgent messages
                    messages = self.check_for_updates(page)

                    # Create action files
                    for message in messages:
                        self.create_action_file(message)

                    # Wait before next check
                    time.sleep(self.check_interval)

            except KeyboardInterrupt:
                logger.info("Stopping WhatsApp watcher...")
            except PlaywrightTimeout:
                logger.error("WhatsApp Web session expired. Please run --setup again.")
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
            finally:
                try:
                    browser.close()
                except:
                    pass
                logger.info("WhatsApp Watcher Stopped")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='WhatsApp Watcher for AI Employee')
    parser.add_argument('--interval', type=int, default=30,
                        help='Check interval in seconds (default: 30)')
    parser.add_argument('--setup', action='store_true',
                        help='Initial setup: scan QR code')
    parser.add_argument('--test', action='store_true',
                        help='Test mode: check once and exit')
    parser.add_argument('--headless', action='store_true',
                        help='Run browser in headless mode')

    args = parser.parse_args()

    watcher = WhatsAppWatcher(check_interval=args.interval)

    if args.setup:
        watcher.setup_session()
    elif args.test:
        logger.info("Running in test mode...")
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=str(watcher.session_path),
                headless=False
            )
            page = browser.pages[0]
            page.goto('https://web.whatsapp.com')
            page.wait_for_selector('[data-testid="chat-list"]', timeout=30000)
            messages = watcher.check_for_updates(page)
            logger.info(f"Found {len(messages)} urgent message(s)")
            for msg in messages:
                watcher.create_action_file(msg)
            browser.close()
        logger.info("Test complete")
    else:
        watcher.run(headless=args.headless)


if __name__ == "__main__":
    main()

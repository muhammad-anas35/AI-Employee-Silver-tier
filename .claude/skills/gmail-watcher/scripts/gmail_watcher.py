#!/usr/bin/env python3
"""
Gmail Watcher for AI Employee
Monitors Gmail inbox for important/unread emails and creates action files
"""

import os
import sys
import time
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# Gmail API imports
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("Error: Gmail API libraries not installed.")
    print("Run: pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    sys.exit(1)

# Configuration
VAULT_PATH = Path(__file__).parent.parent / "AI_Employee_Vault"
NEEDS_ACTION = VAULT_PATH / "Needs_Action"
LOGS = VAULT_PATH / "Logs"
CREDENTIALS_FILE = Path(__file__).parent.parent / "credentials.json"
TOKEN_FILE = Path(__file__).parent.parent / "token.json"
PROCESSED_FILE = Path(__file__).parent.parent / ".processed_emails"

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOGS / "gmail_watcher.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("GmailWatcher")


class GmailWatcher:
    """Monitors Gmail inbox for important emails"""

    def __init__(self, vault_path: Path = VAULT_PATH, check_interval: int = 120):
        self.vault_path = vault_path
        self.needs_action = vault_path / "Needs_Action"
        self.check_interval = check_interval
        self.service = None
        self.processed_ids = self._load_processed_ids()

        # Ensure folders exist
        self.needs_action.mkdir(parents=True, exist_ok=True)
        LOGS.mkdir(parents=True, exist_ok=True)

    def _load_processed_ids(self) -> set:
        """Load set of already processed email IDs"""
        if PROCESSED_FILE.exists():
            try:
                with open(PROCESSED_FILE, 'r') as f:
                    return set(json.load(f))
            except Exception as e:
                logger.warning(f"Could not load processed IDs: {e}")
        return set()

    def _save_processed_ids(self):
        """Save processed email IDs to avoid duplicates"""
        try:
            with open(PROCESSED_FILE, 'w') as f:
                json.dump(list(self.processed_ids), f)
        except Exception as e:
            logger.error(f"Could not save processed IDs: {e}")

    def authenticate(self):
        """Authenticate with Gmail API using OAuth2"""
        creds = None

        # Load existing token
        if TOKEN_FILE.exists():
            try:
                creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
            except Exception as e:
                logger.warning(f"Could not load token: {e}")

        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    logger.info("Token refreshed successfully")
                except Exception as e:
                    logger.error(f"Token refresh failed: {e}")
                    creds = None

            if not creds:
                if not CREDENTIALS_FILE.exists():
                    logger.error(f"Credentials file not found: {CREDENTIALS_FILE}")
                    logger.error("Please download OAuth2 credentials from Google Cloud Console")
                    sys.exit(1)

                flow = InstalledAppFlow.from_client_secrets_file(
                    str(CREDENTIALS_FILE), SCOPES
                )
                creds = flow.run_local_server(port=0)
                logger.info("New token obtained successfully")

            # Save credentials for next run
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())

        try:
            self.service = build('gmail', 'v1', credentials=creds)
            logger.info("Gmail API authenticated successfully")
        except Exception as e:
            logger.error(f"Failed to build Gmail service: {e}")
            sys.exit(1)

    def check_for_updates(self) -> List[Dict]:
        """Check Gmail for new important/unread emails"""
        try:
            # Query for unread important emails
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread is:important',
                maxResults=10
            ).execute()

            messages = results.get('messages', [])

            # Filter out already processed
            new_messages = [
                m for m in messages
                if m['id'] not in self.processed_ids
            ]

            if new_messages:
                logger.info(f"Found {len(new_messages)} new email(s)")

            return new_messages

        except HttpError as error:
            logger.error(f"Gmail API error: {error}")
            return []
        except Exception as e:
            logger.error(f"Error checking for updates: {e}")
            return []

    def get_email_details(self, message_id: str) -> Optional[Dict]:
        """Get full email details"""
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()

            # Extract headers
            headers = {}
            for header in message['payload'].get('headers', []):
                headers[header['name']] = header['value']

            # Get email body
            snippet = message.get('snippet', '')

            return {
                'id': message_id,
                'headers': headers,
                'snippet': snippet,
                'labels': message.get('labelIds', []),
                'internal_date': message.get('internalDate', '')
            }

        except Exception as e:
            logger.error(f"Error getting email details: {e}")
            return None

    def create_action_file(self, email: Dict) -> Optional[Path]:
        """Create action file for email"""
        try:
            headers = email['headers']
            from_addr = headers.get('From', 'Unknown')
            subject = headers.get('Subject', 'No Subject')
            date = headers.get('Date', '')

            # Create safe filename
            timestamp = int(time.time())
            safe_subject = "".join(c for c in subject if c.isalnum() or c in (' ', '-', '_'))[:50]
            filename = f"EMAIL_{safe_subject.replace(' ', '_')}_{timestamp}.md"
            filepath = self.needs_action / filename

            # Determine priority
            priority = 'high' if 'IMPORTANT' in email['labels'] else 'medium'

            # Check for urgent keywords
            urgent_keywords = ['urgent', 'asap', 'immediate', 'critical', 'emergency']
            if any(kw in subject.lower() or kw in email['snippet'].lower() for kw in urgent_keywords):
                priority = 'high'

            # Create markdown content
            content = f"""---
type: email
from: {from_addr}
subject: {subject}
received: {datetime.now().isoformat()}
priority: {priority}
status: pending
message_id: {email['id']}
labels: {', '.join(email['labels'])}
---

# Email Received

## Email Content

{email['snippet']}

## Suggested Actions

- [ ] Read full email content
- [ ] Draft reply
- [ ] Forward if needed
- [ ] Archive after processing

## Email Details

- **From:** {from_addr}
- **Subject:** {subject}
- **Date:** {date}
- **Priority:** {priority}
- **Labels:** {', '.join(email['labels'])}

## Notes

Add processing notes here.
"""

            filepath.write_text(content, encoding='utf-8')
            logger.info(f"Created action file: {filename}")

            # Log to audit trail
            self._log_action(email, filepath)

            return filepath

        except Exception as e:
            logger.error(f"Error creating action file: {e}")
            return None

    def _log_action(self, email: Dict, filepath: Path):
        """Log email detection to audit trail"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action_type": "email_detected",
            "actor": "gmail_watcher",
            "email_id": email['id'],
            "from": email['headers'].get('From', 'Unknown'),
            "subject": email['headers'].get('Subject', 'No Subject'),
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

    def run(self):
        """Main watcher loop"""
        logger.info("=" * 60)
        logger.info("Gmail Watcher Started")
        logger.info("=" * 60)
        logger.info(f"Vault: {self.vault_path}")
        logger.info(f"Check interval: {self.check_interval} seconds")
        logger.info("=" * 60)

        # Authenticate
        self.authenticate()

        try:
            while True:
                logger.info("Checking for new emails...")

                # Check for new emails
                messages = self.check_for_updates()

                # Process each new email
                for message in messages:
                    email = self.get_email_details(message['id'])
                    if email:
                        self.create_action_file(email)
                        self.processed_ids.add(message['id'])

                # Save processed IDs
                if messages:
                    self._save_processed_ids()

                # Wait before next check
                time.sleep(self.check_interval)

        except KeyboardInterrupt:
            logger.info("Stopping Gmail watcher...")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        finally:
            logger.info("Gmail Watcher Stopped")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Gmail Watcher for AI Employee')
    parser.add_argument('--interval', type=int, default=120,
                        help='Check interval in seconds (default: 120)')
    parser.add_argument('--test', action='store_true',
                        help='Test mode: check once and exit')

    args = parser.parse_args()

    watcher = GmailWatcher(check_interval=args.interval)

    if args.test:
        logger.info("Running in test mode...")
        watcher.authenticate()
        messages = watcher.check_for_updates()
        logger.info(f"Found {len(messages)} new email(s)")
        for msg in messages[:3]:  # Process max 3 in test mode
            email = watcher.get_email_details(msg['id'])
            if email:
                watcher.create_action_file(email)
        logger.info("Test complete")
    else:
        watcher.run()


if __name__ == "__main__":
    main()

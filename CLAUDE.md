# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Silver Tier** implementation of the Personal AI Employee hackathon project. It's an autonomous AI agent system that monitors Gmail, WhatsApp, and file systems, processes tasks using Claude Code, and manages workflows through an Obsidian vault.

**Architecture:** Local-first, agent-driven, human-in-the-loop automation system.

## Development Setup

### Prerequisites
- Python 3.13+
- Claude Code CLI
- Obsidian v1.10.6+
- Node.js v24+ (for MCP servers)

### Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Verify vault structure
python verify.py

# Configure environment variables
cp .env.template .env
# Edit .env with your credentials
```

### Environment Variables

Required in `.env`:
- `GMAIL_CLIENT_ID` - Gmail API OAuth2 client ID
- `GMAIL_CLIENT_SECRET` - Gmail API OAuth2 secret
- `VAULT_PATH` - Path to AI_Employee_Vault
- `DROP_FOLDER` - Path to file drop folder (default: ~/AI_Employee_Drop)

## Architecture

### Core Components

**1. Obsidian Vault** (`AI_Employee_Vault/`)
- Central knowledge base and task management system
- All state stored as markdown files
- Folders represent workflow stages

**2. Watchers** (Perception Layer)
- `filesystem_watcher.py` - Monitors drop folder for new files
- `gmail_watcher.py` - Monitors Gmail for important emails (Silver tier)
- `whatsapp_watcher.py` - Monitors WhatsApp for urgent messages (Silver tier)

**3. Claude Integration** (Reasoning Layer)
- `claude_integration.py` - VaultManager class for vault operations
- Reads tasks, creates plans, manages approvals
- Updates dashboard and logs actions

**4. Agent Skills** (`.claude/skills/`)
- `/process-vault-tasks` - Process tasks from Needs_Action
- `/update-dashboard` - Update Dashboard.md metrics
- `/send-email` - Send emails via MCP (Silver tier)
- `/post-linkedin` - Post to LinkedIn (Silver tier)
- `/check-approvals` - Process approval workflow (Silver tier)

**5. Orchestrator** (Silver tier)
- `orchestrator.py` - Master process coordinating all components
- Manages scheduling, folder watching, process health
- Triggers Claude Code at appropriate times

### Vault Folder Structure

```
AI_Employee_Vault/
├── Dashboard.md              # Real-time status dashboard
├── Company_Handbook.md       # Rules and boundaries
├── Inbox/                    # Manual file drops
├── Needs_Action/             # Tasks awaiting processing
├── Plans/                    # Generated action plans
├── Pending_Approval/         # Awaiting human approval
├── Approved/                 # Approved for execution
├── Rejected/                 # Rejected actions
├── Done/                     # Completed tasks
├── Accounting/               # Financial records
└── Logs/                     # Audit trail (JSON)
```

### Workflow

```
External Event → Watcher → /Needs_Action/TASK.md
                              ↓
                    Claude reads & analyzes
                              ↓
                    Creates /Plans/PLAN.md
                              ↓
              Sensitive? → /Pending_Approval/
                              ↓
                    Human reviews & approves
                              ↓
                    MCP executes action
                              ↓
                    Moves to /Done/ & logs
```

## Common Commands

### Start Watchers

```bash
# File system watcher (Bronze tier)
python filesystem_watcher.py

# Gmail watcher (Silver tier)
python .claude/skills/gmail-watcher/scripts/gmail_watcher.py

# WhatsApp watcher (Silver tier)
python .claude/skills/whatsapp-watcher/scripts/whatsapp_watcher.py

# Start all watchers via orchestrator (Silver tier)
python .claude/skills/orchestrator/scripts/orchestrator.py
```

### Process Tasks

```bash
# Process all pending tasks
claude /process-vault-tasks --vault-path "AI_Employee_Vault"

# Update dashboard
claude /update-dashboard --vault-path "AI_Employee_Vault"

# Send email (Silver tier)
claude /send-email --to "client@example.com" --subject "Invoice" --body "..."

# Post to LinkedIn (Silver tier)
claude /post-linkedin --content "Business update..."
```

### Verification

```bash
# Verify Bronze tier setup
python verify.py

# Check watcher status
ps aux | grep watcher

# View logs
tail -f AI_Employee_Vault/Logs/watcher.log
cat AI_Employee_Vault/Logs/2026-03-12.json | jq .
```

### Testing

```bash
# Test file drop
cp test.txt ~/AI_Employee_Drop/

# Test Gmail watcher (requires credentials)
python .claude/skills/gmail-watcher/scripts/gmail_watcher.py --test

# Test vault operations
python claude_integration.py
```

## Development Guidelines

### Adding New Watchers

1. Inherit from `BaseWatcher` class in `base_watcher.py`
2. Implement `check_for_updates()` and `create_action_file()`
3. Add to orchestrator process list
4. Document in SKILL.md

### Creating New Skills

1. Create folder in `.claude/skills/<skill-name>/`
2. Add `SKILL.md` with usage documentation
3. Implement skill logic (Python or Node.js)
4. Test with `claude /<skill-name>`

### Approval Workflow

**Auto-approve:**
- Reading emails/messages
- Creating drafts
- Organizing files
- Updating dashboard

**Always require approval:**
- Sending emails to new contacts
- Making payments
- Posting on social media
- Deleting files

### Security

- Never commit `.env` file
- Store credentials in environment variables only
- All sensitive actions require human approval
- Complete audit trail in `/Logs/`
- Rate limiting on external actions

### Error Handling

- Watchers use exponential backoff retry
- Failed tasks moved to `/Needs_Action` with error notes
- Orchestrator auto-restarts crashed watchers
- All errors logged to `/Logs/`

## File Naming Conventions

- Action files: `TYPE_description_timestamp.md`
  - `FILE_invoice_1234567890.md`
  - `EMAIL_client_request_1234567890.md`
  - `WHATSAPP_urgent_message_1234567890.md`
- Plan files: `PLAN_task_name_timestamp.md`
- Approval files: `ACTION_description_timestamp.md`
- Log files: `YYYY-MM-DD.json`

## Key Python Modules

### VaultManager (`claude_integration.py`)

```python
from claude_integration import VaultManager

vault = VaultManager()

# Read pending tasks
tasks = vault.read_needs_action()

# Create a plan
vault.create_plan("task_name", "objective", ["step1", "step2"])

# Request approval
vault.create_approval_request("payment", {"amount": "$100"}, "reason")

# Move to done
vault.move_to_done("path/to/file.md", "completion notes")

# Update dashboard
vault.update_dashboard({"pending_tasks": 5, "activity": "Processed invoice"})
```

### BaseWatcher Pattern

```python
from base_watcher import BaseWatcher

class MyWatcher(BaseWatcher):
    def check_for_updates(self) -> list:
        # Return list of new items
        pass

    def create_action_file(self, item) -> Path:
        # Create .md file in Needs_Action
        pass
```

## Troubleshooting

### Watcher not detecting files
- Check drop folder exists: `ls ~/AI_Employee_Drop/`
- Verify watcher is running: `ps aux | grep watcher`
- Check logs: `tail -f AI_Employee_Vault/Logs/watcher.log`

### Claude can't read vault
- Verify vault path in `.env`
- Check file permissions: `chmod -R 755 AI_Employee_Vault/`
- Test integration: `python claude_integration.py`

### Gmail API errors
- Verify OAuth2 credentials in `.env`
- Check token expiration
- Re-authenticate if needed

### Orchestrator crashes
- Check process logs in `/Logs/`
- Verify all dependencies installed
- Restart with `python orchestrator.py`

## Silver Tier Specific

### MCP Servers

Configure in `~/.config/claude-code/mcp.json`:

```json
{
  "servers": [
    {
      "name": "email",
      "command": "node",
      "args": ["/path/to/email-mcp/index.js"],
      "env": {
        "GMAIL_CREDENTIALS": "/path/to/credentials.json"
      }
    }
  ]
}
```

### Scheduling

```bash
# Linux/Mac cron
0 8 * * * cd /path/to/Silver && claude /process-vault-tasks
*/30 * * * * cd /path/to/Silver && claude /update-dashboard

# Windows Task Scheduler
# Create tasks pointing to claude.exe with skill arguments
```

### Human-in-the-Loop

1. Sensitive action detected
2. Claude creates file in `/Pending_Approval/`
3. Human reviews and moves to `/Approved/` or `/Rejected/`
4. Orchestrator detects approval and executes
5. Result logged and moved to `/Done/`

## References

- Hackathon Document: `Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md`
- Company Rules: `AI_Employee_Vault/Company_Handbook.md`
- Dashboard: `AI_Employee_Vault/Dashboard.md`
- Verification: `VERIFICATION_REPORT.md`

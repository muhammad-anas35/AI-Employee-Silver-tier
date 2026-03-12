# AI Employee - Bronze Tier Implementation

**Status:** ✅ Bronze Tier Foundation Complete
**Version:** 1.0
**Last Updated:** 2026-02-23

---

## 📋 Overview

This is a **Bronze Tier** implementation of the Personal AI Employee hackathon project. It provides the foundational architecture for an autonomous AI agent that manages personal and business tasks using Claude Code and Obsidian.

### What You Get

✅ **Obsidian Vault** - Local-first knowledge base with Dashboard and Company Handbook
✅ **File System Watcher** - Monitors a drop folder and creates action files
✅ **Claude Integration** - Python module for vault interaction
✅ **Agent Skills** - Reusable skills for task processing and dashboard updates
✅ **Audit Logging** - Complete action trail for transparency

---

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- Claude Code (installed and working)
- Obsidian (v1.10.6+)
- Git (optional, for version control)

### Installation

1. **Install Python dependencies:**
```bash
cd "D:\Coding world\Hackathone_0\Bronze"
pip install -r requirements.txt
```

2. **Verify the vault structure:**
```bash
ls -la AI_Employee_Vault/
```

You should see:
```
AI_Employee_Vault/
├── Dashboard.md
├── Company_Handbook.md
├── Inbox/
├── Needs_Action/
├── Plans/
├── Pending_Approval/
├── Approved/
├── Rejected/
├── Done/
├── Accounting/
└── Logs/
```

3. **Open Obsidian:**
   - Launch Obsidian
   - Click "Open folder as vault"
   - Navigate to `AI_Employee_Vault`
   - Click "Open"

4. **Start the File System Watcher:**
```bash
python filesystem_watcher.py
```

The watcher will create a drop folder at `~/AI_Employee_Drop`

---

## 📁 Project Structure

```
Bronze/
├── AI_Employee_Vault/              # Obsidian vault (local-first)
│   ├── Dashboard.md                # Real-time status dashboard
│   ├── Company_Handbook.md         # Rules and boundaries
│   ├── Inbox/                      # Incoming items
│   ├── Needs_Action/               # Tasks awaiting processing
│   ├── Plans/                      # Generated action plans
│   ├── Pending_Approval/           # Awaiting human approval
│   ├── Approved/                   # Approved for execution
│   ├── Rejected/                   # Rejected actions
│   ├── Done/                       # Completed tasks
│   ├── Accounting/                 # Financial records
│   └── Logs/                       # Audit trail (JSON)
│
├── .claude/skills/                 # Agent Skills
│   ├── process-vault-tasks/        # Process tasks from vault
│   ├── update-dashboard/           # Update dashboard metrics
│   └── browsing-with-playwright/   # Browser automation
│
├── filesystem_watcher.py           # File system monitoring
├── claude_integration.py           # Claude Code integration
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

## 🔄 Workflow

### 1. File Drop Detection

```
User drops file → Watcher detects → Creates action file in /Needs_Action
```

**Example:**
```bash
# Drop a file
cp invoice.pdf ~/AI_Employee_Drop/

# Watcher creates:
# AI_Employee_Vault/Needs_Action/FILE_invoice_123456.md
```

### 2. Task Processing

```
Action file → Claude reads → Creates plan → Requests approval → Executes
```

**Using the skill:**
```bash
claude /process-vault-tasks --vault-path "AI_Employee_Vault"
```

### 3. Approval Workflow

```
Sensitive action → Creates approval file → Human reviews → Moves to /Approved → Executes
```

**Example approval file:**
```markdown
---
type: approval_request
action: payment
---

# Approval Required: Payment

- **Amount:** $100
- **Recipient:** Client A
- **Reason:** Invoice #123

Move to /Approved to proceed.
```

### 4. Completion

```
Task executed → Logged → Moved to /Done → Dashboard updated
```

---

## 🛠️ Core Components

### Dashboard.md

Real-time status of your AI Employee:
- Key metrics (pending tasks, completed today)
- Recent activity log
- Active projects
- Financial summary
- System status

**Update it with:**
```bash
claude /update-dashboard --activity "Processed invoice from Client A"
```

### Company_Handbook.md

Rules and boundaries for autonomous decision-making:
- Permission boundaries (auto-approve vs. require approval)
- Communication guidelines
- Financial rules
- Task prioritization
- Escalation protocol
- Security requirements

**Reference it when:**
- Claude needs to make a decision
- You want to change approval thresholds
- You need to add new rules

### Vault Folders

| Folder | Purpose | Auto-Managed |
|--------|---------|--------------|
| `/Inbox` | Incoming items | No |
| `/Needs_Action` | Tasks awaiting processing | Yes (by watcher) |
| `/Plans` | Generated action plans | Yes (by Claude) |
| `/Pending_Approval` | Awaiting human approval | Yes (by Claude) |
| `/Approved` | Approved for execution | Manual (you move files) |
| `/Rejected` | Rejected actions | Manual (you move files) |
| `/Done` | Completed tasks | Yes (by Claude) |
| `/Logs` | Audit trail (JSON) | Yes (auto-logged) |

---

## 🔐 Security & Privacy

### Credential Management

Never store credentials in the vault. Use environment variables:

```bash
# Create .env file (add to .gitignore)
export GMAIL_API_KEY="your-key"
export BANK_API_TOKEN="your-token"
```

### Audit Logging

All actions are logged to `/Logs/YYYY-MM-DD.json`:

```json
{
  "timestamp": "2026-02-23T17:52:22Z",
  "action_type": "file_drop_detected",
  "actor": "filesystem_watcher",
  "source_file": "/path/to/file",
  "status": "pending"
}
```

### Permission Boundaries

From `Company_Handbook.md`:

**Auto-Approve:**
- Reading emails/messages
- Creating drafts
- Organizing files
- Updating dashboard

**Always Require Approval:**
- Sending emails to new contacts
- Making payments
- Posting on social media
- Deleting files

---

## 📊 Using the Watcher

### Start the Watcher

```bash
python filesystem_watcher.py
```

Output:
```
2026-02-23 17:52:22 - FileSystemWatcher - INFO - ============================================================
2026-02-23 17:52:22 - FileSystemWatcher - INFO - File System Watcher Started
2026-02-23 17:52:22 - FileSystemWatcher - INFO - Monitoring: /home/user/AI_Employee_Drop
2026-02-23 17:52:22 - FileSystemWatcher - INFO - Vault: /path/to/AI_Employee_Vault
2026-02-23 17:52:22 - FileSystemWatcher - INFO - ============================================================
```

### Drop a File

```bash
# Copy a file to the drop folder
cp myfile.txt ~/AI_Employee_Drop/

# Watcher detects it and creates:
# AI_Employee_Vault/Needs_Action/FILE_myfile_1708700342.md
```

### Check Logs

```bash
# View watcher logs
tail -f AI_Employee_Vault/Logs/watcher.log

# View daily audit log
cat AI_Employee_Vault/Logs/2026-02-23.json | jq .
```

---

## 🤖 Using Claude Integration

### Read Tasks

```python
from claude_integration import VaultManager

vault = VaultManager()
tasks = vault.read_needs_action()

for task in tasks:
    print(f"Task: {task['filename']}")
    print(f"Content: {task['content']}")
```

### Create a Plan

```python
vault.create_plan(
    task_name="invoice_processing",
    objective="Process and log invoice",
    steps=[
        "Extract invoice details",
        "Validate amounts",
        "Log transaction",
        "Archive file"
    ]
)
```

### Request Approval

```python
vault.create_approval_request(
    action_type="payment",
    details={
        "amount": "$100",
        "recipient": "Client A",
        "invoice": "#123"
    },
    reason="Invoice payment due"
)
```

### Move to Done

```python
vault.move_to_done(
    file_path="AI_Employee_Vault/Needs_Action/FILE_invoice_123.md",
    notes="Invoice processed and logged"
)
```

### Update Dashboard

```python
vault.update_dashboard({
    "pending_tasks": 3,
    "needs_action": 2,
    "completed_today": 5,
    "activity": "Processed invoice from Client A"
})
```

---

## 🎯 Agent Skills

### Process Vault Tasks

Automatically process tasks from `/Needs_Action`:

```bash
claude /process-vault-tasks --vault-path "AI_Employee_Vault"
```

**What it does:**
1. Scans `/Needs_Action` for new tasks
2. Analyzes each task
3. Creates a plan in `/Plans`
4. Requests approval if needed
5. Updates Dashboard.md

### Update Dashboard

Update metrics and activity:

```bash
claude /update-dashboard --metric "pending_tasks" --value 3
claude /update-dashboard --activity "Processed invoice"
```

**What it does:**
1. Reads current vault state
2. Calculates metrics
3. Updates Dashboard.md
4. Logs all changes

### Browser Automation (Playwright)

For Silver tier and beyond:

```bash
# Start Playwright server
bash .claude/skills/browsing-with-playwright/scripts/start-server.sh

# Use in Claude Code for web automation
# (See browsing-with-playwright/SKILL.md for details)
```

---

## 📝 Example Workflow

### Scenario: Process an Invoice

1. **Drop the file:**
```bash
cp invoice_client_a.pdf ~/AI_Employee_Drop/
```

2. **Watcher detects it:**
```
FILE_invoice_client_a_1708700342.md created in /Needs_Action
```

3. **Claude processes it:**
```bash
claude /process-vault-tasks
```

4. **Claude creates a plan:**
```
PLAN_invoice_processing_1708700342.md created in /Plans
```

5. **Claude requests approval:**
```
PAYMENT_client_a_1708700342.md created in /Pending_Approval
```

6. **You review and approve:**
```bash
# Move approval file to /Approved
mv AI_Employee_Vault/Pending_Approval/PAYMENT_*.md AI_Employee_Vault/Approved/
```

7. **Claude executes:**
```
Payment logged, files moved to /Done
Dashboard updated
```

8. **Check the logs:**
```bash
cat AI_Employee_Vault/Logs/2026-02-23.json | jq .
```

---

## 🐛 Troubleshooting

### Watcher not detecting files

```bash
# Check if drop folder exists
ls -la ~/AI_Employee_Drop/

# Check watcher logs
tail -f AI_Employee_Vault/Logs/watcher.log

# Restart watcher
# Ctrl+C to stop, then run again
python filesystem_watcher.py
```

### Claude Code not reading vault

```bash
# Verify vault path
ls -la AI_Employee_Vault/

# Check permissions
chmod -R 755 AI_Employee_Vault/

# Test integration
python claude_integration.py
```

### Logs not being created

```bash
# Ensure Logs folder exists
mkdir -p AI_Employee_Vault/Logs

# Check permissions
chmod 755 AI_Employee_Vault/Logs

# Restart watcher
```

### Obsidian not syncing

```bash
# Obsidian reads files directly from disk
# If changes don't appear, try:
# 1. Close and reopen the vault
# 2. Refresh the view (Ctrl+R)
# 3. Check file permissions
```

---

## 📚 Next Steps (Silver Tier)

Once Bronze is working, you can add:

1. **Gmail Watcher** - Monitor incoming emails
2. **WhatsApp Watcher** - Detect urgent messages
3. **LinkedIn Integration** - Auto-post content
4. **Email MCP Server** - Send emails automatically
5. **Scheduling** - Cron jobs for daily briefings
6. **Human-in-the-Loop** - Approval workflows

See the main hackathon document for Silver tier requirements.

---

## 📖 Documentation

- **Company_Handbook.md** - Rules and boundaries
- **Dashboard.md** - Real-time status
- **SKILL.md files** - Skill documentation
- **Logs/** - Audit trail

---

## 🤝 Support

For issues or questions:

1. Check `Company_Handbook.md` for rules
2. Review logs in `AI_Employee_Vault/Logs/`
3. Check the main hackathon document
4. Join the Wednesday research meeting

---

## 📄 License

This is part of the Personal AI Employee Hackathon 0 project.

---

**Built with:** Claude Code + Obsidian + Python
**Status:** Bronze Tier ✅
**Ready for:** Silver Tier Expansion 🚀

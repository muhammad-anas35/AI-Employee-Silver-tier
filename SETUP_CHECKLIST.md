# Silver Tier Setup Checklist

**Last Updated:** 2026-03-15

Use this checklist to verify all instructions and configurations are properly set before running the AI Employee system.

---

## ✅ Pre-Flight Checklist

### 1. Core Files & Structure
- [x] CLAUDE.md exists with complete instructions
- [x] .env.template exists with all required variables
- [x] Company_Handbook.md defines rules and boundaries
- [x] All 8 skills have SKILL.md with proper frontmatter
- [x] All 7 Python scripts in `.claude/skills/*/scripts/`
- [x] Vault structure complete (9 folders)
- [x] requirements.txt has all dependencies

### 2. Skill Configuration

#### Gmail Watcher
- [x] SKILL.md has frontmatter (name, description)
- [x] Script path: `.claude/skills/gmail-watcher/scripts/gmail_watcher.py`
- [x] Instructions in SKILL.md for OAuth2 setup
- [ ] Gmail API credentials configured in .env
- [ ] credentials.json downloaded from Google Cloud Console

#### WhatsApp Watcher
- [x] SKILL.md has frontmatter
- [x] Script path: `.claude/skills/whatsapp-watcher/scripts/whatsapp_watcher.py`
- [x] Instructions for QR code setup
- [ ] Playwright installed: `playwright install chromium`
- [ ] Session directory created

#### LinkedIn Poster
- [x] SKILL.md has frontmatter
- [x] Script path: `.claude/skills/linkedin-poster/scripts/linkedin_poster.py`
- [x] Approval workflow documented
- [ ] LinkedIn session configured
- [ ] Playwright installed

#### Send Email
- [x] SKILL.md has frontmatter
- [x] Script path: `.claude/skills/send-email/scripts/send_email.py`
- [x] Smart approval logic implemented
- [ ] known_contacts.json created
- [ ] Gmail API credentials configured

#### Orchestrator
- [x] SKILL.md has frontmatter
- [x] Script path: `.claude/skills/orchestrator/scripts/orchestrator.py`
- [x] Health monitoring implemented
- [x] Approval processing implemented
- [ ] All watcher dependencies installed

#### Process Vault Tasks
- [x] SKILL.md has frontmatter
- [x] Instructions for Claude Code integration
- [x] Documented in CLAUDE.md

#### Update Dashboard
- [x] SKILL.md has frontmatter
- [x] Instructions for dashboard updates
- [x] Documented in CLAUDE.md

#### Browsing with Playwright
- [x] SKILL.md has frontmatter
- [x] MCP server configuration documented
- [ ] MCP server configured in ~/.config/claude-code/mcp.json

### 3. Environment Configuration

#### .env File Setup
- [ ] Copy .env.template to .env
- [ ] Set VAULT_PATH
- [ ] Set DROP_FOLDER
- [ ] Set GMAIL_CLIENT_ID
- [ ] Set GMAIL_CLIENT_SECRET
- [ ] Set CHECK_INTERVAL
- [ ] Enable/disable watchers as needed
- [ ] Configure approval thresholds
- [ ] Set rate limits (MAX_EMAILS_PER_HOUR, MAX_POSTS_PER_DAY)

#### Vault Configuration
- [x] Dashboard.md exists
- [x] Company_Handbook.md defines rules
- [x] All workflow folders exist:
  - [x] Inbox/
  - [x] Needs_Action/
  - [x] Plans/
  - [x] Pending_Approval/
  - [x] Approved/
  - [x] Rejected/
  - [x] Done/
  - [x] Accounting/
  - [x] Logs/

### 4. Dependencies Installation

#### Python Packages
- [ ] `pip install -r requirements.txt`
- [ ] google-auth-oauthlib==1.2.0
- [ ] google-auth-httplib2==0.2.0
- [ ] google-api-python-client==2.116.0
- [ ] watchdog==4.0.0
- [ ] python-dotenv==1.0.0
- [ ] playwright==1.41.0
- [ ] psutil==5.9.8
- [ ] schedule==1.2.0

#### Additional Setup
- [ ] `playwright install chromium`
- [ ] Create drop folder: `mkdir ~/AI_Employee_Drop`

### 5. API & Authentication Setup

#### Gmail API
- [ ] Enable Gmail API in Google Cloud Console
- [ ] Create OAuth2 credentials
- [ ] Download credentials.json
- [ ] Run first authentication: `python .claude/skills/gmail-watcher/scripts/gmail_watcher.py --setup`
- [ ] Verify token.json created

#### WhatsApp Web
- [ ] Run setup: `python .claude/skills/whatsapp-watcher/scripts/whatsapp_watcher.py --setup`
- [ ] Scan QR code with phone
- [ ] Verify session saved

#### LinkedIn
- [ ] Run setup: `python .claude/skills/linkedin-poster/scripts/linkedin_poster.py --setup`
- [ ] Login manually
- [ ] Verify session saved

### 6. Documentation Verification

#### CLAUDE.md Completeness
- [x] Project overview
- [x] Development setup instructions
- [x] Architecture documentation
- [x] Vault folder structure
- [x] Workflow diagram
- [x] Common commands
- [x] Troubleshooting guide
- [x] All script paths use `.claude/skills/*/scripts/` pattern
- [x] Silver tier specific sections
- [x] MCP server configuration
- [x] Scheduling instructions
- [x] Human-in-the-loop workflow

#### Company_Handbook.md Completeness
- [x] Core values & principles
- [x] Permission boundaries (auto-approve, require approval)
- [x] Communication guidelines (email, WhatsApp, social media)
- [x] Financial rules & thresholds
- [x] Task management states
- [x] Prohibited actions
- [x] Escalation protocol
- [x] Reporting & auditing requirements
- [x] Security & privacy guidelines

### 7. Testing & Verification

#### Bronze Tier Tests
- [x] Run `python verify.py` (14/17 checks pass)
- [x] Test filesystem_watcher.py
- [x] Test claude_integration.py

#### Silver Tier Tests
- [ ] Test gmail_watcher.py with real credentials
- [ ] Test whatsapp_watcher.py with session
- [ ] Test linkedin_poster.py with session
- [ ] Test send_email.py with Gmail API
- [ ] Test orchestrator.py with all watchers
- [ ] Verify approval workflow (Pending_Approval → Approved → Done)
- [ ] Check dashboard updates
- [ ] Verify audit logging

### 8. Operational Readiness

#### Monitoring
- [ ] Set up cron jobs or Task Scheduler
- [ ] Configure log rotation
- [ ] Set up health check alerts
- [ ] Test auto-restart functionality

#### Security
- [x] .gitignore includes .env, credentials, tokens
- [ ] Credentials stored in environment variables only
- [ ] Audit logging enabled
- [ ] Rate limits configured
- [ ] Approval thresholds set appropriately

#### Documentation
- [x] README.md lists essential files
- [x] BRONZE_TIER_SUMMARY.md complete
- [x] SILVER_TIER_SUMMARY.md complete
- [x] TEST_RESULTS.md documents all tests
- [x] All duplicate files removed (11 files cleaned up)

---

## 🎯 Deployment Readiness Score

**Structure & Code:** 100/100 ✅
- All files in correct locations
- All skills properly implemented
- Clean project structure

**Documentation:** 100/100 ✅
- CLAUDE.md comprehensive
- Company_Handbook.md complete
- All skills documented

**Configuration:** 0/100 ⚠️
- .env needs to be created from template
- API credentials need to be configured
- Sessions need to be set up

**Dependencies:** 0/100 ⚠️
- Python packages need installation
- Playwright browsers need installation

**Testing:** 50/100 ⚠️
- Bronze tier tested
- Silver tier needs real credentials for full testing

---

## 🚀 Quick Start Commands

```bash
# 1. Install dependencies
pip install -r requirements.txt
playwright install chromium

# 2. Configure environment
cp .env.template .env
# Edit .env with your credentials

# 3. Set up Gmail API
python .claude/skills/gmail-watcher/scripts/gmail_watcher.py --setup

# 4. Set up WhatsApp (optional)
python .claude/skills/whatsapp-watcher/scripts/whatsapp_watcher.py --setup

# 5. Set up LinkedIn (optional)
python .claude/skills/linkedin-poster/scripts/linkedin_poster.py --setup

# 6. Verify setup
python verify.py

# 7. Start orchestrator
python .claude/skills/orchestrator/scripts/orchestrator.py
```

---

## ✅ Final Verification

Before going live, confirm:

- [ ] All checkboxes above are checked
- [ ] Test email sent successfully
- [ ] Test file drop processed
- [ ] Dashboard updates correctly
- [ ] Approval workflow tested
- [ ] Logs are being written
- [ ] All watchers running without errors
- [ ] Orchestrator health monitoring working

---

**Status:** Ready for deployment after configuration and dependency installation

**Next Steps:** Install dependencies → Configure APIs → Test → Deploy

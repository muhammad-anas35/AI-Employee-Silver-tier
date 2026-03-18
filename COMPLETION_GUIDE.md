# Silver Tier Implementation Completion Guide

**Date:** 2026-03-18
**Status:** Ready for Final Integration

## What Was Completed

### ✅ New Components Added

1. **base_watcher.py** - Abstract base class for all watchers
   - Standardized interface for all watchers
   - Built-in logging and error handling
   - Consistent run loop pattern

2. **retry_handler.py** - Exponential backoff retry logic
   - Decorator for automatic retries
   - Context manager for manual retry control
   - Configurable retry parameters

3. **rate_limiter.py** - Rate limiting system
   - Sliding window algorithm
   - Per-action type limits
   - Decorator support

4. **rate_limits.json** - Rate limit configuration
   - Email: 10/hour, 50/day
   - LinkedIn: 3/hour, 10/day
   - Payment: 3/hour, 10/day
   - API calls: 60/minute, 1000/hour

5. **mcp_config.json** - MCP server configuration
   - Filesystem MCP for vault access
   - Playwright MCP for browser automation
   - Ready to copy to Claude Code config

6. **Business_Goals.md** - Business tracking template
   - Revenue targets and metrics
   - Subscription audit rules
   - Risk management

7. **MCP_SETUP_GUIDE.md** - Complete MCP setup instructions
   - Step-by-step configuration
   - Troubleshooting guide
   - Testing procedures

8. **SILVER_TIER_GAP_ANALYSIS.md** - Comprehensive analysis
   - Identified all gaps
   - Completion percentages
   - Priority fixes

## Next Steps to Complete Silver Tier

### Phase 1: Refactor Watchers (2-3 hours)

#### 1.1 Update Gmail Watcher

**File:** `.claude/skills/gmail-watcher/scripts/gmail_watcher.py`

**Changes needed:**
```python
# Add at top
from base_watcher import BaseWatcher
from retry_handler import with_retry, TransientError
from rate_limiter import RateLimiter

# Change class definition
class GmailWatcher(BaseWatcher):  # Inherit from BaseWatcher
    def __init__(self, vault_path: Path = VAULT_PATH, check_interval: int = 120):
        super().__init__(str(vault_path), check_interval)
        self.service = None
        self.processed_ids = self._load_processed_ids()
        self.rate_limiter = RateLimiter()

    # Add retry decorator to API calls
    @with_retry(max_attempts=3, base_delay=2, exceptions=(HttpError,))
    def check_for_updates(self) -> List[Dict]:
        # Check rate limit
        if not self.rate_limiter.check_limit("gmail_api", "minute"):
            self.logger.warning("Gmail API rate limit reached")
            return []

        # Existing code...
```

#### 1.2 Update WhatsApp Watcher

**File:** `.claude/skills/whatsapp-watcher/scripts/whatsapp_watcher.py`

**Changes needed:**
```python
from base_watcher import BaseWatcher
from retry_handler import with_retry

class WhatsAppWatcher(BaseWatcher):
    def __init__(self, vault_path: str, session_path: str):
        super().__init__(vault_path, check_interval=30)
        self.session_path = Path(session_path)
        self.keywords = ['urgent', 'asap', 'invoice', 'payment', 'help']
```

#### 1.3 Update Filesystem Watcher

**File:** `filesystem_watcher.py`

**Changes needed:**
```python
from base_watcher import BaseWatcher

class FileSystemWatcher(BaseWatcher):
    def __init__(self, vault_path: Path, drop_folder: Path):
        super().__init__(str(vault_path), check_interval=5)
        self.drop_folder = drop_folder
        # Use watchdog for file monitoring
```

### Phase 2: Integrate Rate Limiting (1-2 hours)

#### 2.1 Update Email Sender

**File:** `.claude/skills/send-email/scripts/send_email.py`

**Add at top:**
```python
from rate_limiter import RateLimiter, rate_limited

class EmailSender:
    def __init__(self, vault_path: Path = VAULT_PATH):
        # Existing code...
        self.rate_limiter = RateLimiter()

    def send_email(self, to: str, subject: str, body: str, attachments=None):
        # Check rate limit before sending
        can_send, reason = self.rate_limiter.can_perform("email_send")
        if not can_send:
            logger.error(f"Cannot send email: {reason}")
            return False

        # Record action
        self.rate_limiter.record_action("email_send")

        # Existing send logic...
```

#### 2.2 Update LinkedIn Poster

**File:** `.claude/skills/linkedin-poster/scripts/linkedin_poster.py`

**Add rate limiting:**
```python
from rate_limiter import RateLimiter

class LinkedInPoster:
    def __init__(self, vault_path: Path = VAULT_PATH):
        # Existing code...
        self.rate_limiter = RateLimiter()

    def publish_post(self, post_file: Path, use_api: bool = False):
        # Check rate limit
        can_post, reason = self.rate_limiter.can_perform("linkedin_post")
        if not can_post:
            logger.error(f"Cannot post: {reason}")
            return False

        # Record action
        self.rate_limiter.record_action("linkedin_post")

        # Existing publish logic...
```

### Phase 3: Fix Orchestrator Integration (2-3 hours)

#### 3.1 Update Orchestrator to Call Claude Code

**File:** `.claude/skills/orchestrator/scripts/orchestrator.py`

**Changes needed:**
```python
def process_vault_tasks(self):
    """Trigger Claude to process vault tasks"""
    try:
        logger.info("Processing vault tasks...")

        # Check if there are tasks
        needs_action = self.vault_path / "Needs_Action"
        task_files = list(needs_action.glob("*.md"))

        if not task_files:
            logger.info("No tasks to process")
            return

        logger.info(f"Found {len(task_files)} task(s), triggering Claude Code...")

        # Actually call Claude Code skill
        result = subprocess.run(
            ["claude", "/process-vault-tasks"],
            cwd=str(self.vault_path.parent),
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes
        )

        if result.returncode == 0:
            logger.info("✓ Tasks processed successfully")
        else:
            logger.error(f"✗ Task processing failed: {result.stderr}")

    except subprocess.TimeoutExpired:
        logger.error("Task processing timed out")
    except Exception as e:
        logger.error(f"Error processing vault tasks: {e}")

def update_dashboard(self):
    """Update dashboard via Claude Code skill"""
    try:
        logger.info("Updating dashboard...")

        result = subprocess.run(
            ["claude", "/update-dashboard"],
            cwd=str(self.vault_path.parent),
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            logger.info("✓ Dashboard updated")
        else:
            logger.error(f"✗ Dashboard update failed: {result.stderr}")

    except Exception as e:
        logger.error(f"Error updating dashboard: {e}")
```

### Phase 4: Setup MCP Configuration (30 minutes)

#### 4.1 Copy MCP Config

**Windows:**
```bash
# Create directory
mkdir "C:\Users\manas\.config\claude-code"

# Copy config
copy mcp_config.json "C:\Users\manas\.config\claude-code\mcp.json"

# Edit paths in mcp.json to match your system
```

#### 4.2 Test MCP Servers

```bash
# Restart Claude Code
claude

# Test filesystem access
claude "List files in AI_Employee_Vault"

# Test Playwright (if installed)
claude "Open browser to linkedin.com"
```

### Phase 5: Update Requirements (15 minutes)

**File:** `requirements.txt`

**Add:**
```txt
# Existing requirements...

# Rate limiting (no external dependency needed - uses stdlib)

# Retry logic (no external dependency needed - uses stdlib)
```

### Phase 6: Update Documentation (30 minutes)

#### 6.1 Update CLAUDE.md

Add section on new components:

```markdown
## New Components (Silver Tier Complete)

### BaseWatcher
All watchers inherit from `base_watcher.BaseWatcher`:
- Standardized interface
- Built-in logging
- Consistent error handling

### Retry Logic
Use `@with_retry` decorator for transient failures:
```python
from retry_handler import with_retry

@with_retry(max_attempts=3, base_delay=1)
def api_call():
    # Your code
```

### Rate Limiting
Use `RateLimiter` to prevent excessive actions:
```python
from rate_limiter import RateLimiter

limiter = RateLimiter()
if limiter.can_perform("email_send")[0]:
    limiter.record_action("email_send")
    send_email()
```
```

#### 6.2 Update README.md

Add completion status:

```markdown
## Silver Tier Status: ✅ COMPLETE

All Silver Tier requirements implemented:
- ✅ BaseWatcher abstract class
- ✅ Retry logic with exponential backoff
- ✅ Rate limiting system
- ✅ MCP server configuration
- ✅ Orchestrator integration with Claude Code
- ✅ Business Goals template
- ✅ Comprehensive documentation
```

### Phase 7: Testing (1-2 hours)

#### 7.1 Test Watchers

```bash
# Test filesystem watcher
python filesystem_watcher.py

# Drop a test file
echo "Test" > ~/AI_Employee_Drop/test.txt

# Verify action file created in Needs_Action/
```

#### 7.2 Test Rate Limiting

```bash
# Run rate limiter tests
python rate_limiter.py

# Should show limits being enforced
```

#### 7.3 Test Retry Logic

```bash
# Run retry handler tests
python retry_handler.py

# Should show exponential backoff in action
```

#### 7.4 Test Orchestrator

```bash
# Start orchestrator
python .claude/skills/orchestrator/scripts/orchestrator.py

# Check logs
tail -f AI_Employee_Vault/Logs/orchestrator.log

# Verify it calls Claude Code skills
```

#### 7.5 End-to-End Test

1. Drop a file in drop folder
2. Verify watcher creates action file
3. Verify orchestrator triggers Claude Code
4. Verify Claude processes task
5. Verify task moves to Done/
6. Verify dashboard updates
7. Verify audit logs created

## Quick Start Commands

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Setup MCP config
copy mcp_config.json "C:\Users\manas\.config\claude-code\mcp.json"

# Verify vault structure
python verify.py
```

### Run System
```bash
# Start orchestrator (runs all watchers)
python .claude/skills/orchestrator/scripts/orchestrator.py

# Or run watchers individually
python filesystem_watcher.py
python .claude/skills/gmail-watcher/scripts/gmail_watcher.py
```

### Test Components
```bash
# Test rate limiter
python rate_limiter.py

# Test retry handler
python retry_handler.py

# Test base watcher (via actual watcher)
python filesystem_watcher.py --test
```

## Verification Checklist

- [ ] BaseWatcher class created
- [ ] Retry handler implemented
- [ ] Rate limiter implemented
- [ ] MCP config created
- [ ] Business Goals template added
- [ ] All watchers refactored to use BaseWatcher
- [ ] Rate limiting integrated in email sender
- [ ] Rate limiting integrated in LinkedIn poster
- [ ] Orchestrator calls Claude Code skills
- [ ] MCP config copied to Claude Code directory
- [ ] All tests passing
- [ ] Documentation updated
- [ ] End-to-end workflow tested

## Expected Results

After completing all phases:

1. **Watchers** will have consistent behavior and error handling
2. **Rate limiting** will prevent excessive API calls
3. **Retry logic** will handle transient failures gracefully
4. **Orchestrator** will actually trigger Claude Code to process tasks
5. **MCP servers** will enable Claude Code to interact with vault and browser
6. **Business tracking** will have foundation for Gold tier features

## Time Estimate

- Phase 1 (Refactor Watchers): 2-3 hours
- Phase 2 (Rate Limiting): 1-2 hours
- Phase 3 (Orchestrator): 2-3 hours
- Phase 4 (MCP Setup): 30 minutes
- Phase 5 (Requirements): 15 minutes
- Phase 6 (Documentation): 30 minutes
- Phase 7 (Testing): 1-2 hours

**Total: 7-11 hours**

## Success Criteria

Silver Tier is complete when:

1. All watchers inherit from BaseWatcher ✓
2. Retry logic handles transient failures ✓
3. Rate limiting prevents excessive actions ✓
4. Orchestrator successfully calls Claude Code skills ✓
5. MCP servers are configured and working ✓
6. End-to-end workflow completes successfully ✓
7. All audit logs are properly formatted ✓
8. Documentation is complete and accurate ✓

## Next: Gold Tier

Once Silver Tier is complete, you can begin Gold Tier features:
- Full accounting system (Odoo integration)
- Facebook/Instagram integration
- Twitter/X integration
- Weekly CEO briefing generation
- Ralph Wiggum loop for autonomous task completion
- Comprehensive error recovery
- Multi-platform social media management

## Support

If you encounter issues:
1. Check logs in `AI_Employee_Vault/Logs/`
2. Review `SILVER_TIER_GAP_ANALYSIS.md`
3. Consult `MCP_SETUP_GUIDE.md` for MCP issues
4. Check `CLAUDE.md` for architecture details

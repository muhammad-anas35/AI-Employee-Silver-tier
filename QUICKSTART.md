# Quick Start Guide - Bronze Tier

**Time to Complete:** 30 minutes
**Difficulty:** Beginner-Friendly

---

## ⚡ 5-Minute Setup

### Step 1: Install Dependencies
```bash
cd "D:\Coding world\Hackathone_0\Bronze"
pip install -r requirements.txt
```

### Step 2: Run Setup Script
```bash
# Windows
setup.bat

# Mac/Linux
bash setup.sh
```

### Step 3: Open Obsidian
1. Launch Obsidian
2. Click "Open folder as vault"
3. Select `AI_Employee_Vault`
4. Click "Open"

### Step 4: Start the Watcher
```bash
python filesystem_watcher.py
```

You should see:
```
2026-02-23 17:54:10 - FileSystemWatcher - INFO - File System Watcher Started
2026-02-23 17:54:10 - FileSystemWatcher - INFO - Monitoring: /home/user/AI_Employee_Drop
```

---

## 🧪 Test It Out (5 minutes)

### Test 1: Drop a File

```bash
# Create a test file
echo "This is a test invoice" > ~/AI_Employee_Drop/test_invoice.txt

# Watch the watcher detect it
# You should see in the terminal:
# 2026-02-23 17:54:15 - FileSystemWatcher - INFO - New file detected: test_invoice.txt
# 2026-02-23 17:54:15 - FileSystemWatcher - INFO - Created action file: FILE_test_invoice_1708700455.md
```

### Test 2: Check the Vault

In Obsidian:
1. Navigate to `Needs_Action` folder
2. You should see `FILE_test_invoice_1708700455.md`
3. Open it and review the content

### Test 3: Process the Task

```bash
claude /process-vault-tasks --vault-path "AI_Employee_Vault"
```

You should see:
- A new plan file created in `/Plans`
- Dashboard updated with activity
- Task moved to `/Done`

### Test 4: Check the Logs

```bash
# View the audit log
cat AI_Employee_Vault/Logs/2026-02-23.json | jq .

# You should see entries like:
# {
#   "timestamp": "2026-02-23T17:54:15Z",
#   "action_type": "file_drop_detected",
#   "actor": "filesystem_watcher",
#   "source_file": "/home/user/AI_Employee_Drop/test_invoice.txt",
#   "status": "pending"
# }
```

---

## 📋 Bronze Tier Checklist

Use this to verify you have everything:

### Vault Structure
- [ ] `AI_Employee_Vault/` folder exists
- [ ] `Dashboard.md` created and readable
- [ ] `Company_Handbook.md` created with rules
- [ ] All 10 subfolders created:
  - [ ] `/Inbox`
  - [ ] `/Needs_Action`
  - [ ] `/Plans`
  - [ ] `/Pending_Approval`
  - [ ] `/Approved`
  - [ ] `/Rejected`
  - [ ] `/Done`
  - [ ] `/Accounting`
  - [ ] `/Logs`

### Watcher Script
- [ ] `filesystem_watcher.py` created
- [ ] Dependencies installed (`watchdog`)
- [ ] Watcher starts without errors
- [ ] Drop folder created at `~/AI_Employee_Drop`
- [ ] Watcher detects new files
- [ ] Action files created in `/Needs_Action`
- [ ] Logs written to `/Logs/watcher.log`

### Claude Integration
- [ ] `claude_integration.py` created
- [ ] Can read tasks from `/Needs_Action`
- [ ] Can create plans in `/Plans`
- [ ] Can create approval requests
- [ ] Can move files to `/Done`
- [ ] Can update Dashboard.md
- [ ] Logs written to `/Logs/claude_integration.log`

### Agent Skills
- [ ] `/process-vault-tasks/SKILL.md` created
- [ ] `/update-dashboard/SKILL.md` created
- [ ] Skills are discoverable by Claude Code
- [ ] Skills have clear documentation

### Documentation
- [ ] `README.md` created with full guide
- [ ] `setup.sh` and `setup.bat` created
- [ ] `.env.template` created
- [ ] This quick start guide created

### Testing
- [ ] File watcher detects dropped files ✓
- [ ] Action files created correctly ✓
- [ ] Claude can read vault files ✓
- [ ] Plans created successfully ✓
- [ ] Dashboard updates work ✓
- [ ] Logs are being written ✓
- [ ] Obsidian opens vault without errors ✓

---

## 🎯 Common Tasks

### Drop a File for Processing
```bash
cp myfile.pdf ~/AI_Employee_Drop/
```

### Process All Pending Tasks
```bash
claude /process-vault-tasks --vault-path "AI_Employee_Vault"
```

### Update Dashboard Manually
```bash
claude /update-dashboard --activity "Completed invoice processing"
```

### View Recent Logs
```bash
tail -20 AI_Employee_Vault/Logs/watcher.log
```

### View Audit Trail
```bash
cat AI_Employee_Vault/Logs/2026-02-23.json | jq .
```

### Stop the Watcher
```bash
# Press Ctrl+C in the terminal where it's running
```

### Restart the Watcher
```bash
python filesystem_watcher.py
```

---

## 🔍 Troubleshooting

### "Module not found: watchdog"
```bash
pip install watchdog
```

### "Drop folder not created"
```bash
mkdir -p ~/AI_Employee_Drop
```

### "Watcher not detecting files"
1. Check drop folder exists: `ls ~/AI_Employee_Drop/`
2. Check watcher is running: Look for "File System Watcher Started"
3. Restart watcher: Ctrl+C, then `python filesystem_watcher.py`

### "Claude can't read vault"
1. Check vault path: `ls AI_Employee_Vault/`
2. Check permissions: `chmod -R 755 AI_Employee_Vault/`
3. Test integration: `python claude_integration.py`

### "Obsidian not showing new files"
1. Close and reopen the vault
2. Press Ctrl+R to refresh
3. Check file permissions

---

## 📚 Next Steps

### Immediate (Today)
- [ ] Complete setup
- [ ] Run all tests
- [ ] Drop a test file
- [ ] Process a task
- [ ] Review logs

### Short Term (This Week)
- [ ] Customize `Company_Handbook.md` with your rules
- [ ] Set up daily watcher monitoring
- [ ] Create a few test tasks
- [ ] Verify approval workflow works

### Medium Term (Next Week)
- [ ] Plan Silver tier additions
- [ ] Research Gmail API setup
- [ ] Plan WhatsApp automation
- [ ] Design LinkedIn integration

### Long Term (Next Month)
- [ ] Implement Silver tier features
- [ ] Add email automation
- [ ] Add social media posting
- [ ] Plan Gold tier features

---

## 💡 Tips & Tricks

### Organize Your Drop Folder
```bash
# Create subfolders for different types
mkdir ~/AI_Employee_Drop/{invoices,documents,reports}

# Drop files in appropriate folders
cp invoice.pdf ~/AI_Employee_Drop/invoices/
```

### Batch Process Files
```bash
# Drop multiple files at once
cp *.pdf ~/AI_Employee_Drop/

# Process all at once
claude /process-vault-tasks
```

### Monitor in Real-Time
```bash
# Watch logs as they're written
tail -f AI_Employee_Vault/Logs/watcher.log
```

### Backup Your Vault
```bash
# Create a backup
cp -r AI_Employee_Vault AI_Employee_Vault.backup

# Or use git
git add -A
git commit -m "Backup before changes"
```

---

## 🎓 Learning Resources

- **Main Document:** `Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md`
- **Rules:** `AI_Employee_Vault/Company_Handbook.md`
- **Status:** `AI_Employee_Vault/Dashboard.md`
- **Full Guide:** `README.md`

---

## ✅ You're Ready!

You now have a working Bronze tier AI Employee. It can:

✅ Monitor a drop folder for new files
✅ Create action files automatically
✅ Process tasks with Claude Code
✅ Create plans and approval requests
✅ Update a real-time dashboard
✅ Log all actions for audit trail
✅ Maintain local-first privacy

**Next:** Explore Silver tier features or customize your setup!

---

**Questions?** Check the README.md or Company_Handbook.md
**Ready for more?** See the main hackathon document for Silver tier

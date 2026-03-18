# MCP Server Setup Guide

## Overview

Model Context Protocol (MCP) servers allow Claude Code to interact with external systems. This guide covers setup for the Silver Tier implementation.

## Configuration File Location

**Windows:** `C:\Users\manas\.config\claude-code\mcp.json`
**Mac/Linux:** `~/.config/claude-code/mcp.json`

## Current MCP Servers

### 1. Filesystem MCP (Built-in)

**Purpose:** Access to Obsidian vault files

**Configuration:**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "D:\\Coding world\\Hackathone_0\\Silver\\AI_Employee_Vault"]
    }
  }
}
```

**Test:**
```bash
claude "Read the Dashboard.md file"
```

### 2. Playwright MCP (Browser Automation)

**Purpose:** WhatsApp and LinkedIn automation

**Configuration:**
```json
{
  "mcpServers": {
    "playwright": {
      "command": "node",
      "args": ["D:\\Coding world\\Hackathone_0\\Silver\\.claude\\skills\\browsing-with-playwright\\scripts\\mcp-server.js"],
      "env": {
        "HEADLESS": "false"
      }
    }
  }
}
```

**Prerequisites:**
```bash
npm install playwright
npx playwright install chromium
```

**Test:**
```bash
claude "Navigate to https://www.linkedin.com using Playwright"
```

## Setup Instructions

### Step 1: Create Config Directory

**Windows:**
```bash
mkdir -p "C:\Users\manas\.config\claude-code"
```

**Mac/Linux:**
```bash
mkdir -p ~/.config/claude-code
```

### Step 2: Copy Configuration

Copy the `mcp_config.json` from this project to the config directory:

**Windows:**
```bash
copy mcp_config.json "C:\Users\manas\.config\claude-code\mcp.json"
```

**Mac/Linux:**
```bash
cp mcp_config.json ~/.config/claude-code/mcp.json
```

### Step 3: Update Paths

Edit the `mcp.json` file and update paths to match your system:

1. Update vault path in filesystem server
2. Update Playwright script path
3. Update any credential paths

### Step 4: Restart Claude Code

```bash
# Exit any running Claude Code sessions
# Then start fresh
claude
```

### Step 5: Verify Setup

```bash
# List available MCP servers
claude --list-mcp-servers

# Test filesystem access
claude "List files in the vault"

# Test Playwright (if installed)
claude "Open a browser window"
```

## Future MCP Servers (Not Yet Implemented)

### Gmail MCP

**Status:** Planned
**Alternative:** Currently using Gmail API directly in Python

**Future Configuration:**
```json
{
  "email": {
    "command": "node",
    "args": ["/path/to/email-mcp/index.js"],
    "env": {
      "GMAIL_CREDENTIALS": "/path/to/credentials.json"
    }
  }
}
```

### Calendar MCP

**Status:** Planned for Gold Tier

**Future Configuration:**
```json
{
  "calendar": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-calendar"],
    "env": {
      "CALENDAR_API_KEY": "your-key"
    }
  }
}
```

### Slack MCP

**Status:** Planned for Gold Tier

**Future Configuration:**
```json
{
  "slack": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-slack"],
    "env": {
      "SLACK_TOKEN": "your-token"
    }
  }
}
```

## Troubleshooting

### MCP Server Not Found

**Error:** `MCP server 'filesystem' not found`

**Solution:**
1. Check config file exists at correct location
2. Verify JSON syntax is valid
3. Restart Claude Code
4. Check paths are absolute, not relative

### Permission Denied

**Error:** `Permission denied accessing vault`

**Solution:**
1. Check file permissions on vault folder
2. Ensure Claude Code has read/write access
3. On Windows, run as administrator if needed

### Playwright Not Working

**Error:** `Playwright browser not found`

**Solution:**
```bash
# Install Playwright browsers
npx playwright install chromium

# Verify installation
npx playwright --version
```

### Node.js Not Found

**Error:** `'node' is not recognized`

**Solution:**
1. Install Node.js v24+ from nodejs.org
2. Add Node.js to PATH
3. Restart terminal
4. Verify: `node --version`

## Security Notes

1. **Never commit MCP config with credentials**
   - Use environment variables for secrets
   - Add `mcp.json` to `.gitignore`

2. **Limit filesystem access**
   - Only grant access to vault directory
   - Don't use root directory

3. **Review MCP permissions**
   - Understand what each server can access
   - Use least privilege principle

## Testing MCP Servers

### Test Script

Create `test_mcp.py`:

```python
#!/usr/bin/env python3
import subprocess
import json

def test_mcp_server(server_name):
    """Test if MCP server is accessible"""
    try:
        result = subprocess.run(
            ["claude", "--list-mcp-servers"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if server_name in result.stdout:
            print(f"✓ {server_name} is configured")
            return True
        else:
            print(f"✗ {server_name} not found")
            return False

    except Exception as e:
        print(f"✗ Error testing {server_name}: {e}")
        return False

if __name__ == "__main__":
    servers = ["filesystem", "playwright"]

    print("Testing MCP Servers...")
    print("=" * 40)

    for server in servers:
        test_mcp_server(server)

    print("=" * 40)
```

Run test:
```bash
python test_mcp.py
```

## References

- [MCP Documentation](https://modelcontextprotocol.io)
- [Claude Code MCP Guide](https://docs.anthropic.com/claude/docs/mcp)
- [Available MCP Servers](https://github.com/modelcontextprotocol/servers)

## Next Steps

1. ✓ Setup filesystem MCP
2. ✓ Setup Playwright MCP
3. ⏳ Test with Claude Code
4. ⏳ Add Gmail MCP (future)
5. ⏳ Add Calendar MCP (Gold tier)

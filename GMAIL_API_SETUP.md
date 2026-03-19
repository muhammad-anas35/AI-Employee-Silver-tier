# Gmail API Setup Guide

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Name it (e.g., "AI Employee Gmail")
4. Click "Create"

## Step 2: Enable Gmail API

1. In your project, go to "APIs & Services" → "Library"
2. Search for "Gmail API"
3. Click on it and press "Enable"

## Step 3: Create OAuth2 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure OAuth consent screen:
   - User Type: External (for personal) or Internal (for workspace)
   - App name: "AI Employee"
   - User support email: your email
   - Developer contact: your email
   - Click "Save and Continue"
   - Scopes: Click "Add or Remove Scopes"
     - Add: `https://www.googleapis.com/auth/gmail.readonly`
     - Add: `https://www.googleapis.com/auth/gmail.send`
   - Click "Save and Continue"
   - Test users: Add your email
   - Click "Save and Continue"

4. Back to "Create OAuth client ID":
   - Application type: "Desktop app"
   - Name: "AI Employee Desktop"
   - Click "Create"

5. Download the credentials:
   - Click "Download JSON"
   - Save as `credentials.json` in your Silver folder

## Step 4: Configure .env

Update your `.env` file:

```bash
# Gmail API Configuration
GMAIL_CLIENT_ID="your_client_id_from_json"
GMAIL_CLIENT_SECRET="your_client_secret_from_json"
GMAIL_CREDENTIALS_PATH="./credentials.json"
GMAIL_TOKEN_PATH="./token.json"
```

**Note:** The `GMAIL_API_KEY` you have in .env is different - that's for simple API access. For Gmail reading/sending, you need OAuth2 credentials (client ID + secret).

## Step 5: First Authentication

Run the Gmail watcher setup to authenticate:

```bash
python .claude/skills/gmail-watcher/scripts/gmail_watcher.py --setup
```

This will:
1. Open a browser window
2. Ask you to login to Google
3. Grant permissions to the app
4. Save `token.json` for future use

## Step 6: Test

```bash
# Test Gmail watcher
python .claude/skills/gmail-watcher/scripts/gmail_watcher.py --test

# Test email sender
python .claude/skills/send-email/scripts/send_email.py --test
```

## Troubleshooting

### "Access blocked: This app's request is invalid"
- Make sure you added your email to "Test users" in OAuth consent screen
- App must be in "Testing" mode for external users

### "invalid_grant" error
- Delete `token.json` and re-authenticate
- Check that credentials.json is valid

### "insufficient permissions"
- Make sure you added both scopes:
  - `https://www.googleapis.com/auth/gmail.readonly`
  - `https://www.googleapis.com/auth/gmail.send`

## Security Notes

- Never commit `credentials.json` or `token.json` to git
- Both are already in `.gitignore`
- Rotate credentials monthly (set in .env: `CREDENTIAL_ROTATION_DAYS=30`)
- Use OAuth2 (not API keys) for Gmail access

## What You Get

After setup, you'll have:
- `credentials.json` - OAuth2 client credentials (download from Google)
- `token.json` - Access token (auto-generated on first auth)
- Gmail watcher monitoring your inbox
- Email sender with approval workflow

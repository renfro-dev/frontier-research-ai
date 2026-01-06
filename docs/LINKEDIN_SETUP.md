# LinkedIn Automation Setup Guide

Complete guide to setting up the automated LinkedIn posting system for Context Orchestration briefs.

## Overview

This system automatically:
1. Extracts 2-3 highlight posts from Context Orchestration briefs using Claude
2. Creates Google Docs for each post draft
3. Adds posts to a tracking spreadsheet with checkboxes
4. Publishes to LinkedIn when you check the approval box

## Prerequisites

- Python 3.8+ installed
- Supabase account (already configured)
- Anthropic API key (already configured)
- Google Cloud account
- LinkedIn company page access

---

## Part 1: Google Cloud Setup

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Note your project ID

### Step 2: Enable Required APIs

1. In Google Cloud Console, go to "APIs & Services" → "Library"
2. Enable these APIs:
   - **Google Docs API**
   - **Google Sheets API**
   - **Google Drive API**

### Step 3: Create Service Account

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Fill in details:
   - Name: `linkedin-automation`
   - Description: `Service account for automated LinkedIn posting`
4. Click "Create and Continue"
5. Skip optional steps, click "Done"

### Step 4: Create Service Account Key

1. Click on your newly created service account
2. Go to "Keys" tab
3. Click "Add Key" → "Create new key"
4. Choose "JSON" format
5. Click "Create" - a JSON file will download

### Step 5: Store Service Account Key

1. Create credentials directory:
   ```bash
   mkdir -p credentials
   ```

2. Move the downloaded JSON file:
   ```bash
   mv ~/Downloads/linkedin-automation-*.json credentials/google-service-account.json
   ```

3. Verify file exists:
   ```bash
   ls -la credentials/
   ```

---

## Part 2: LinkedIn API Setup

### Step 1: Create LinkedIn App

1. Go to [LinkedIn Developers](https://www.linkedin.com/developers/apps)
2. Click "Create app"
3. Fill in app details:
   - **App name**: Context Orchestration Posts
   - **LinkedIn Page**: Select your company page
   - **App logo**: Upload your logo (optional)
4. Check "I have read and agree to these terms"
5. Click "Create app"

### Step 2: Request Product Access

1. In your app dashboard, go to "Products" tab
2. Request access to:
   - **Share on LinkedIn** (required)
   - **Marketing Developer Platform** (if available)
3. Wait for approval (usually instant for "Share on LinkedIn")

### Step 3: Get OAuth Credentials

1. Go to "Auth" tab
2. Note your:
   - **Client ID**
   - **Client Secret** (click "Show" to reveal)

### Step 4: Generate Access Token

For initial setup, use LinkedIn's OAuth Playground:

1. Go to "Auth" tab
2. Scroll to "OAuth 2.0 settings"
3. Add redirect URL: `https://www.linkedin.com/developers/tools/oauth/redirect`
4. Click "Update"

5. Generate token using this URL (replace YOUR_CLIENT_ID):
   ```
   https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=https://www.linkedin.com/developers/tools/oauth/redirect&scope=w_organization_social%20rw_organization_admin
   ```

6. Visit the URL, authorize the app
7. Copy the `code` from the redirect URL
8. Exchange code for token using curl:
   ```bash
   curl -X POST https://www.linkedin.com/oauth/v2/accessToken \
     -H 'Content-Type: application/x-www-form-urlencoded' \
     -d 'grant_type=authorization_code' \
     -d 'code=YOUR_CODE' \
     -d 'redirect_uri=https://www.linkedin.com/developers/tools/oauth/redirect' \
     -d 'client_id=YOUR_CLIENT_ID' \
     -d 'client_secret=YOUR_CLIENT_SECRET'
   ```

9. Save the `access_token` and `refresh_token` from the response

### Step 5: Get Company URN

1. Go to your LinkedIn company page
2. Find the company ID in the URL (e.g., `linkedin.com/company/12345678`)
3. Your URN is: `urn:li:organization:12345678`

---

## Part 3: Configuration

### Step 1: Update .env File

Add these variables to your `.env` file:

```bash
# Google Workspace OAuth
GOOGLE_SERVICE_ACCOUNT_FILE=/absolute/path/to/credentials/google-service-account.json

# LinkedIn API
LINKEDIN_CLIENT_ID=your-linkedin-client-id
LINKEDIN_CLIENT_SECRET=your-linkedin-client-secret
LINKEDIN_ACCESS_TOKEN=your-access-token
LINKEDIN_REFRESH_TOKEN=your-refresh-token
LINKEDIN_COMPANY_URN=urn:li:organization:12345678

# Webhook Configuration
WEBHOOK_SECRET=generate-a-random-secret-key-here
WEBHOOK_PORT=5000
WEBHOOK_HOST=0.0.0.0

# Optional: Skip LinkedIn post generation
# SKIP_LINKEDIN_POSTS=1
```

### Step 2: Generate Webhook Secret

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the output and use it as `WEBHOOK_SECRET` in your `.env` file.

---

## Part 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `google-api-python-client` - Google Docs/Sheets API
- `google-auth-oauthlib` - Google OAuth
- `flask` - Webhook server
- `tenacity` - Retry logic

---

## Part 5: Database Migration

Run the migration to create the `linkedin_posts` table:

```bash
# If you have a migration runner script
python scripts/utils/run_migration.py migrations/005_linkedin_posts.sql

# Or run directly in Supabase SQL editor
# Copy contents of migrations/005_linkedin_posts.sql and run
```

Verify the table was created:
```sql
SELECT * FROM linkedin_posts LIMIT 1;
```

---

## Part 6: Test the System

### Test 1: Validate Configuration

```bash
python3 -c "from scripts.linkedin.config import Config; Config.validate(); print('✅ Configuration valid')"
```

### Test 2: Test LinkedIn API

```bash
python3 -c "from scripts.linkedin.linkedin_publisher import LinkedInPublisher; pub = LinkedInPublisher(); print('✅ Connection successful' if pub.test_connection() else '❌ Connection failed')"
```

### Test 3: Generate Posts (Dry Run)

```bash
python scripts/linkedin/generate_linkedin_posts.py --dry-run
```

This should:
- Load the latest brief
- Generate 2 LinkedIn posts
- Display previews
- NOT create any docs or database records

---

## Part 7: Deploy Webhook Server

You need a publicly accessible URL for the webhook. Choose one option:

### Option A: ngrok (for testing)

1. Install ngrok: https://ngrok.com/download
2. Start webhook server:
   ```bash
   python scripts/linkedin/webhook_listener.py
   ```
3. In another terminal, start ngrok:
   ```bash
   ngrok http 5000
   ```
4. Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

### Option B: Railway (recommended for production)

1. Install Railway CLI: https://railway.app/
2. Login: `railway login`
3. Create new project: `railway init`
4. Set environment variables in Railway dashboard
5. Deploy: `railway up`
6. Get URL from Railway dashboard

### Option C: Render

1. Create account at https://render.com/
2. Create new "Web Service"
3. Connect your GitHub repo
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `python scripts/linkedin/webhook_listener.py`
6. Add environment variables
7. Deploy and get URL

---

## Part 8: Configure Google Sheets Webhook

### Step 1: Generate First Post

Run the post generator:
```bash
python scripts/linkedin/generate_linkedin_posts.py
```

This creates:
- LinkedIn post records in database
- Google Docs for each post
- Tracking spreadsheet

### Step 2: Open Tracking Spreadsheet

Find the URL in the output (or in Google Drive: "LinkedIn Posts Tracker")

### Step 3: Add Apps Script

1. In the spreadsheet, go to **Extensions → Apps Script**
2. Delete any existing code
3. Copy contents of `scripts/linkedin/apps-script-webhook.gs`
4. Update these lines:
   ```javascript
   const WEBHOOK_URL = 'https://YOUR-WEBHOOK-URL-HERE/webhook/linkedin-post';
   const WEBHOOK_SECRET = 'your-secret-key-from-env';
   ```
5. **Save** the script (Ctrl+S or Cmd+S)

### Step 4: Test the Webhook

1. In Apps Script editor, select `testWebhook` function
2. Click **Run**
3. Check logs for success/error messages

---

## Part 9: Full System Test

### End-to-End Test

1. **Generate posts:**
   ```bash
   python scripts/linkedin/generate_linkedin_posts.py
   ```

2. **Start webhook server** (if not already running):
   ```bash
   python scripts/linkedin/webhook_listener.py
   ```

3. **Open tracking spreadsheet**
   - You should see your posts listed
   - Column A has Google Doc links
   - Column B has unchecked checkboxes

4. **Review a post:**
   - Click the Google Doc link in column A
   - Review and edit the post content

5. **Approve for posting:**
   - Back in the tracking sheet, check the box in column B
   - Watch column I (Status) change to "Processing..."
   - After ~5 seconds, status should change to "Posted"
   - Column H should show LinkedIn URL

6. **Verify on LinkedIn:**
   - Visit your company page
   - You should see the new post

---

## Part 10: Production Workflow

### Automated Brief → Posts

When a new Context Orchestration brief is generated:

1. `synthesis_agent_orchestration.py` runs (weekly cron job)
2. Automatically generates 2 LinkedIn posts
3. Creates Google Docs and updates tracking sheet
4. You receive notification (implement email/Slack as needed)
5. You review and approve posts by checking boxes
6. Posts automatically publish to LinkedIn

### Manual Control

To skip automatic post generation:
```bash
export SKIP_LINKEDIN_POSTS=1
python scripts/synthesis_agent_orchestration.py --start-date 2026-01-05 --end-date 2026-01-11
```

To generate posts manually later:
```bash
python scripts/linkedin/generate_linkedin_posts.py --brief-id <uuid>
```

---

## Troubleshooting

### "Configuration error: Missing required environment variables"

**Solution:** Ensure all variables are in `.env` file:
```bash
grep -E "GOOGLE_SERVICE_ACCOUNT_FILE|LINKEDIN_" .env
```

### "Google service account file not found"

**Solution:** Use absolute path in `.env`:
```bash
GOOGLE_SERVICE_ACCOUNT_FILE=/Users/YourName/Desktop/fun/Frontier AI/credentials/google-service-account.json
```

### "LinkedIn access token expired"

**Solution:** Refresh your token:
```python
from scripts.linkedin.linkedin_publisher import LinkedInPublisher
pub = LinkedInPublisher()
new_token = pub.refresh_access_token()
print(f"Update .env with: LINKEDIN_ACCESS_TOKEN={new_token}")
```

### Webhook not triggering

**Checklist:**
1. Webhook server is running: `curl http://localhost:5000/health`
2. Apps Script URL is correct (public HTTPS URL)
3. Webhook secret matches in Apps Script and `.env`
4. Check Apps Script logs: Executions → View logs

### Posts not appearing on LinkedIn

**Checklist:**
1. Company URN is correct
2. LinkedIn app has "Share on LinkedIn" product access
3. Access token has `w_organization_social` scope
4. Test connection: `LinkedInPublisher().test_connection()`

---

## Security Notes

- **Never commit** `.env` or `credentials/` directory
- **Rotate** LinkedIn access tokens every 60 days
- **Use HTTPS** for webhook server (required by Google Sheets)
- **Validate** webhook signatures in production
- **Monitor** LinkedIn API rate limits (100 posts/day per company page)

---

## Support

For issues:
1. Check logs: `tail -f logs/*.log`
2. Test individual components (see Test sections above)
3. Review webhook server logs: `python scripts/linkedin/webhook_listener.py` (shows requests)
4. Check Google Apps Script execution logs

---

## Next Steps

Once everything is working:

1. Set up monitoring/alerts for webhook failures
2. Add email notifications when posts are ready
3. Implement post scheduling (hold posts for specific times)
4. Add analytics tracking (engagement metrics)
5. Expand to other social platforms (Twitter, etc.)

Congratulations! Your LinkedIn automation system is now fully operational. 🎉

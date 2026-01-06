/**
 * Google Apps Script for LinkedIn Post Tracking Sheet
 *
 * This script triggers a webhook when the "Ready to Post" checkbox (Column B) is checked.
 *
 * SETUP INSTRUCTIONS:
 * 1. Open your LinkedIn Posts Tracker spreadsheet
 * 2. Extensions → Apps Script
 * 3. Delete any existing code and paste this script
 * 4. Update WEBHOOK_URL with your webhook server URL
 * 5. Update WEBHOOK_SECRET with your secret key from .env
 * 6. Save the script (Ctrl+S or Cmd+S)
 * 7. The script will automatically run when you check boxes in column B
 *
 * TROUBLESHOOTING:
 * - View logs: Execution log in Apps Script editor
 * - Test: Check a box and verify status updates in column I
 * - Check: Make sure webhook server is running
 */

// ============================================================================
// CONFIGURATION - UPDATE THESE VALUES
// ============================================================================

// Your webhook server URL (update after deploying webhook_listener.py)
// Examples:
//   - Local (ngrok): https://abc123.ngrok.io/webhook/linkedin-post
//   - Railway: https://your-app.railway.app/webhook/linkedin-post
//   - Render: https://your-app.onrender.com/webhook/linkedin-post
const WEBHOOK_URL = 'https://YOUR-WEBHOOK-URL-HERE/webhook/linkedin-post';

// Your webhook secret (must match WEBHOOK_SECRET in .env file)
const WEBHOOK_SECRET = 'your-secret-key-here';

// ============================================================================
// MAIN TRIGGER FUNCTION
// ============================================================================

/**
 * Trigger function that runs when any cell is edited
 *
 * This function is automatically called by Google Sheets when you edit a cell.
 * It checks if the edit was to the checkbox column, and if so, sends a webhook.
 */
function onEdit(e) {
  try {
    // Get the edited range info
    const range = e.range;
    const sheet = range.getSheet();
    const row = range.getRow();
    const col = range.getColumn();
    const value = range.getValue();

    // Only trigger on checkbox column (Column B = index 2)
    if (col !== 2) {
      return;
    }

    // Skip header row
    if (row === 1) {
      return;
    }

    // Only trigger when checkbox is checked (TRUE)
    if (value !== true) {
      return;
    }

    Logger.log(`Checkbox checked in row ${row}`);

    // Get row data
    const rowData = sheet.getRange(row, 1, 1, 9).getValues()[0];

    // Build webhook payload
    const payload = {
      doc_link: rowData[0],           // Column A: Google Doc Link
      ready_to_post: rowData[1],      // Column B: Ready to Post
      title: rowData[2],              // Column C: Post Title
      brief_source: rowData[3],       // Column D: Brief Source
      generated_date: rowData[4],     // Column E: Generated Date
      word_count: rowData[5],         // Column F: Word Count
      posted_date: rowData[6],        // Column G: Posted Date
      linkedin_url: rowData[7],       // Column H: LinkedIn URL
      status: rowData[8],             // Column I: Status
      row_number: row,
      spreadsheet_id: sheet.getParent().getId(),
      sheet_name: sheet.getName()
    };

    Logger.log('Payload: ' + JSON.stringify(payload));

    // Send webhook
    sendWebhook(payload, sheet, row);

  } catch (error) {
    Logger.log('ERROR in onEdit: ' + error.toString());

    // Try to update status column with error
    try {
      if (typeof row !== 'undefined' && typeof sheet !== 'undefined') {
        sheet.getRange(row, 9).setValue('Error - See logs');
      }
    } catch (updateError) {
      Logger.log('ERROR updating status: ' + updateError.toString());
    }
  }
}

/**
 * Send webhook to the Flask server
 */
function sendWebhook(payload, sheet, row) {
  try {
    // Validate configuration
    if (WEBHOOK_URL === 'https://YOUR-WEBHOOK-URL-HERE/webhook/linkedin-post') {
      sheet.getRange(row, 9).setValue('Error - Configure webhook URL');
      Logger.log('ERROR: WEBHOOK_URL not configured in Apps Script');
      return;
    }

    if (WEBHOOK_SECRET === 'your-secret-key-here') {
      sheet.getRange(row, 9).setValue('Error - Configure webhook secret');
      Logger.log('ERROR: WEBHOOK_SECRET not configured in Apps Script');
      return;
    }

    // Update status to "Processing"
    sheet.getRange(row, 9).setValue('Processing...');

    // Configure request
    const options = {
      method: 'post',
      contentType: 'application/json',
      headers: {
        'X-Webhook-Secret': WEBHOOK_SECRET
      },
      payload: JSON.stringify(payload),
      muteHttpExceptions: true  // Don't throw on HTTP errors
    };

    Logger.log('Sending webhook to: ' + WEBHOOK_URL);

    // Send request
    const response = UrlFetchApp.fetch(WEBHOOK_URL, options);
    const responseCode = response.getResponseCode();
    const responseText = response.getContentText();

    Logger.log('Response code: ' + responseCode);
    Logger.log('Response body: ' + responseText);

    // Handle response
    if (responseCode === 200) {
      // Success - webhook will update the status
      Logger.log('Webhook sent successfully');
      // Status will be updated by the webhook server
    } else if (responseCode === 401) {
      sheet.getRange(row, 9).setValue('Error - Unauthorized');
      Logger.log('ERROR: Webhook authentication failed (check WEBHOOK_SECRET)');
    } else if (responseCode >= 500) {
      sheet.getRange(row, 9).setValue('Error - Server error');
      Logger.log('ERROR: Webhook server error: ' + responseCode);
    } else {
      sheet.getRange(row, 9).setValue('Error - HTTP ' + responseCode);
      Logger.log('ERROR: Webhook failed: ' + responseCode);
    }

  } catch (error) {
    Logger.log('ERROR sending webhook: ' + error.toString());
    sheet.getRange(row, 9).setValue('Error - Network failure');
  }
}

/**
 * Test function - run this manually to test your webhook
 *
 * HOW TO USE:
 * 1. Click "Run" button in Apps Script editor
 * 2. Select "testWebhook" function
 * 3. Check logs to see if webhook was sent successfully
 */
function testWebhook() {
  Logger.log('=== TESTING WEBHOOK ===');

  // Create test payload
  const testPayload = {
    doc_link: 'https://docs.google.com/document/d/TEST123/edit',
    ready_to_post: true,
    title: 'Test Post',
    brief_source: 'Test Brief',
    generated_date: new Date().toISOString(),
    word_count: 150,
    posted_date: '',
    linkedin_url: '',
    status: 'Draft',
    row_number: 999,
    spreadsheet_id: 'TEST',
    sheet_name: 'Test'
  };

  Logger.log('Test payload: ' + JSON.stringify(testPayload));

  try {
    const options = {
      method: 'post',
      contentType: 'application/json',
      headers: {
        'X-Webhook-Secret': WEBHOOK_SECRET
      },
      payload: JSON.stringify(testPayload),
      muteHttpExceptions: true
    };

    Logger.log('Sending to: ' + WEBHOOK_URL);

    const response = UrlFetchApp.fetch(WEBHOOK_URL, options);
    const responseCode = response.getResponseCode();
    const responseText = response.getContentText();

    Logger.log('Response code: ' + responseCode);
    Logger.log('Response: ' + responseText);

    if (responseCode === 200) {
      Logger.log('✅ SUCCESS - Webhook is working!');
    } else {
      Logger.log('❌ FAILED - Response code: ' + responseCode);
    }

  } catch (error) {
    Logger.log('❌ ERROR: ' + error.toString());
    Logger.log('Check that:');
    Logger.log('1. WEBHOOK_URL is correct and server is running');
    Logger.log('2. WEBHOOK_SECRET matches your .env file');
    Logger.log('3. Server is publicly accessible (not localhost)');
  }

  Logger.log('=== TEST COMPLETE ===');
}

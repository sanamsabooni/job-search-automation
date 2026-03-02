# Job Search Automation with n8n and Google Gemini

> AI-powered job search automation that scrapes job boards, enhances listings with Google Gemini AI, and delivers organized results to Google Sheets.

## 🎯 Overview

This project automates job searching by:
- Fetching job listings from multiple sources (GitLab jobs via Greenhouse API)
- Using **Google Gemini AI** (free tier) to extract skills and enhance descriptions
- Storing results in Google Sheets for easy tracking
- Processing up to 20 jobs per search with keyword filtering

## ✨ Features

- **Interactive Form**: Popup form to enter job search keywords
- **Smart Filtering**: Searches top 20 relevant jobs based on keywords
- **AI Enhancement**: Google Gemini extracts skills and summarizes descriptions
- **Google Sheets Integration**: Automatic data storage with proper formatting
- **Zero Cost**: Uses free tiers of n8n (self-hosted), Gemini API, and Google Sheets

## 🏗️ Architecture

### Workflow Nodes:
1. **Form Trigger** → Collects keywords from user
2. **HTTP Request** → Fetches jobs from job boards
3. **Code/Loop** → Splits job array into individual items
4. **Edit Fields** → Extracts basic job data
5. **Google Gemini** → AI enhancement for skills/descriptions
6. **Google Sheets** → Stores results

## 📋 Prerequisites

- n8n instance (self-hosted or n8n cloud)
- Google account
- Google Gemini API key (free)

## 🚀 Setup Instructions

### 1. Get Google Gemini API Key (Free)

1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click **"Get API key"** → **"Create API key"**
4. Select or create a Google Cloud project
5. Copy your API key and save it securely

> 💡 The free tier includes generous rate limits perfect for job searching!

### 2. Set Up Google Sheets

1. Create a new Google Sheet named **"CRM"**
2. Create a tab named **"jobsearch-n8n-ai"**
3. Add column headers:
   - Job Title
   - Company
   - Location
   - Job URL
   - Description  
   - Date Posted
   - Skills
   - Application Status

### 3. Configure Google Cloud (for Sheets API)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable **Google Sheets API**
3. Enable **Google Drive API**
4. Create OAuth 2.0 credentials:
   - Application type: Web application
   - Add redirect URI: `https://YOUR-N8N-INSTANCE/rest/oauth2-credential/callback`
5. Save Client ID and Client Secret

### 4. Import n8n Workflow

**Current Working Workflow** (without Form/Gemini):
```
Schedule Trigger → HTTP Request → Edit Fields → Google Sheets
```

**Enhanced Workflow** (with Form + Gemini):
```
Form Trigger → HTTP Request → Code (Split) → Edit Fields → Google Gemini → Google Sheets
```

## 🔧 Detailed Node Configuration

### Form Trigger Node

1. Add **Form Trigger** node
2. Configure form fields:
   ```
   Field Name: keywords
   Field Type: Text
   Field Label: "Enter job search keywords (e.g., data analyst, python)"
   Required: Yes
   ```
3. Form Title: "Job Search Automation"
4. Form Description: "Enter keywords to find top 20 matching jobs"

### HTTP Request Node

```
Method: GET
URL: https://boards-api.greenhouse.io/v1/boards/gitlab/jobs
Query Parameters:
  - content: {{ $json.keywords }} (from Form)
```

### Code Node (Split Jobs Array)

```javascript
// Split the jobs array into individual items
const jobs = items[0].json.jobs || [];

// Return top 20 jobs
return jobs.slice(0, 20).map(job => ({
  json: { job }
}));
```

### Edit Fields Node

**Fields to Extract:**
- `job_title`: `{{ $json.job.title }}`
- `company`: "GitLab" (or dynamic from API)
- `location`: `{{ $json.job.location.name }}`
- `job_url`: `{{ $json.job.absolute_url }}`
- `date_posted`: `{{ $json.job.updated_at }}`

### Google Gemini Node

1. Add **HTTP Request** node for Gemini
2. Configure:
```
Method: POST
URL: https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent
Authentication: None
Headers:
  - Content-Type: application/json
  - x-goog-api-key: YOUR_GEMINI_API_KEY

Body (JSON):
{
  "contents": [{
    "parts": [{
      "text": "Extract key skills from this job posting and provide a brief 2-sentence summary. Job Title: {{ $json.job_title }}. Location: {{ $json.location }}. URL: {{ $json.job_url }}.  Format: Skills: [list]  Summary: [text]"
    }]
  }]
}
```

3. Add **Edit Fields** after Gemini to extract response:
```javascript
skills: {{ $json.candidates[0].content.parts[0].text.match(/Skills: (.+)/)[1] }}
description: {{ $json.candidates[0].content.parts[0].text.match(/Summary: (.+)/)[1] }}
```

### Google Sheets Node

**Operation**: Append Row
**Document**: CRM
**Sheet**: jobsearch-n8n-ai

**Column Mappings**:
- Job Title: `{{ $json.job_title }}`
- Company: `{{ $json.company }}`
- Location: `{{ $json.location }}`
- Job URL: `{{ $json.job_url }}`
- Description: `{{ $json.description }}` (from Gemini)
- Date Posted: `{{ $json.date_posted }}`
- Skills: `{{ $json.skills }}` (from Gemini)
- Application Status: "New"

## 📊 Current Status

✅ **Working Components:**
- HTTP Request fetching job data
- Edit Fields extracting job information
- Google Sheets integration
- Data successfully written to sheet

🚧 **To Be Added:**
- Form Trigger for keyword input
- Code node to split jobs array (process all 20 jobs)
- Google Gemini integration for AI enhancement

## 🎬 Usage

### Current Workflow:
1. Manually trigger workflow from n8n
2. Fetches GitLab jobs
3. Writes first job to Google Sheet

### Enhanced Workflow (After Setup):
1. Open workflow form URL
2. Enter job keywords (e.g., "automation engineer python")
3. Submit form
4. Workflow fetches top 20 matching jobs
5. Gemini AI extracts skills and summaries
6. All jobs saved to Google Sheet with AI insights

## 📝 Example Output

| Job Title | Company | Location | Skills | Description | Status |
|-----------|---------|----------|--------|-------------|--------|
| Accounts Receivable Associate | GitLab | Remote, Ireland | Excel, SAP, Finance | Manage accounts receivable processes... | New |

## 🔐 Security Notes

- Never commit API keys to Git
- Use n8n's credential system for sensitive data
- Gemini API key should be stored in n8n credentials
- OAuth tokens are managed securely by n8n

## 🐛 Troubleshooting

### "No columns found" in Google Sheets
- Ensure sheet has header row with column names
- Refresh the Google Sheets node configuration

### Gemini API Rate Limits
- Free tier: 60 requests/minute
- Add delay between requests if processing many jobs

### Job Array Not Splitting
- Check Code node has correct syntax
- Verify HTTP Request returns `jobs` array

## 🚀 Next Steps

1. Get Gemini API key from Google AI Studio
2. Add Form Trigger node
3. Add Code node to split jobs array
4. Add Gemini HTTP Request node
5. Test with keyword search
6. Monitor Google Sheet results

## 📚 Resources

- [Google Gemini API Docs](https://ai.google.dev/gemini-api/docs)
- [n8n Documentation](https://docs.n8n.io/)
- [Greenhouse API](https://developers.greenhouse.io/)
- [Google Sheets API](https://developers.google.com/sheets/api)

## 📄 License

MIT License - Feel free to use this for your job search!

## 🤝 Contributing

Contributions welcome! This is a portfolio project demonstrating workflow automation and AI integration.

---

**Built with:** n8n • Google Gemini AI • Google Sheets • Node.js

**Author:** Sanam Sabooni | [GitHub](https://github.com/sanamsabooni) | [Portfolio](https://sanamsabooni.github.io)

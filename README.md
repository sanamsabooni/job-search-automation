# Job Search Automation Pipeline

> AI-powered job search automation using n8n. Scrapes multiple job boards, scores listings with OpenAI, and delivers daily ranked results.

## Overview

This project automates the entire job search process by scraping job listings from multiple sources, scoring them using AI based on relevance criteria, and delivering a curated daily report of the best opportunities. Built with n8n, it demonstrates enterprise-grade workflow automation, API integration, and intelligent data processing.


## 🚀 Live Demo

**n8n Workflow**: [View Live Workflow](https://24748-6lmsk.irann8n.com/workflow/QejQEHHtRxQp8iuT)

The automated workflow is built and running in n8n. It includes:
- Schedule Trigger (runs daily at midnight)
- HTTP Request (scrapes GitLab jobs from Greenhouse API)
- OpenAI Integration (scores jobs based on relevance)


## What It Does

1. **Automated Job Discovery**
   - Scrapes LinkedIn Jobs and Greenhouse job boards daily at 9 AM
   - Searches for automation engineer positions across the United States
   - Extracts job title, company, location, description, salary, and application URL

2. **Data Processing & Storage**
   - Normalizes job data from different sources into a unified format
   - Stores all listings in a MySQL database
   - Prevents duplicate entries with upsert logic

3. **AI-Powered Scoring**
   - Uses OpenAI GPT-4 to evaluate each job listing
   - Scores jobs 1-10 based on:
     - Automation/workflow experience requirements
     - n8n, Python, or API integration skills
     - Remote work opportunities
     - Competitive salary ranges
   - Provides reasoning for each score

4. **Intelligent Filtering & Reporting**
   - Filters jobs with scores above 7/10
   - Ranks results by AI score
   - Sends a daily email report with top matches
   - Updates job scores in the database for tracking

## Architecture

```
┌─────────────────┐
│  Schedule       │ Trigger: Daily at 9 AM
│  Trigger        │
└────────┬────────┘
         │
         ├──────────────┬──────────────┐
         ▼              ▼              │
┌─────────────┐  ┌─────────────┐      │
│  LinkedIn   │  │ Greenhouse  │      │
│  Scraper    │  │  Scraper    │      │
└──────┬──────┘  └──────┬──────┘      │
       │                │             │
       └────────┬───────┘             │
                ▼                     │
       ┌────────────────┐             │
       │ Parse &        │             │
       │ Normalize      │             │
       └───────┬────────┘             │
               │                      │
       ┌───────┴────────┐             │
       ▼                ▼             │
┌──────────────┐  ┌──────────────┐   │
│   Store in   │  │  AI Scoring  │   │
│   Database   │  │  (OpenAI)    │   │
└──────────────┘  └──────┬───────┘   │
                         │           │
                         ▼           │
                ┌────────────────┐   │
                │ Extract &      │   │
                │ Rank Scores    │   │
                └───────┬────────┘   │
                        │            │
                ┌───────┴────────┐   │
                ▼                ▼   │
       ┌────────────────┐  ┌─────────────┐
       │ Filter High-   │  │  Update DB  │
       │ Priority Jobs  │  │  Scores     │
       └───────┬────────┘  └─────────────┘
               │
               ▼
       ┌────────────────┐
       │ Send Email     │
       │ Report         │
       └────────────────┘
```

## Features

- **Multi-Source Aggregation**: Combines jobs from LinkedIn, Greenhouse, and other boards
- **AI-Driven Relevance Scoring**: GPT-4 evaluates job fit based on custom criteria
- **Automated Daily Reports**: Email delivery of ranked job opportunities
- **Data Persistence**: MySQL database tracks all listings and scores
- **Duplicate Prevention**: Smart upsert logic prevents re-processing
- **Timezone Support**: Configured for America/Los_Angeles
- **Fully Autonomous**: Runs without manual intervention

## Technology Stack

- **n8n**: Workflow automation platform
- **OpenAI GPT-4**: Job scoring and relevance analysis
- **MySQL**: Relational database for job storage
- **MongoDB**: Document storage for job scores
- **Node.js**: Custom JavaScript code nodes
- **HTTP/REST APIs**: Job board integrations

## Setup Instructions

### Prerequisites

- n8n installed (self-hosted or cloud)
- MySQL database
- MongoDB database
- OpenAI API key
- Email SMTP credentials

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sanamsabooni/job-search-automation.git
   cd job-search-automation
   ```

2. **Set up the database**
   
   Create a MySQL database and table:
   ```sql
   CREATE DATABASE job_automation;
   
   USE job_automation;
   
   CREATE TABLE jobs (
     id INT AUTO_INCREMENT PRIMARY KEY,
     title VARCHAR(255) NOT NULL,
     company VARCHAR(255),
     location VARCHAR(255),
     description TEXT,
     url VARCHAR(512) UNIQUE,
     posted_date DATE,
     salary VARCHAR(100),
     source VARCHAR(50),
     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
   );
   ```

3. **Import the n8n workflow**
   
   - Open your n8n instance
   - Go to Workflows → Import from File
   - Select `workflows/job-search-workflow.json`

4. **Configure credentials in n8n**
   
   Set up the following credentials:
   - **MySQL**: Database connection (host, user, password, database)
   - **MongoDB**: Connection string
   - **OpenAI**: API key
   - **Email (SMTP)**: Your email service credentials

5. **Update workflow parameters**
   
   In the n8n workflow, customize:
   - Job search keywords (default: "automation engineer")
   - Location preferences
   - AI scoring criteria
   - Email recipient address
   - Schedule (default: daily at 9 AM)

6. **Activate the workflow**
   
   Click the "Active" toggle in n8n to start the automation.

## Usage

Once activated, the workflow runs automatically on schedule. You can also:

- **Manual Execution**: Click "Execute Workflow" in n8n to run immediately
- **Monitor Runs**: View execution history in the n8n UI
- **Check Database**: Query the `jobs` table to see all discovered listings
- **Adjust Scoring**: Modify the OpenAI prompt in the "AI Scoring" node

## Customization

### Change Job Search Criteria

Edit the "Scrape LinkedIn Jobs" and "Scrape Greenhouse Boards" nodes:
```javascript
{
  "keywords": "your keywords here",
  "location": "Your Location",
  "f_TP": "1,2"  // 1=Full-time, 2=Part-time
}
```

### Modify AI Scoring Logic

Update the prompt in the "AI Scoring with OpenAI" node:
```
Rate this job for relevance (1-10) based on:
- [Your custom criteria]
- [Another criterion]
- [etc.]

Provide score and brief reason.
```

### Add More Job Sources

Duplicate the scraper nodes and add new HTTP Request nodes targeting other job boards' APIs.

## Project Structure

```
job-search-automation/
├── workflows/
│   └── job-search-workflow.json    # Main n8n workflow
├── README.md                        # This file
└── .gitignore
```

## Troubleshooting

**Workflow not triggering**: Check the cron expression in the Schedule Trigger node.

**API errors**: Verify your OpenAI API key has sufficient credits.

**Database connection failed**: Confirm MySQL credentials and network access.

**No jobs found**: Check if job board URLs are still valid; APIs may change.

**Email not sending**: Verify SMTP credentials and check spam folder.

## Future Enhancements

- [ ] Add more job board sources (Indeed, Glassdoor, etc.)
- [ ] Web scraping for sites without APIs
- [ ] Resume auto-application for high-scoring jobs
- [ ] Slack/Discord notifications
- [ ] Analytics dashboard
- [ ] Machine learning for personalized scoring
- [ ] Mobile app integration

## Contributing

Contributions welcome! Please open an issue or submit a pull request.

## License

MIT License - see LICENSE file for details.

## Author

**Sanam Sabooni**  
Data Scientist & Automation Engineer  
[GitHub](https://github.com/sanamsabooni) | [Portfolio](https://sanamsabooni.github.io)

---

*Built with n8n, OpenAI, and automation expertise.*

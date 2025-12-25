# 🎬 Young Production - AI Context Document

> **Purpose**: This document provides complete context for AI assistants or developers to quickly understand and continue work on this project.
>
> **Last Updated**: 2025-12-25

---

## 📋 Project Overview

**Young Production** is an **automated YouTube video production pipeline** that integrates with Notion databases to manage the entire content creation workflow—from idea research to final video production.

### 🎯 Core Goals
1. **Automate video script generation** using viral content patterns
2. **Manage production workflow** through Notion databases
3. **Extract and learn from viral content** (perspectives, hooks, open loops)
4. **Track channel performance** and strategic growth

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        NOTION DATABASES                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌───────────────────┐  ┌───────────────┐  ┌─────────────────┐  │
│  │ Young Production  │  │   Viral DNA   │  │  Young Empire   │  │
│  │     Tracker       │  │  (Research)   │  │  (Analytics)    │  │
│  │  [Execution Hub]  │  │ [Learning Hub]│  │ [Strategy Hub]  │  │
│  └─────────┬─────────┘  └───────┬───────┘  └────────┬────────┘  │
│            │                    │                    │           │
│            └────────────────────┼────────────────────┘           │
│                                 │                                │
│                          ┌──────▼──────┐                         │
│                          │ Scene List  │                         │
│                          │ (Per Video) │                         │
│                          └─────────────┘                         │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PYTHON BACKEND                              │
│  • Notion API Integration                                        │
│  • Script Generation (Future: AI-powered)                        │
│  • Video Production Automation (Future)                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🗄️ Notion Database Schema

### 1. Young Production Tracker (Execution Engine)
**Purpose**: Track each video from idea to published status

| Property | Type | Purpose |
|----------|------|---------|
| Title | title | Video title/working name |
| Status | status | Workflow stage (Idea → Researching → Scripting → Rendering → Published) |
| Format | select | Video format (Shorts, Long-form, etc.) |
| *Related to Viral DNA* | relation | Research sources used |
| *Scene List* | relation | Linked scene breakdowns |

### 2. Viral DNA (Research & Learning Hub)
**Purpose**: Repository of viral content patterns, hooks, and insights

| Property | Type | Purpose |
|----------|------|---------|
| Title | title | Reference video/content title |
| Full Transcript | rich_text | Full content transcript |
| *Extracted Hooks* | rich_text | Opening hooks that grab attention |
| *Open Loop Seeds* | rich_text | Curiosity-building patterns |
| *Perspectives* | multi_select | Unique angles/viewpoints |

### 3. Young Empire (Strategy & Analytics)
**Purpose**: Multi-channel strategic analysis and performance tracking

| Property | Type | Purpose |
|----------|------|---------|
| Title | title | Channel/Report name |
| *Weekly/Monthly Reports* | rich_text | Performance summaries |
| *Prospecting Notes* | rich_text | New content ideas from Viral DNA |

### 4. Scene List (Per-Video Breakdown)
**Purpose**: Detailed scene-by-scene breakdown for each video

| Property | Type | Purpose |
|----------|------|---------|
| Title | title | Scene name/number |
| *Parent Video* | relation | Link to Production Tracker entry |
| *Visuals* | rich_text | Visual description |
| *Audio/Script* | rich_text | Voiceover/dialogue |

---

## 📁 File Structure

```
Young-Production/
├── PROJECT_CONTEXT.md      # This file - AI onboarding context
├── .gitignore              # Git ignore rules
├── backend/
│   ├── requirements.txt    # Python dependencies
│   ├── .env               # Environment variables (DO NOT COMMIT)
│   └── src/
│       ├── inspect_db.py      # 🔍 Schema inspector - run first to check DB structure
│       ├── check_connection.py # ✅ Connection test - verify API access
│       ├── manual_check.py     # 🧪 Manual test cases - create test pages
│       ├── clear_dbs.py        # 🗑️ Utility - archive all pages in DBs
│       └── debug_lib.py        # 🐛 Debug - inspect notion-client library
```

---

## 🔧 Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.x |
| Database | Notion (via API) |
| API Client | `notion-client` |
| HTTP Requests | `requests` |
| Environment | `python-dotenv` |
| Data Processing | `pandas` |
| Future API Server | `FastAPI` + `uvicorn` |

---

## ⚙️ Environment Setup

### Required `.env` Variables

Create a `.env` file in `backend/` with:

```env
# Notion API Configuration
NOTION_API_KEY=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Database IDs (get from Notion URL: notion.so/[DATABASE_ID]?v=...)
PROD_TRACKER_DB_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
VIRAL_DNA_DB_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
YOUNG_EMPIRE_DB_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SCENE_LIST_DB_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Notion Integration Setup
1. Go to [Notion Developers](https://www.notion.so/my-integrations)
2. Create a new integration
3. Copy the API key to `.env`
4. Share each database with your integration (click ••• → Add connections → Your Integration)

### Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

---

## 🚀 Quick Start Commands

```bash
# 1. Always run this first to check current DB schema
python src/inspect_db.py

# 2. Test API connection and permissions
python src/check_connection.py

# 3. Run manual test cases (creates test pages)
python src/manual_check.py

# 4. Clear all test data (archives pages)
python src/clear_dbs.py
```

---

## 📊 Current Progress

### ✅ Completed
- [x] Project structure setup
- [x] Notion API integration
- [x] Database schema inspector
- [x] Connection testing utilities
- [x] Basic CRUD operations for Notion pages
- [x] Multi-database support (4 databases)

### 🔄 In Progress
- [ ] Viral DNA extraction patterns
- [ ] AI-powered script generation
- [ ] Scene List automation

### 📋 Planned Features
- [ ] Workflow automation (status-triggered actions)
- [ ] AI integration for content generation
- [ ] Video production automation
- [ ] Analytics dashboard
- [ ] Webhook listeners for real-time updates

---

## 🔄 Typical Workflow

1. **Research Phase**
   - Add viral content to **Viral DNA** database
   - AI extracts hooks, perspectives, open loops

2. **Ideation Phase**
   - Create new entry in **Young Production Tracker**
   - Link relevant Viral DNA entries as research sources
   - Set status to "Idea"

3. **Scripting Phase**
   - Python detects "Ready to Script" status
   - Pulls patterns from linked Viral DNA entries
   - Generates script and populates Scene List

4. **Production Phase**
   - Scene List drives video generation
   - Status updates to "Rendering"

5. **Publishing Phase**
   - Final video URL updated in Tracker
   - Status set to "Published"
   - Analytics tracked in Young Empire

---

## 🐛 Common Issues & Solutions

### "Property X not found" errors
→ Run `python src/inspect_db.py` to check current schema
→ Property names are case-sensitive

### "Validation error" on Status property
→ Check if Status is `status` type vs `select` type
→ Use the correct API format:
  - For status type: `{"status": {"name": "Value"}}`
  - For select type: `{"select": {"name": "Value"}}`

### Connection refused
→ Check NOTION_API_KEY is correct
→ Ensure database is shared with your integration

---

## 📝 Notes for AI Assistants

When continuing work on this project:

1. **Always run `inspect_db.py` first** to get current schema
2. **Check property types** before making API calls
3. **The project uses direct HTTP requests** alongside notion-client
4. **UTF-8 encoding is forced** for Windows compatibility
5. **Database IDs come from Notion URLs** after the workspace name

---

## 📞 Quick Reference

| Action | File to Edit/Run |
|--------|------------------|
| Check DB schema | `inspect_db.py` |
| Test connection | `check_connection.py` |
| Create test entries | `manual_check.py` |
| Clear test data | `clear_dbs.py` |
| Add new DB support | Update `.env` + `inspect_db.py` |

---

*This context document should be updated as the project evolves.*

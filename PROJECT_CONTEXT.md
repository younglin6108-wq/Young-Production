# 🎬 Young Production - AI Context Document

> **Purpose**: This document provides complete context for AI assistants or developers to quickly understand and continue work on this project.
>
> **Last Updated**: 2025-12-26

---

## 📋 Project Overview

**Young Production** is an **automated YouTube video production pipeline** that integrates with Notion databases to manage the entire content creation workflow—from viral content research to final video production.

### 🎯 Core Goals
1. **Automate video script generation** using viral content patterns
2. **Manage production workflow** through Notion databases
3. **Extract and learn from viral content** (perspectives, hooks, open loops)
4. **Track channel performance** and strategic growth
5. **Minimize AI costs** through intelligent tool usage (OCR, local transcription, targeted AI)

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        NOTION DATABASES                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌───────────────────┐  ┌───────────────┐  ┌─────────────────┐  │
│  │ Young Production  │  │   Viral DNA   │  │  Young Empire   │  │
│  │     Tracker       │  │  (Research)   │  │  (Analytics)    │  │
│  │  [Execution Hub]  │  │ [Learning Hub]│  │ [Strategy Hub]  │  │
│  │                   │  │               │  │   + Writing     │  │
│  │  Contains:        │  │  Contains:    │  │     Style Docs  │  │
│  │  • Script (body)  │  │  • DNA data   │  │                 │  │
│  │  • Scene Table    │  │               │  │                 │  │
│  └─────────┬─────────┘  └───────┬───────┘  └────────┬────────┘  │
│            │                    │                    │           │
│            └────────────────────┼────────────────────┘           │
│                                 │                                │
│                          ┌──────▼──────┐                         │
│                          │ Scene List  │                         │
│                          │   (Global)  │                         │
│                          └─────────────┘                         │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PYTHON BACKEND                              │
│  • Notion API Integration (Read/Write Properties + Page Body)    │
│  • Content Transcription (yt-dlp + Whisper + OCR)               │
│  • AI-Powered Analysis (Claude: Haiku/Sonnet/Opus)              │
│  • Script Generation (AI + Viral DNA Patterns)                  │
│  • Workflow Orchestration (Manual CLI + State Management)       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🗄️ Notion Database Schema (Detailed)

### 1. Young Production Tracker (Execution Engine)
**Purpose**: Track each video from idea to published status

| Property | Type | Importance | Purpose | Used By |
|----------|------|------------|---------|---------|
| **Title** | title | 100 | Video title/working name | All workflows, user display |
| **Status** | status | 100 | Workflow stage driver | All workflows (triggers automation) |
| **Channel** | select | 95 | Channel assignment | WF3 (style), WF4 (reports) |
| **Format** | select | 90 | Video format (shorts/Video) | WF3 (script length) |
| **Viral DNA sources** | relation | 90 | Linked research sources | WF2 (linking), WF3 (script gen) |
| **Published Date** | date | 70 | Publish timestamp | WF4 (analytics) |
| **production URL** | url | 65 | YouTube video URL | WF4 (fetch stats) |
| **Production Date** | date | 50 | Recording/creation date | Timeline tracking |
| **Voice ID** | select | 45 | TTS voice selection | Future: voice synthesis |
| **Rendered File** | url | 40 | Local/cloud file path | Future: asset management |

**Status Flow**: `pending` → `Idea` → `Researching` → `DNA matching` → `Ready to Render` → `Done`

**Page Body Content** (written by workflows):
- **Script** (heading_2 + paragraphs): Full video script generated by WF3
- **Scene Breakdown** (table): Scene-by-scene breakdown with Visual/Audio columns

**Options**:
- **Status**: `['pending', 'Idea', 'Researching', 'DNA matching', 'Ready to Render', 'Done']`
- **Voice ID**: `['Drew', 'Adam', 'Rachel']`
- **Format**: `['shorts', 'Video']`
- **Channel**: `['next10yearz', 'orbity', 'BioVibe']`

---

### 2. Viral DNA (Research & Learning Hub)
**Purpose**: Repository of viral content patterns, hooks, and insights

| Property | Type | Importance | Purpose | Used By |
|----------|------|------------|---------|---------|
| **Title** | title | 100 | Content reference name | All workflows, user display |
| **URL** | url | 95 | Source URL (YouTube/IG/Web) | S18 (scraper), S04 (transcribe) |
| **Extracted Perspective** | rich_text | 95 | AI-generated analysis (merit) | WF3 (script gen), WF5 (prospecting) |
| **Hook Potential** | rich_text | 90 | AI-extracted opening hooks | WF3 (script gen) |
| **Open Loop Seed** | rich_text | 90 | Curiosity-building patterns | WF3 (script gen) |
| **Tags (niche)** | multi_select | 85 | Content categorization | WF2 (DNA→Production linking) |
| **Info Type** | multi_select | 80 | Content format classification | S04 (determines transcribe method) |
| **Productions** | relation | 75 | Backlink to videos using this DNA | Usage tracking |
| **Creator** | rich_text | 50 | Original content creator | Empire competitor analysis (future) |

**Options**:
- **Info Type**: `['Reel (Audio)', 'Reel (Visual Only)', 'Carousel', 'Static Post', 'Youtube Short', 'Long Video']`
- **Tags (niche)**: Dynamic (user-created)

**Processing Rules**:
- **Reel (Audio) / YouTube Short / Long Video**: yt-dlp + Whisper transcription + IG description extraction
- **Reel (Visual Only)**: Video OCR (extract on-screen text) + visual description AI + IG description
- **Carousel / Static Post**: Image OCR + visual analysis + IG description

---

### 3. Young Empire (Strategy & Analytics Hub)
**Purpose**: Multi-channel strategic analysis and performance tracking

| Property | Type | Importance | Purpose | Used By |
|----------|------|------------|---------|---------|
| **Report Title** | title | 100 | Report identifier | All empire workflows |
| **Status** | status | 95 | Report completion stage | WF4, WF5 triggers |
| **Channel** | select | 95 | Channel being analyzed | WF4 (filter Productions) |
| **Year** | select | 80 | Reporting year | Time-based filtering |
| **Month** | select | 75 | Reporting month | WF4 (monthly reports) |
| **Week** | select | 75 | Reporting week (W1-W4) | WF4 (weekly reports) |

**Status Flow**: `Not started` → `Drafting` → `Published`

**Options**:
- **Status**: `['Not started', 'Drafting', 'Published']`
- **Year**: `['2026']`
- **Month**: `['January', 'Feburary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']`
- **Channel**: `['next10yearz', 'Orbity', 'BioVibe']`
- **Week**: `['W1', 'W2', 'W3', 'W4']`

**Page Body Content** (written by workflows):
- **Writing Style Engine** (per-channel guide): See "Writing Style Format" section below
- **Reviewing Section**: Performance analysis (WF4)
- **Prospecting Section**: New content ideas (WF5)

---

### 4. Global Scene List (Production Assets)
**Purpose**: Scene-by-scene breakdown for each video (script-level, not asset-level)

| Property | Type | Importance | Purpose | Used By |
|----------|------|------------|---------|---------|
| **Name** | title | 100 | Scene identifier (e.g., "Scene 1") | User display, ordering |
| **Production** | relation | 100 | Parent video link | All scene queries |
| **Script** | rich_text | 95 | Voiceover/dialogue text | Video production |
| **Visual Prompt** | rich_text | 95 | Scene visual description | AI image/video generation |
| **Status** | status | 85 | Asset readiness (Pending/Downloading/Error/Ready) | Asset pipeline tracking |
| **Source** | select | 80 | Asset source type | Determines download method |
| **Source URL** | url | 75 | Original asset URL (if applicable) | Asset downloader |
| **Asset Path** | rich_text | 70 | Local file path after download | Video editor |
| **Duration (sec)** | number | 65 | Scene length in seconds | Timeline calculation |
| **Source Timestamp** | rich_text | 45 | YouTube clip time range (e.g., "1:23-1:45") | Clip extraction |

**Options**:
- **Status**: `['Pending', 'Downloading', 'Error', 'Ready']`
- **Source**: `['Pexels', 'Youtube', 'Manual', 'B-Roll Library', 'AI-Generate']`
- **Channel**: REMOVED (redundant - use Production.Channel)

**Note**: Scene List is created by WF3.1 after script generation, NOT during asset rendering phase.

---

## 📐 Writing Style Format (Stored in Young Empire Page Body)

Each channel has a Writing Style guide stored in a Young Empire page (per-channel). Format:

```markdown
# 🧠 Writing Style Engine
Last Updated: YYYY-MM-DD

---

## 🎯 Core Identity (The "Why")
- **Tone**: [e.g., "Conversational, slightly provocative, never condescending"]
- **Audience Avatar**: [e.g., "27-year-old creative professional, tired of hustle culture"]
- **Content Philosophy**: [e.g., "Make the viewer feel smarter, not inferior"]

---

## 🪝 Hook Library (Proven Patterns)
| Pattern | Example | Source (Viral DNA Link) |
|---------|---------|-------------------------|
| Contrarian Claim | "Most productivity advice is making you slower." | VD-001 |
| Specific Number | "I tried 47 apps so you don't have to." | VD-015 |
| Identity Challenge | "If you're still using to-do lists, you're stuck in 2015." | VD-022 |

---

## 🔁 Open Loop Techniques
- **Question Plant**: Ask a question in the first 5 seconds, answer at 60%.
- **Preview Tease**: "I'll show you the tool that changed everything... but first."
- **Contrast Setup**: "Here's what everyone does [WRONG]. Here's what actually works."

---

## ⚠️ Anti-Patterns (Things to Avoid)
- Never start with "Hey guys"
- Avoid passive voice in the first 3 sentences
- Don't use more than 2 jargon terms per minute

---

## 📈 Iteration Log
| Date | Lesson | Source | Action Taken |
|------|--------|--------|--------------|
| 2024-12-20 | Shorter sentences in hooks perform better | Video #12 | Updated Hook Library |
```

**Retention Formula**: `retention = (pacing + open loops) / cognitive load`

---

## 📁 File Structure

```
Young-Production/
├── PROJECT_CONTEXT.md           # This file - AI onboarding context
├── TECHNICAL_SPEC.md            # Detailed skill/workflow specifications
├── ARCHITECTURE.md              # System design and module structure
├── IMPLEMENTATION_CHECKLIST.md  # Phased build order
├── .gitignore                   # Git ignore rules
├── backend/
│   ├── requirements.txt         # Python dependencies
│   ├── .env                     # Environment variables (DO NOT COMMIT)
│   ├── venv/                    # Virtual environment (DO NOT COMMIT)
│   ├── config/                  # Configuration files
│   │   ├── databases.yaml       # DB schema mappings
│   │   ├── ai_config.yaml       # AI model selection + cost limits
│   │   └── prompts/             # AI prompt templates
│   │       ├── extract_perspective.txt
│   │       ├── generate_hook.txt
│   │       ├── generate_script.txt
│   │       └── ...
│   ├── state/                   # Workflow state (DO NOT COMMIT)
│   │   ├── last_run.json
│   │   ├── workflow_history.json
│   │   └── ai_costs.json
│   ├── src/
│   │   ├── core/                # Core modules
│   │   │   ├── notion_client.py
│   │   │   ├── ai_client.py
│   │   │   └── config_loader.py
│   │   ├── skills/              # Atomic functions (S01-S21+)
│   │   │   ├── crud.py          # S01-S03
│   │   │   ├── transcription.py # S04, S18
│   │   │   ├── ai_analysis.py   # S05-S07, S09
│   │   │   ├── classification.py # S08
│   │   │   ├── analytics.py     # S10-S11
│   │   │   ├── reporting.py     # S13
│   │   │   └── production.py    # S14-S16, S19-S21
│   │   ├── workflows/           # Workflow orchestrators (WF1-WF6)
│   │   │   ├── wf1_viral_dna_encoding.py
│   │   │   ├── wf2_dna_linking.py
│   │   │   ├── wf3_script_generation.py
│   │   │   ├── wf4_empire_review.py
│   │   │   └── wf5_empire_prospecting.py
│   │   ├── utils/               # Utilities
│   │   │   ├── logger.py
│   │   │   ├── state_manager.py
│   │   │   └── cost_tracker.py
│   │   ├── inspect_db.py        # 🔍 Schema inspector
│   │   ├── check_connection.py  # ✅ Connection test
│   │   ├── manual_check.py      # 🧪 Manual test cases
│   │   ├── clear_dbs.py         # 🗑️ Clear test data
│   │   └── run.py               # 🚀 Main CLI entry point
│   └── tests/                   # Unit tests
│       ├── test_skills.py
│       └── test_workflows.py
```

---

## 🔧 Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Language | Python 3.12+ | Backend logic |
| Database | Notion API | Data storage + UI |
| Notion Client | `notion-client` + `requests` | DB access + page body manipulation |
| AI Provider | Anthropic Claude (Haiku/Sonnet/Opus) | Content analysis + generation |
| Transcription | `yt-dlp` + `faster-whisper` | Audio extraction + local transcription |
| OCR | `pytesseract` + `easyocr` | Text extraction from images/video |
| Image Processing | `Pillow` + `opencv-python` | Image manipulation for OCR |
| HTTP Requests | `requests` | API calls, web scraping |
| Environment | `python-dotenv` | Config management |
| Data Processing | `pandas` | Analytics (WF4) |
| YAML Parser | `pyyaml` | Config file parsing |
| CLI Framework | `click` or `typer` | Interactive CLI |

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

# AI Configuration (Anthropic Claude)
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AI_MODEL_CHEAP=claude-3-5-haiku-20241022      # Classification, simple tasks
AI_MODEL_BALANCED=claude-3-5-sonnet-20241022  # Script generation, analysis
AI_MODEL_PREMIUM=claude-opus-4-20250514       # Critical decisions only

# AI Cost Management
AI_DAILY_SOFT_LIMIT_USD=5.00    # Warning threshold
AI_DAILY_HARD_LIMIT_USD=20.00   # Stop execution
AI_MONTHLY_SOFT_LIMIT_USD=100.00
AI_MONTHLY_HARD_LIMIT_USD=500.00

# Transcription (Whisper)
WHISPER_MODEL=base               # tiny/base/small/medium/large
WHISPER_DEVICE=cuda              # cuda/cpu
WHISPER_COMPUTE_TYPE=float16     # int8/float16/float32

# YouTube API (Optional - for video stats in WF4)
YOUTUBE_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  # Optional
```

### Notion Integration Setup
1. Go to [Notion Developers](https://www.notion.so/my-integrations)
2. Create a new integration
3. Copy the API key to `.env`
4. Share each database with your integration (click ••• → Add connections → Your Integration)
5. **CRITICAL**: Share Writing Style pages in Young Empire with the integration

### Install Dependencies

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Install Whisper dependencies
pip install faster-whisper

# Install OCR dependencies
sudo apt-get install tesseract-ocr  # Linux
brew install tesseract              # macOS
pip install pytesseract easyocr

# Install yt-dlp
pip install yt-dlp
```

---

## 🚀 Quick Start Commands

```bash
# 1. Activate virtual environment
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Check database schemas
./venv/bin/python3 src/inspect_db.py

# 3. Test API connection
./venv/bin/python3 src/check_connection.py

# 4. Run workflows (manual execution)
./venv/bin/python3 src/run.py --workflow WF1 --dry-run  # Test mode
./venv/bin/python3 src/run.py --workflow WF1             # Execute

# 5. Interactive CLI
./venv/bin/python3 src/run.py                            # Shows menu

# 6. Clear test data
./venv/bin/python3 src/clear_dbs.py
```

---

## 🔄 Complete Workflow Descriptions

### WF1: Viral DNA Encoding
**Trigger**: Manual execution on new/unprocessed Viral DNA entries
**Purpose**: Extract insights from viral content

**Steps**:
1. **S17**: Fetch unprocessed DNA entries (Extracted Perspective = empty)
2. **S08**: Classify Info Type (if empty) based on URL
3. **S18**: Scrape URL content:
   - **YouTube/IG Reel (Audio)**: Download via yt-dlp + extract IG description
   - **YouTube/IG Reel (Visual Only)**: Download via yt-dlp + extract IG description
   - **IG Carousel**: Download images via yt-dlp + extract IG description
   - **IG Static Post**: Download image via yt-dlp + extract IG description
   - **Web Article**: Scrape text via BeautifulSoup
4. **S04**: Transcribe content:
   - **Audio/Video**: Whisper transcription
   - **Visual Only**: Video OCR (extract on-screen text)
   - **Images**: Image OCR (pytesseract/easyocr)
5. **S05**: Extract Perspective (AI: Sonnet) - "What makes this viral? What's the merit?"
6. **S06**: Generate Hook Potential (AI: Haiku) - Extract opening hooks
7. **S07**: Generate Open Loop Seed (AI: Haiku) - Identify curiosity gaps
8. **S03**: Update DNA entry with all extracted data

**Cost Optimization**: OCR before AI, use Haiku for simple extractions, Sonnet only for deep analysis.

---

### WF2: Production-DNA Linking (Hybrid)
**Trigger**: Manual execution when Production status = "Idea"
**Purpose**: Suggest relevant Viral DNA sources for script generation

**Steps**:
1. **S01**: Fetch Production entries with status = "Idea"
2. **S01**: Query Viral DNA by matching Tags (niche)
3. **S16**: Generate DNA link suggestions (AI: Haiku ranks by relevance)
4. **User Review**: System presents suggestions, user approves/modifies
5. **S03**: Update Production with approved DNA links
6. **S03**: Update status → "Researching"

**Manual Approval**: User reviews AI suggestions before linking.

---

### WF3: Script Generation
**Trigger**: Manual execution when Production status = "Researching" + has DNA sources
**Purpose**: Generate video script using viral patterns

**Steps**:
1. **S01**: Fetch Production entry (Title, Channel, Format, DNA sources)
2. **S14**: Read Writing Style from Young Empire page body (per-channel)
3. **S01**: Fetch linked Viral DNA entries (Hook Potential, Open Loop Seed, Extracted Perspective)
4. **S15**: Generate script (AI: Sonnet):
   - Input: Writing Style + DNA patterns + video Title + Format
   - Output: Full script with hooks + open loops integrated
5. **Write to Page Body**: Append script to Production page (heading_2 + paragraphs)
6. **S03**: Update status → "DNA matching" (user reviews script)

**Manual Review**: User checks script quality before proceeding.

---

### WF3.1: Scene Breakdown (After WF3)
**Trigger**: Manual execution after user approves script
**Purpose**: Parse script into scene-by-scene breakdown

**Steps**:
1. **S01**: Fetch Production entry (read script from page body)
2. **S19**: Generate scene breakdown (AI: Sonnet):
   - Input: Full script
   - Output: List of scenes with Visual Prompt + Script per scene
3. **Write to Page Body**: Append scene table to Production page (table block)
4. **S20**: Create Scene List entries in Global Scene List DB:
   - One entry per scene with Production relation
5. **S03**: Update status → "Ready to Render"

**Alternative**: Scene table can stay in Production page body only (no separate Scene List DB entries) - this is flexible.

---

### WF4: Empire Week Review
**Trigger**: Manual execution on Young Empire entry with status = "Not started"
**Purpose**: Analyze weekly video performance

**Steps**:
1. **S01**: Fetch Young Empire entry (Channel, Year, Month, Week)
2. **S01**: Query Productions for matching Channel + Published Date in date range
3. **S10**: Fetch video performance for each published video:
   - If `production URL` exists: Use YouTube API (or yt-dlp metadata)
   - Extract: Views, Likes, Comments, Watch Time %
4. **S13**: Generate Reviewing section (AI: Sonnet):
   - Input: Performance data + video titles
   - Output: Markdown report analyzing trends, top performers, insights
5. **Write to Page Body**: Append Reviewing section to Empire page
6. **S03**: Update status → "Drafting"

**Manual Review**: User edits report before publishing.

---

### WF5: Empire Prospecting
**Trigger**: Manual execution after WF4 or standalone
**Purpose**: Generate new video ideas from Viral DNA

**Steps**:
1. **S01**: Fetch Young Empire entry (Channel)
2. **S01**: Query Viral DNA: Tags match Channel niche + has Extracted Perspective
3. **S13**: Generate Prospecting section (AI: Sonnet):
   - Input: DNA perspectives + current channel strategy
   - Output: List of video ideas with rationale
4. **Optional - S02**: Auto-create Production entries for each idea (status: "pending")
5. **Write to Page Body**: Append Prospecting section to Empire page
6. **S03**: Update status → "Published"

---

## 📊 Current Progress

### ✅ Completed
- [x] Project structure setup
- [x] Notion API integration (properties + page body)
- [x] Database schema inspector
- [x] Connection testing utilities
- [x] Basic CRUD operations for Notion pages
- [x] Multi-database support (4 databases)
- [x] Page content read/write (blocks API)
- [x] **Phase 1 Complete (2025-12-26)**:
  - [x] Directory structure created (`core/`, `skills/`, `workflows/`, `utils/`, `cli/`)
  - [x] Configuration files (databases.yaml, ai_config.yaml)
  - [x] Core modules: ConfigLoader, NotionClient, AIClient
  - [x] Utilities: CostTracker, StateManager
  - [x] Exception handling framework
  - [x] Demo script with all tests passing

### 🔄 Next Steps (Phase 2: Skills Implementation)
- [ ] CRUD Skills (S01-S03)
- [ ] Content Processing (S04, S08, S18)
- [ ] AI Analysis (S05-S07)
- [ ] Production Skills (S14-S16, S19-S21)
- [ ] Analytics (S10, S13)
- [ ] Workflow orchestration (WF1-WF5)
- [ ] CLI interface
- [ ] Testing framework

---

## 🐛 Common Issues & Solutions

### "Property X not found" errors
→ Run `./venv/bin/python3 src/inspect_db.py` to check current schema
→ Property names are case-sensitive

### "Validation error" on Status property
→ Check if Status is `status` type vs `select` type
→ Use the correct API format:
  - For status type: `{"status": {"name": "Value"}}`
  - For select type: `{"select": {"name": "Value"}}`

### Connection refused
→ Check NOTION_API_KEY is correct
→ Ensure database is shared with your integration
→ Ensure Writing Style pages in Young Empire are shared with integration

### Whisper transcription slow
→ Use GPU: Set `WHISPER_DEVICE=cuda` in `.env`
→ Use smaller model: Set `WHISPER_MODEL=base` (faster, less accurate)
→ Use Faster-Whisper: Already recommended in dependencies

### AI costs too high
→ Check `state/ai_costs.json` for usage breakdown
→ Adjust limits in `.env`
→ Use Haiku instead of Sonnet for simple tasks

---

## 📝 Critical Notes for AI Assistants

When continuing work on this project:

1. **Always run `inspect_db.py` first** to get current schema
2. **Check property types** before making API calls (status vs select!)
3. **The project uses direct HTTP requests** alongside notion-client for page body manipulation
4. **UTF-8 encoding is forced** for Windows compatibility
5. **Database IDs come from Notion URLs** after the workspace name
6. **Sequential execution only** - no concurrent workflows
7. **Manual execution required** - no automatic cron jobs
8. **Test entries have "Test Entry" checkbox** in Production Tracker only
9. **Scene List approach is flexible** - can be table in Production page body OR separate DB entries
10. **Cost optimization is critical** - use OCR/local tools before AI, tier AI models by task complexity
11. **Dry-run mode is required** for all workflows during development
12. **State is stored in JSON files** under `state/` directory
13. **Writing Style is stored in Young Empire page body** - access via blocks API
14. **IG content requires manual sharing to Notion** - system processes from there

---

## 📞 Quick Reference

| Action | Command |
|--------|---------|
| Check DB schema | `./venv/bin/python3 src/inspect_db.py` |
| Test connection | `./venv/bin/python3 src/check_connection.py` |
| Create test entries | `./venv/bin/python3 src/manual_check.py` |
| Clear test data | `./venv/bin/python3 src/clear_dbs.py` |
| Run workflow (dry-run) | `./venv/bin/python3 src/run.py --workflow WF1 --dry-run` |
| Run workflow (execute) | `./venv/bin/python3 src/run.py --workflow WF1` |
| Interactive menu | `./venv/bin/python3 src/run.py` |
| Check AI costs | `cat state/ai_costs.json` |

---

*This context document is the source of truth for the project. Update it whenever architectural decisions change.*

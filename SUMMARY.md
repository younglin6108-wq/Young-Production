# 📋 Young Production - Documentation Summary

> **Quick Reference**: Links to all specification documents
>
> **Last Updated**: 2025-12-26

---

## 📚 Documentation Index

### 1. [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) - **START HERE**
**What**: Complete project overview for AI assistants and developers
**Contains**:
- Project goals and architecture
- Detailed Notion database schemas with property importance scores (0-100)
- Complete workflow descriptions (WF1-WF5)
- Writing Style format specification
- Tech stack and environment setup
- Quick start commands
- Critical notes for AI assistants

**When to Read**: Before starting any work, when onboarding new team members, when context is lost

---

### 2. [TECHNICAL_SPEC.md](TECHNICAL_SPEC.md) - **IMPLEMENTATION BLUEPRINT**
**What**: Exact function signatures and technical requirements
**Contains**:
- All 21+ skills with Python function signatures (S01-S21)
- Input/output types with type hints
- AI model selection per skill (Haiku/Sonnet/Opus)
- Workflow state machines with error handling
- API integration contracts (Notion, Claude, yt-dlp, Whisper, OCR)
- Configuration schema (YAML files)
- Error handling matrix
- Cost tracking requirements

**When to Read**: During implementation, when writing code, when debugging API issues

---

### 3. [ARCHITECTURE.md](ARCHITECTURE.md) - **SYSTEM DESIGN**
**What**: Module structure and data flow patterns
**Contains**:
- Directory structure (`core/`, `skills/`, `workflows/`, `utils/`, `cli/`)
- Module dependency graph
- Data flow diagrams for WF1 and WF3
- Core module designs (NotionClient, AIClient, ConfigLoader)
- Workflow base class pattern
- CLI design and interactive prompts
- State management structure
- Testing architecture

**When to Read**: When planning architecture, before writing new modules, when refactoring

---

### 4. [IMPLEMENTATION_CHECKLIST.md](IMPLEMENTATION_CHECKLIST.md) - **BUILD GUIDE**
**What**: Phased implementation plan with testing requirements
**Contains**:
- 7-week implementation timeline
- Phase 1: Foundation (core modules, config)
- Phase 2: Skills (S01-S21)
- Phase 3: Advanced skills
- Phase 4: Workflows (WF1-WF5)
- Phase 5: CLI interface
- Phase 6: Polish and documentation
- Phase 7: Production deployment
- Success metrics and testing checklist

**When to Read**: When starting implementation, tracking progress, planning sprints

---

## 🎯 Quick Navigation by Task

### "I need to understand the project"
→ Read [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) sections:
- Project Overview
- Notion Database Schema
- Complete Workflow Descriptions

### "I need to implement skill X"
→ Read [TECHNICAL_SPEC.md](TECHNICAL_SPEC.md) → Skills Catalog → Find your skill (S01-S21)
→ Copy function signature, implement according to spec

### "I need to add a new module"
→ Read [ARCHITECTURE.md](ARCHITECTURE.md) → Module Structure
→ Check dependency graph to understand where it fits

### "I need to build a workflow"
→ Read [TECHNICAL_SPEC.md](TECHNICAL_SPEC.md) → Workflow State Machines
→ Read [ARCHITECTURE.md](ARCHITECTURE.md) → Workflow Base Class

### "I don't know where to start"
→ Read [IMPLEMENTATION_CHECKLIST.md](IMPLEMENTATION_CHECKLIST.md) → Phase 1
→ Follow checklist step-by-step

### "I'm getting Notion API errors"
→ Read [TECHNICAL_SPEC.md](TECHNICAL_SPEC.md) → API Integration Contracts → Notion API
→ Read [TECHNICAL_SPEC.md](TECHNICAL_SPEC.md) → Error Handling Matrix

### "I need to track AI costs"
→ Read [ARCHITECTURE.md](ARCHITECTURE.md) → Core Module Designs → AIClient
→ Read [TECHNICAL_SPEC.md](TECHNICAL_SPEC.md) → Cost Tracking Requirements

### "I need to understand a specific database"
→ Read [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) → Notion Database Schema (Detailed)
→ Find your database (Production Tracker, Viral DNA, Young Empire, Scene List)

### "I need to write an AI prompt"
→ Read [TECHNICAL_SPEC.md](TECHNICAL_SPEC.md) → Skills Catalog → Find AI skill (S05-S07, S13, S15, S16, S19)
→ See prompt template examples in spec

---

## 🔑 Key Decisions Summary

### Database Architecture
- **4 Databases**: Production Tracker, Viral DNA, Young Empire, Scene List
- **Removed Properties**: Virality (Tracker), Quarter (Empire), Channel (Scene List)
- **Importance Scores**: All properties rated 0-100 based on workflow usage
- **Writing Style Storage**: In Young Empire page body (per-channel)
- **Script Storage**: In Production Tracker page body (with scene table)

### AI Strategy
- **Provider**: Anthropic Claude only
- **Model Tiering**:
  - Haiku (cheap): Classification, simple extraction
  - Sonnet (balanced): Perspective, script generation, reports
  - Opus (premium): Not used currently
- **Cost Management**:
  - Daily soft: $5, hard: $20
  - Monthly soft: $100, hard: $500
  - Tracked per-skill, per-workflow, daily, monthly

### Transcription Strategy
- **Audio/Video**: yt-dlp + faster-whisper (local GPU)
- **Visual-Only Video**: Video OCR (opencv + pytesseract/easyocr)
- **Images**: Image OCR (pytesseract + easyocr)
- **IG Content**: Manual share to Notion, system processes description + content

### Execution Model
- **Triggers**: Manual CLI only (no cron)
- **State**: JSON files in `state/` directory
- **Concurrency**: Sequential only (no parallel workflows)
- **Error Handling**: Fail gracefully, continue to next entry, log errors
- **Idempotency**: Skip already processed entries

### Workflow Flow
1. **WF1**: Viral DNA Encoding (URL → Transcription → AI Analysis)
2. **WF2**: DNA Linking (Hybrid with user approval)
3. **WF3**: Script Generation (DNA patterns → Claude → Production page)
4. **WF3.1**: Scene Breakdown (Script → Scenes → Table in page)
5. **WF4**: Empire Week Review (Performance analysis)
6. **WF5**: Empire Prospecting (New video ideas from DNA)

---

## 📊 Skills Overview

### CRUD (3 skills)
- S01: fetch_db_entries - Query with filters
- S02: create_db_entry - Create new page
- S03: update_db_entry - Update properties/body

### Content Processing (3 skills)
- S04: transcribe_content - Whisper + OCR
- S08: classify_info_type - Detect content type
- S18: scrape_url_content - yt-dlp + web scraping

### AI Analysis (4 skills)
- S05: extract_perspective - What makes it viral? (Sonnet)
- S06: generate_hook - Extract opening hooks (Haiku)
- S07: generate_open_loop - Identify curiosity gaps (Haiku)
- S09: REMOVED (classify_urgency was removed)

### Production (7 skills)
- S14: read_writing_style - Parse Empire page body
- S15: generate_script - AI script generation (Sonnet)
- S16: link_dna_to_production - AI-ranked suggestions (Haiku)
- S17: fetch_unprocessed_dna - Query helper
- S19: generate_scene_breakdown - Script → Scenes (Sonnet)
- S20: fetch_scenes_for_video - Query helper
- S21: validate_scene_continuity - Rule-based validation

### Analytics (2 skills)
- S10: fetch_video_performance - YouTube stats
- S13: generate_report - Empire reports (Sonnet)

**Total: 21 skills**

---

## 🚀 Getting Started (Quick Guide)

### 1. First Time Setup
```bash
# Clone/navigate to project
cd Young-Production/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install system dependencies (OCR)
# Linux:
sudo apt-get install tesseract-ocr
# macOS:
brew install tesseract

# Copy .env.example to .env and fill in API keys
cp .env.example .env
nano .env  # Add your API keys

# Verify Notion connection
./venv/bin/python3 src/inspect_db.py
./venv/bin/python3 src/check_connection.py
```

### 2. Start Implementation
Follow [IMPLEMENTATION_CHECKLIST.md](IMPLEMENTATION_CHECKLIST.md) Phase 1:
1. Create directory structure
2. Implement core modules (config_loader, notion_client, ai_client)
3. Write unit tests
4. Move to Phase 2 (skills)

### 3. Daily Development Workflow
```bash
# Activate environment
cd backend
source venv/bin/activate

# Before coding: Check current DB schemas
./venv/bin/python3 src/inspect_db.py

# Write code following TECHNICAL_SPEC.md

# Run tests
pytest tests/test_your_module.py -v

# Commit often (specs are reference, don't commit to repo)
```

### 4. Testing Workflows
```bash
# Test with dry-run first
./venv/bin/python3 src/run.py --workflow WF1 --dry-run

# Execute for real
./venv/bin/python3 src/run.py --workflow WF1

# Check costs
cat state/ai_costs.json

# Check workflow state
cat state/wf1_last_run.json
```

---

## ⚠️ Critical Reminders

### For AI Assistants
1. **Always read PROJECT_CONTEXT.md first** - it's the source of truth
2. **Match function signatures exactly** from TECHNICAL_SPEC.md
3. **No cron jobs** - manual execution only
4. **Sequential workflows only** - no concurrency
5. **State in JSON files** - not in database
6. **Cost optimization is critical** - use OCR before AI, tier models correctly
7. **Writing Style is in Empire page body** - access via blocks API
8. **Scene table can live in Production page** - Scene List DB is optional

### For Developers
1. **Validate schema before API calls** - use databases.yaml
2. **Always use dry-run first** - test before executing
3. **Track costs carefully** - check state/ai_costs.json regularly
4. **Don't commit .env or state/** - in .gitignore
5. **Test with "Test Entry" flag** - in Production Tracker only
6. **Handle errors gracefully** - skip entry, log, continue
7. **Idempotent workflows** - safe to rerun

---

## 🔄 When Documents Conflict

**Priority Order** (highest to lowest):
1. **PROJECT_CONTEXT.md** - Source of truth for decisions and schemas
2. **TECHNICAL_SPEC.md** - Implementation details and function signatures
3. **ARCHITECTURE.md** - System design patterns
4. **IMPLEMENTATION_CHECKLIST.md** - Suggested build order (flexible)

If conflict exists:
- PROJECT_CONTEXT.md wins for business logic and requirements
- TECHNICAL_SPEC.md wins for implementation details
- Update other docs to match

---

## 📝 Document Update Protocol

When making architectural decisions:
1. Update [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) first (source of truth)
2. Update [TECHNICAL_SPEC.md](TECHNICAL_SPEC.md) if function signatures change
3. Update [ARCHITECTURE.md](ARCHITECTURE.md) if module structure changes
4. Update [IMPLEMENTATION_CHECKLIST.md](IMPLEMENTATION_CHECKLIST.md) if build order changes
5. Update this SUMMARY.md last

---

## 🎯 Success Criteria

### Phase 1 Complete
- [ ] Core modules pass unit tests
- [ ] Config files load correctly
- [ ] Notion API connection works with rate limiting
- [ ] AI client tracks costs accurately

### Phase 2 Complete
- [ ] All 21 skills implemented
- [ ] All skills have unit tests
- [ ] Integration test: Download video → Transcribe → Extract perspective
- [ ] Costs tracked in state/ai_costs.json

### Phase 3-4 Complete
- [ ] All 5 workflows (WF1-WF5) working
- [ ] End-to-end test: DNA → Script → Scenes → Report
- [ ] Dry-run mode works for all workflows
- [ ] State persisted correctly

### Phase 5-6 Complete
- [ ] CLI interface intuitive
- [ ] Interactive menu works
- [ ] Cost reporting clear
- [ ] Documentation complete

### Production Ready
- [ ] 90%+ test coverage
- [ ] All workflows tested with real data
- [ ] Error handling robust
- [ ] Cost optimization verified
- [ ] User feedback incorporated

---

**Questions? Start with [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) → Find your specific topic → Dive into detailed specs as needed.**

*This summary is your navigation hub. Bookmark it.*

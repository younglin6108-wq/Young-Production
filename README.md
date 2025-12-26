# 🎬 Young Production

**Automated YouTube video production pipeline powered by AI and Notion**

Transform viral content research into production-ready video scripts using pattern analysis, AI generation, and strategic workflow automation.

---

## 🚀 Quick Start

```bash
# 1. Clone and setup
cd Young-Production/backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install OCR dependencies
sudo apt-get install tesseract-ocr  # Linux
brew install tesseract              # macOS

# 4. Configure environment
cp .env.example .env
# Edit .env with your API keys (Notion, Anthropic)

# 5. Verify setup
./venv/bin/python3 src/inspect_db.py
./venv/bin/python3 src/check_connection.py

# 6. Run your first workflow
./venv/bin/python3 src/run.py
```

---

## 📋 What This Does

Young Production automates your YouTube content creation workflow:

1. **Research**: Add viral content URLs to Notion → AI extracts hooks, perspectives, and patterns
2. **Ideate**: Create video ideas → AI suggests relevant viral DNA sources
3. **Script**: Generate scripts using proven viral patterns + your channel's writing style
4. **Produce**: Break scripts into scenes with visual prompts
5. **Analyze**: Track performance and generate strategic reports

**Cost-Optimized**: Uses local transcription (Whisper), OCR, and tiered AI models (Haiku → Sonnet → Opus) to minimize API costs while maximizing quality.

---

## 📚 Documentation

| Document | Purpose | When to Read |
|----------|---------|--------------|
| [SUMMARY.md](SUMMARY.md) | Navigation hub | **Start here** - links to all docs |
| [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) | Complete project overview | Before any work, for context |
| [TECHNICAL_SPEC.md](TECHNICAL_SPEC.md) | Function signatures & APIs | During implementation |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design & patterns | Before writing new modules |
| [IMPLEMENTATION_CHECKLIST.md](IMPLEMENTATION_CHECKLIST.md) | 7-week build guide | Planning & tracking progress |

**First time here?** Read [SUMMARY.md](SUMMARY.md) → [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md)

---

## 🗄️ Notion Databases

### Required Setup
Create 4 Notion databases and share them with your integration:

1. **Young Production Tracker** - Video execution hub (Idea → Done)
2. **Viral DNA** - Content research repository
3. **Young Empire** - Analytics & strategy (includes Writing Style guides)
4. **Scene List** - Per-video scene breakdowns

See [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) for detailed schemas.

---

## 🤖 AI Strategy

- **Provider**: Anthropic Claude
- **Models**:
  - Haiku (cheap): Classification, hooks, open loops
  - Sonnet (balanced): Perspectives, scripts, reports
  - Opus (premium): Not used (optional for critical tasks)
- **Cost Management**: Daily/monthly limits with soft warnings + hard stops

**Current Costs** (estimated):
- Viral DNA analysis: ~$0.02-0.05 per entry
- Script generation: ~$0.10-0.30 per video
- Weekly report: ~$0.05-0.20

---

## 🔄 Workflows

| Workflow | Purpose | Trigger |
|----------|---------|---------|
| **WF1** | Viral DNA Encoding | Manual (process new DNA entries) |
| **WF2** | DNA → Production Linking | Manual (hybrid with user approval) |
| **WF3** | Script Generation | Manual (after DNA linked) |
| **WF3.1** | Scene Breakdown | Manual (after script review) |
| **WF4** | Empire Week Review | Manual (performance analysis) |
| **WF5** | Empire Prospecting | Manual (generate new ideas) |

```bash
# Run workflows
./venv/bin/python3 src/run.py --workflow WF1
./venv/bin/python3 src/run.py --workflow WF1 --dry-run  # Test first

# Interactive menu
./venv/bin/python3 src/run.py

# Check costs
./venv/bin/python3 src/run.py --show-costs
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Database/UI | Notion API |
| AI | Anthropic Claude (Haiku/Sonnet/Opus) |
| Transcription | yt-dlp + faster-whisper (local GPU) |
| OCR | pytesseract + easyocr |
| Backend | Python 3.12+ |
| CLI | Click + Rich |
| State | JSON files |

---

## 📊 Project Status

### ✅ Completed
- [x] Project structure & documentation
- [x] Notion API integration (CRUD + page body)
- [x] Database schema design
- [x] Complete technical specifications
- [x] 7-week implementation plan

### 🔄 In Progress (Follow [IMPLEMENTATION_CHECKLIST.md](IMPLEMENTATION_CHECKLIST.md))
- [ ] Phase 1: Core modules (config, Notion client, AI client)
- [ ] Phase 2: Skills (S01-S21)
- [ ] Phase 3: Workflows (WF1-WF5)
- [ ] Phase 4: CLI interface

---

## 🧪 Testing

```bash
# Run all tests
pytest backend/tests/ -v

# Run specific test file
pytest backend/tests/test_skills/test_crud.py -v

# Coverage report
pytest --cov=src backend/tests/
```

---

## 💰 Cost Tracking

AI costs are tracked in `state/ai_costs.json`:
- Daily/monthly totals
- Per-skill breakdown
- Per-workflow breakdown
- Automatic limit checking

Limits configured in `.env`:
```env
AI_DAILY_SOFT_LIMIT_USD=5.00    # Warning
AI_DAILY_HARD_LIMIT_USD=20.00   # Stop execution
AI_MONTHLY_SOFT_LIMIT_USD=100.00
AI_MONTHLY_HARD_LIMIT_USD=500.00
```

---

## 📁 Project Structure

```
Young-Production/
├── README.md                    # This file
├── SUMMARY.md                   # Documentation hub
├── PROJECT_CONTEXT.md           # Complete project context
├── TECHNICAL_SPEC.md            # Implementation blueprint
├── ARCHITECTURE.md              # System design
├── IMPLEMENTATION_CHECKLIST.md  # Build guide
├── .gitignore
└── backend/
    ├── requirements.txt
    ├── .env                     # API keys (DO NOT COMMIT)
    ├── venv/                    # Virtual environment
    ├── config/                  # YAML configs
    │   ├── databases.yaml
    │   ├── ai_config.yaml
    │   └── prompts/             # AI prompt templates
    ├── state/                   # Workflow state (DO NOT COMMIT)
    │   ├── ai_costs.json
    │   └── wf*_last_run.json
    └── src/
        ├── core/                # Core infrastructure
        ├── skills/              # Atomic functions (S01-S21)
        ├── workflows/           # Orchestrators (WF1-WF5)
        ├── utils/               # Utilities
        ├── cli/                 # CLI interface
        ├── tests/               # Unit & integration tests
        └── run.py               # Main entry point
```

---

## 🔧 Configuration

### Required `.env` Variables

```env
# Notion
NOTION_API_KEY=secret_...
PROD_TRACKER_DB_ID=...
VIRAL_DNA_DB_ID=...
YOUNG_EMPIRE_DB_ID=...
SCENE_LIST_DB_ID=...

# AI (Anthropic)
ANTHROPIC_API_KEY=sk-ant-...
AI_MODEL_CHEAP=claude-3-5-haiku-20241022
AI_MODEL_BALANCED=claude-3-5-sonnet-20241022
AI_MODEL_PREMIUM=claude-opus-4-20250514

# Cost Limits
AI_DAILY_SOFT_LIMIT_USD=5.00
AI_DAILY_HARD_LIMIT_USD=20.00
AI_MONTHLY_SOFT_LIMIT_USD=100.00
AI_MONTHLY_HARD_LIMIT_USD=500.00

# Transcription
WHISPER_MODEL=base
WHISPER_DEVICE=cuda
WHISPER_COMPUTE_TYPE=float16

# YouTube API (Optional)
YOUTUBE_API_KEY=...
```

---

## 🎯 Design Principles

1. **Atomic Skills** - Each function does ONE thing well
2. **Cost-First** - OCR before AI, rule-based before ML
3. **Fail-Safe** - Errors in one entry don't break workflow
4. **Idempotent** - Safe to rerun workflows
5. **Observable** - All costs, errors, progress logged
6. **Scalable** - Built to handle growth without code changes

---

## 🐛 Troubleshooting

### "Property X not found"
```bash
# Check current DB schema
./venv/bin/python3 src/inspect_db.py
```

### "Connection refused"
- Verify `NOTION_API_KEY` in `.env`
- Check databases are shared with your Notion integration
- Ensure Writing Style pages in Young Empire are shared

### "Whisper transcription slow"
- Use GPU: Set `WHISPER_DEVICE=cuda` in `.env`
- Use smaller model: Set `WHISPER_MODEL=base`

### "AI costs too high"
```bash
# Check cost breakdown
cat state/ai_costs.json
# Adjust limits in .env
```

---

## 🤝 Contributing

This is a personal project. Follow the implementation checklist for development:

1. Read all documentation (start with SUMMARY.md)
2. Follow IMPLEMENTATION_CHECKLIST.md phase-by-phase
3. Match function signatures from TECHNICAL_SPEC.md exactly
4. Write tests alongside code
5. Test with dry-run mode first
6. Update PROJECT_CONTEXT.md when making architectural decisions

---

## 📝 License

Private project - All rights reserved

---

## 🔗 Quick Links

- **Documentation Hub**: [SUMMARY.md](SUMMARY.md)
- **Implementation Guide**: [IMPLEMENTATION_CHECKLIST.md](IMPLEMENTATION_CHECKLIST.md)
- **API Specs**: [TECHNICAL_SPEC.md](TECHNICAL_SPEC.md)
- **Notion Setup**: [Notion Developers](https://www.notion.so/my-integrations)
- **Anthropic API**: [Anthropic Console](https://console.anthropic.com/)

---

**Ready to start?** → Open [SUMMARY.md](SUMMARY.md) and follow Phase 1 of the implementation checklist.


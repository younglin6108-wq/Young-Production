# ✅ Young Production - Implementation Checklist

> **Purpose**: Phased implementation guide with build order and testing requirements
>
> **Last Updated**: 2025-12-26

---

## 🎯 Implementation Strategy

### Build Principles
1. **Bottom-Up**: Build core modules → skills → workflows → CLI
2. **Test-Driven**: Write tests alongside implementation
3. **Incremental**: Test each phase before moving to next
4. **Dry-Run First**: All workflows support dry-run mode from day 1

---

## 📅 Phase 1: Foundation (Week 1)

### 1.1 Project Setup
- [ ] **Update requirements.txt** with all dependencies
  ```txt
  # Existing
  notion-client
  python-dotenv
  pandas
  fastapi
  uvicorn
  requests

  # Add these
  anthropic          # Claude AI SDK
  yt-dlp             # YouTube/IG downloader
  faster-whisper     # Local transcription
  pytesseract        # OCR
  easyocr            # Alternative OCR
  Pillow             # Image processing
  opencv-python      # Video frame extraction
  beautifulsoup4     # Web scraping
  lxml               # HTML parsing
  pyyaml             # Config files
  click              # CLI framework
  rich               # Pretty terminal output
  pytest             # Testing
  pytest-mock        # Mocking
  ```

- [ ] **Create directory structure** (as per ARCHITECTURE.md)
  ```bash
  mkdir -p backend/src/{core,skills,workflows,utils,cli,tests}
  mkdir -p backend/{config,state,logs}
  mkdir -p backend/config/prompts
  touch backend/src/{core,skills,workflows,utils,cli,tests}/__init__.py
  ```

- [ ] **Update .gitignore**
  ```
  # Add to existing
  venv/
  state/
  logs/
  *.pyc
  __pycache__/
  .pytest_cache/
  temp/
  downloads/
  ```

### 1.2 Configuration Files

- [ ] **Create config/databases.yaml** (copy from TECHNICAL_SPEC.md)
- [ ] **Create config/ai_config.yaml** (copy from TECHNICAL_SPEC.md)
- [ ] **Update .env with new variables**
  ```env
  # Add these to existing .env
  ANTHROPIC_API_KEY=sk-ant-...
  AI_MODEL_CHEAP=claude-3-5-haiku-20241022
  AI_MODEL_BALANCED=claude-3-5-sonnet-20241022
  AI_MODEL_PREMIUM=claude-opus-4-20250514
  AI_DAILY_SOFT_LIMIT_USD=5.00
  AI_DAILY_HARD_LIMIT_USD=20.00
  AI_MONTHLY_SOFT_LIMIT_USD=100.00
  AI_MONTHLY_HARD_LIMIT_USD=500.00
  WHISPER_MODEL=base
  WHISPER_DEVICE=cuda
  WHISPER_COMPUTE_TYPE=float16
  YOUTUBE_API_KEY=  # Optional
  ```

### 1.3 Core Modules

- [ ] **Implement core/exceptions.py**
  - [ ] Define all custom exceptions:
    - `NotionAPIError`
    - `NotionRateLimitError`
    - `PageNotFoundError`
    - `PropertyNotFoundError`
    - `AIError`
    - `CostLimitExceeded`
    - `DownloadError`
    - `TranscriptionError`
    - `ValidationError`
  - [ ] Write docstrings for each exception

- [ ] **Implement core/config_loader.py**
  - [ ] `ConfigLoader` class with YAML loading
  - [ ] Environment variable substitution
  - [ ] Test with databases.yaml and ai_config.yaml
  - [ ] Write unit tests (test_core/test_config_loader.py)

- [ ] **Implement utils/logger.py**
  - [ ] Setup structured logging (JSON format)
  - [ ] Log levels: DEBUG, INFO, WARNING, ERROR
  - [ ] Optional file logging (disabled by default per requirements)
  - [ ] Pretty console output using `rich`

- [ ] **Implement utils/state_manager.py**
  - [ ] `StateManager` class for JSON persistence
  - [ ] Load/save workflow states
  - [ ] Track processed entries (idempotency)
  - [ ] Write unit tests

- [ ] **Implement utils/cost_tracker.py**
  - [ ] `CostTracker` class (copy from TECHNICAL_SPEC.md)
  - [ ] Daily/monthly aggregation
  - [ ] Soft/hard limit checking
  - [ ] Per-skill and per-workflow tracking
  - [ ] Write unit tests

- [ ] **Implement core/notion_client.py**
  - [ ] `NotionClient` class (copy from ARCHITECTURE.md)
  - [ ] Rate limiting (2.5 req/sec)
  - [ ] Retry logic with exponential backoff
  - [ ] All CRUD methods
  - [ ] Write unit tests with mocked responses

- [ ] **Implement core/ai_client.py**
  - [ ] `AIClient` class (copy from ARCHITECTURE.md)
  - [ ] Claude API integration
  - [ ] Cost calculation
  - [ ] Cost tracker integration
  - [ ] Write unit tests with mocked API

### 1.4 Phase 1 Testing

- [ ] **Run all unit tests**: `pytest backend/tests/test_core/`
- [ ] **Verify config loading** from databases.yaml and ai_config.yaml
- [ ] **Test rate limiting** with multiple rapid Notion API calls
- [ ] **Test cost tracking** with mock AI calls
- [ ] **Verify state persistence** to JSON files

**Success Criteria**: All core modules pass unit tests, configurations load correctly

---

## 📅 Phase 2: Skills Implementation (Week 2-3)

### 2.1 CRUD Skills (S01-S03)

- [ ] **Implement skills/crud.py**
  - [ ] `S01: fetch_db_entries()` (copy signature from TECHNICAL_SPEC.md)
    - [ ] Support filters (NotionFilter dataclass)
    - [ ] Support pagination
    - [ ] Return QueryResult
    - [ ] Handle all error cases
  - [ ] `S02: create_db_entry()`
    - [ ] Validate properties against schema (use databases.yaml)
    - [ ] Support page body blocks
    - [ ] Dry-run mode
  - [ ] `S03: update_db_entry()`
    - [ ] Update properties (partial updates)
    - [ ] Append blocks to page body
    - [ ] Optional clear_body parameter
    - [ ] Dry-run mode
  - [ ] `S17: fetch_unprocessed_dna()` (wrapper around S01)

- [ ] **Write tests**: `test_skills/test_crud.py`
  - [ ] Test S01 with various filters
  - [ ] Test S02 with valid/invalid properties
  - [ ] Test S03 property updates and block appends
  - [ ] Test error handling

### 2.2 Content Scraping & Transcription (S04, S18)

- [ ] **Implement skills/scraping.py**
  - [ ] `S18: scrape_url_content()`
    - [ ] Detect platform from URL (YouTube, Instagram, Web)
    - [ ] Use yt-dlp for YouTube/IG:
      - [ ] Extract video/audio
      - [ ] Extract description/caption
      - [ ] Handle download errors
    - [ ] Use BeautifulSoup for web articles
    - [ ] Return ScrapedContent dataclass
  - [ ] Helper: `detect_platform(url)` → PlatformType

- [ ] **Implement skills/transcription.py**
  - [ ] `S04: transcribe_content()`
    - [ ] Whisper transcription for audio/video:
      - [ ] Use faster-whisper library
      - [ ] Support GPU/CPU (from .env)
      - [ ] Return text + language + confidence
    - [ ] Video OCR for visual-only content:
      - [ ] Extract frames with opencv
      - [ ] Run pytesseract + easyocr on frames
      - [ ] Concatenate text from all frames
    - [ ] Image OCR for static images:
      - [ ] Use pytesseract + easyocr
      - [ ] Combine results
    - [ ] Return TranscriptionResult dataclass
  - [ ] Helper: `extract_text_from_video_frames(video_path)`
  - [ ] Helper: `extract_text_from_image(image_path)`

- [ ] **Write tests**: `test_skills/test_scraping.py`, `test_skills/test_transcription.py`
  - [ ] Test URL detection for various platforms
  - [ ] Test yt-dlp integration with sample URLs
  - [ ] Test Whisper transcription with sample audio file
  - [ ] Test OCR with sample images

### 2.3 Classification Skills (S08)

- [ ] **Implement skills/classification.py**
  - [ ] `S08: classify_info_type()`
    - [ ] Rule-based classification from URL patterns:
      - [ ] YouTube shorts/videos
      - [ ] Instagram reels/posts
    - [ ] Use AI (Haiku) for ambiguous cases
    - [ ] Return List[InfoType]

- [ ] **Write tests**: `test_skills/test_classification.py`
  - [ ] Test rule-based classification for various URLs
  - [ ] Test AI classification (mocked)

### 2.4 AI Analysis Skills (S05-S07)

- [ ] **Create AI prompt templates**
  - [ ] `config/prompts/extract_perspective.txt`
    ```
    You are analyzing viral content to understand what makes it valuable.

    Content Title: {title}
    Description: {description}
    Transcript: {transcript}

    Analyze this content and provide:

    1. **Unique Perspective**: What unique angle or viewpoint does this content offer?
    2. **Viral Factors**: What specific techniques or patterns make this content viral?
    3. **Merit**: What value does this provide to viewers? Why would someone share this?

    Format your response as markdown with clear sections.
    ```

  - [ ] `config/prompts/generate_hook.txt`
    ```
    Extract opening hooks from this content.

    Transcript: {transcript}

    Identify:
    1. The exact opening line(s) (verbatim)
    2. Hook pattern type (question, contrarian claim, specific number, identity challenge, etc.)
    3. Why this hook works (psychological principle)

    Return as JSON:
    {
      "hooks": ["hook 1", "hook 2"],
      "patterns": ["pattern type 1", "pattern type 2"],
      "best_hook": "the most effective hook",
      "reasoning": "why it's the best"
    }
    ```

  - [ ] `config/prompts/generate_open_loop.txt`
    ```
    Identify open loops and curiosity gaps in this content.

    Transcript: {transcript}

    Find:
    1. Questions planted but not immediately answered
    2. "I'll tell you X later" patterns
    3. Contrast setups (wrong way → right way, old → new)
    4. Preview teases

    Return as JSON:
    {
      "seeds": ["open loop 1", "open loop 2"],
      "techniques": ["technique 1", "technique 2"],
      "resolution_timing": {"loop 1": "at 45% mark", "loop 2": "at end"}
    }
    ```

- [ ] **Implement skills/ai_analysis.py**
  - [ ] Load prompt templates from files
  - [ ] `S05: extract_perspective()` (use Sonnet)
  - [ ] `S06: generate_hook()` (use Haiku)
  - [ ] `S07: generate_open_loop()` (use Haiku)
  - [ ] Cost tracking for each call
  - [ ] Parse JSON responses from S06/S07

- [ ] **Write tests**: `test_skills/test_ai_analysis.py`
  - [ ] Test with mocked AI client
  - [ ] Verify cost tracking
  - [ ] Test JSON parsing

### 2.5 Phase 2 Testing

- [ ] **Integration test**: Download real YouTube video → Transcribe → Extract perspective
- [ ] **Integration test**: Download IG carousel → OCR → Extract hooks
- [ ] **Verify cost tracking** in state/ai_costs.json
- [ ] **Test dry-run mode** for all skills

**Success Criteria**: All skills work independently, costs tracked correctly

---

## 📅 Phase 3: Advanced Skills (Week 3-4)

### 3.1 Production Skills (S14-S16, S19-S21)

- [ ] **Create prompt templates**
  - [ ] `config/prompts/generate_script.txt`
  - [ ] `config/prompts/generate_scene_breakdown.txt`
  - [ ] `config/prompts/link_dna_suggestions.txt`

- [ ] **Implement skills/production.py**
  - [ ] `S14: read_writing_style()` (parse Empire page body)
  - [ ] `S15: generate_script()` (use Sonnet)
  - [ ] `S16: link_dna_to_production()` (use Haiku for ranking)
  - [ ] `S19: generate_scene_breakdown()` (use Sonnet)
  - [ ] `S20: fetch_scenes_for_video()` (wrapper around S01)
  - [ ] `S21: validate_scene_continuity()` (rule-based validation)

- [ ] **Write tests**: `test_skills/test_production.py`

### 3.2 Analytics & Reporting Skills (S10, S13)

- [ ] **Create prompt templates**
  - [ ] `config/prompts/generate_reviewing_report.txt`
  - [ ] `config/prompts/generate_prospecting_report.txt`

- [ ] **Implement skills/analytics.py**
  - [ ] `S10: fetch_video_performance()`
    - [ ] Option 1: Use YouTube Data API v3 (if API key available)
    - [ ] Option 2: Use yt-dlp --dump-json (fallback)
  - [ ] Return VideoPerformance dataclass

- [ ] **Implement skills/reporting.py**
  - [ ] `S13: generate_report()` for both REVIEWING and PROSPECTING

- [ ] **Write tests**: `test_skills/test_analytics.py`, `test_skills/test_reporting.py`

### 3.3 Phase 3 Testing

- [ ] **Test S14**: Read actual Writing Style from Empire page
- [ ] **Test S15**: Generate full script from DNA entries
- [ ] **Test S10**: Fetch real YouTube video stats
- [ ] **Test S13**: Generate Empire reports

**Success Criteria**: All 21 skills implemented and tested

---

## 📅 Phase 4: Workflows (Week 4-5)

### 4.1 Workflow Base Class

- [ ] **Implement workflows/base.py** (copy from ARCHITECTURE.md)
  - [ ] `BaseWorkflow` abstract class
  - [ ] State management methods
  - [ ] Dry-run support

### 4.2 WF1: Viral DNA Encoding

- [ ] **Implement workflows/wf1_viral_dna_encoding.py**
  - [ ] Inherit from BaseWorkflow
  - [ ] Implement state machine (from TECHNICAL_SPEC.md)
  - [ ] Error handling for each step
  - [ ] Skip already processed entries (idempotency)
  - [ ] Cost tracking
  - [ ] Dry-run mode

- [ ] **Write tests**: `test_workflows/test_wf1.py`
  - [ ] Test with mock skills
  - [ ] Test error recovery
  - [ ] Test cost limit handling

- [ ] **Manual test with real data**:
  ```bash
  # Create test Viral DNA entry in Notion
  # Run workflow
  ./venv/bin/python3 src/run.py --workflow WF1 --dry-run
  ./venv/bin/python3 src/run.py --workflow WF1
  # Verify DNA entry updated with Perspective/Hook/Loop
  ```

### 4.3 WF2: DNA Linking (Hybrid)

- [ ] **Implement cli/interactive.py** (copy from ARCHITECTURE.md)
  - [ ] `prompt_dna_link_approval()` function

- [ ] **Implement workflows/wf2_dna_linking.py**
  - [ ] Interactive user approval flow
  - [ ] Support approve/modify/skip actions

- [ ] **Write tests**: `test_workflows/test_wf2.py`
  - [ ] Test with mocked user input

- [ ] **Manual test**: Run with real Production entry

### 4.4 WF3: Script Generation

- [ ] **Implement workflows/wf3_script_generation.py**
  - [ ] Fetch Productions with status="Researching"
  - [ ] Read Writing Style
  - [ ] Generate script
  - [ ] Write to page body (blocks API)
  - [ ] Update status

- [ ] **Write tests**: `test_workflows/test_wf3.py`

- [ ] **Manual test**: Verify script appears in Production page

### 4.5 WF3.1: Scene Breakdown

- [ ] **Implement workflows/wf3_1_scene_breakdown.py**
  - [ ] Read script from page body
  - [ ] Generate scenes
  - [ ] Write scene table to page
  - [ ] Optional: Create Scene List DB entries

- [ ] **Manual test**: Verify scene table in Production page

### 4.6 WF4 & WF5: Empire Reports

- [ ] **Implement workflows/wf4_empire_review.py**
  - [ ] Fetch Empire entries with status="Not started"
  - [ ] Query Productions by time period
  - [ ] Fetch video performance
  - [ ] Generate Reviewing report
  - [ ] Write to page body

- [ ] **Implement workflows/wf5_empire_prospecting.py**
  - [ ] Query Viral DNA by channel tags
  - [ ] Generate Prospecting report
  - [ ] Optional: Create Production entries

- [ ] **Manual tests**: Run with real Empire entry

### 4.7 Phase 4 Testing

- [ ] **End-to-end test**: Complete production cycle
  1. Add Viral DNA URL → Run WF1
  2. Create Production "Idea" → Run WF2 (link DNA)
  3. Run WF3 (generate script)
  4. Review script → Run WF3.1 (scenes)
  5. Publish video → Run WF4 (review)
  6. Run WF5 (prospecting)

**Success Criteria**: All workflows execute successfully, state persisted

---

## 📅 Phase 5: CLI Interface (Week 5)

### 5.1 Command-Line Interface

- [ ] **Implement cli/commands.py**
  - [ ] Use `click` or `typer` framework
  - [ ] Commands:
    - [ ] `run.py --workflow WF1` (execute workflow)
    - [ ] `run.py --workflow WF1 --dry-run` (dry-run mode)
    - [ ] `run.py --show-costs` (display cost report)
    - [ ] `run.py --show-state` (display workflow states)
    - [ ] `run.py` (interactive menu)

- [ ] **Implement interactive menu** (using `rich` library)
  ```
  ╔═══════════════════════════════════════════╗
  ║   Young Production - Workflow Manager    ║
  ╚═══════════════════════════════════════════╝

  Select a workflow:
  [1] WF1: Viral DNA Encoding
  [2] WF2: Production-DNA Linking
  [3] WF3: Script Generation
  [4] WF3.1: Scene Breakdown
  [5] WF4: Empire Week Review
  [6] WF5: Empire Prospecting
  [7] Show AI Costs
  [8] Show Workflow States
  [0] Exit

  Choice:
  ```

### 5.2 Cost Reporting

- [ ] **Implement cost display**:
  ```
  ╔════════════════════════════════════════╗
  ║         AI Cost Report                 ║
  ╚════════════════════════════════════════╝

  Today (2025-12-26):        $3.45 / $5.00 (soft limit)
  This Month (2025-12):     $42.10 / $100.00

  By Skill:
    S05 (extract_perspective):  $15.20
    S15 (generate_script):      $18.50
    S06 (generate_hook):         $4.30
    ...

  By Workflow:
    WF1 (DNA Encoding):         $25.30
    WF3 (Script Generation):    $16.80
    ...

  Projected Monthly Cost: $82.40
  ```

### 5.3 Phase 5 Testing

- [ ] **Test all CLI commands**
- [ ] **Test interactive menu navigation**
- [ ] **Test dry-run mode from CLI**
- [ ] **Test cost reporting display**

**Success Criteria**: Full CLI interface working, user-friendly

---

## 📅 Phase 6: Polish & Documentation (Week 6)

### 6.1 Error Handling & Validation

- [ ] **Implement utils/validators.py**
  - [ ] Schema validation against databases.yaml
  - [ ] Property type checking
  - [ ] Required field validation

- [ ] **Add validation to all S02/S03 calls**

### 6.2 Documentation

- [ ] **Update requirements.txt** with final dependencies + versions
- [ ] **Create README.md** with:
  - [ ] Quick start guide
  - [ ] Installation instructions
  - [ ] Common commands
  - [ ] Troubleshooting

- [ ] **Add docstrings** to all functions (Google-style)

- [ ] **Create example .env.example** file

### 6.3 Final Testing

- [ ] **Run full test suite**: `pytest backend/tests/ -v`
- [ ] **Manual end-to-end test** with real data
- [ ] **Test cost limits** (trigger soft/hard limits)
- [ ] **Test error recovery** (network failures, rate limits)
- [ ] **Test idempotency** (rerun workflows on same data)

### 6.4 Performance Optimization

- [ ] **Profile slow operations** (Whisper transcription, AI calls)
- [ ] **Optimize Whisper model selection** (base vs small)
- [ ] **Batch AI calls where possible**

### 6.5 Phase 6 Checklist

- [ ] All tests passing
- [ ] Documentation complete
- [ ] Error handling robust
- [ ] Cost tracking accurate
- [ ] CLI user-friendly

**Success Criteria**: Production-ready system

---

## 📅 Phase 7: Production Deployment (Week 7)

### 7.1 Database Cleanup

- [ ] **Remove test properties** from Notion DBs (if you added "Test Entry" checkbox to other DBs)
- [ ] **Clean test data**: `./venv/bin/python3 src/clear_dbs.py`

### 7.2 Production Configuration

- [ ] **Review .env settings**:
  - [ ] Set production cost limits
  - [ ] Verify all API keys
  - [ ] Set Whisper model (base recommended for speed/cost)

- [ ] **Create Writing Style guides** in Young Empire pages for each channel

### 7.3 First Production Run

- [ ] **WF1**: Process existing Viral DNA entries
- [ ] **WF2**: Link DNA to existing Production ideas
- [ ] **WF3**: Generate first scripts
- [ ] **Monitor costs**: Check state/ai_costs.json after each workflow

### 7.4 Iteration

- [ ] **Refine AI prompts** based on output quality
- [ ] **Adjust cost limits** based on usage patterns
- [ ] **Update Writing Style guides** based on results

---

## 📊 Testing Checklist Summary

### Unit Tests
- [ ] Core modules (notion_client, ai_client, config_loader)
- [ ] Utilities (cost_tracker, state_manager)
- [ ] All 21 skills

### Integration Tests
- [ ] Notion API integration
- [ ] Claude AI integration
- [ ] yt-dlp integration
- [ ] Whisper integration
- [ ] OCR integration

### Workflow Tests
- [ ] WF1-WF5 with mocked skills
- [ ] WF1-WF5 end-to-end with test data

### Manual Tests
- [ ] Complete production cycle (DNA → Script → Scenes → Report)
- [ ] Cost limit triggers
- [ ] Error recovery
- [ ] Dry-run mode

---

## 🎯 Success Metrics

### Code Quality
- [ ] 90%+ test coverage
- [ ] All functions have docstrings
- [ ] Type hints on all function signatures
- [ ] No pylint/flake8 errors

### Functionality
- [ ] All 21 skills working
- [ ] All 5 workflows executing
- [ ] Cost tracking accurate within $0.01
- [ ] State persistence working
- [ ] Error recovery robust

### User Experience
- [ ] CLI commands intuitive
- [ ] Interactive menu clear
- [ ] Error messages helpful
- [ ] Cost reports readable

### Performance
- [ ] WF1 processes 10 DNA entries in < 5 minutes
- [ ] WF3 generates script in < 30 seconds
- [ ] No memory leaks over long runs

---

## 🚀 Post-Launch Tasks

### Month 1
- [ ] Monitor AI costs daily
- [ ] Refine prompts based on output quality
- [ ] Collect user feedback
- [ ] Fix bugs as discovered

### Month 2
- [ ] Optimize Whisper model selection
- [ ] Add workflow analytics (which workflows used most)
- [ ] Consider batch processing for WF1

### Future Enhancements
- [ ] Video asset downloading (implement Source/Asset Path in Scene List)
- [ ] Automated video rendering
- [ ] Webhook integration for real-time triggers
- [ ] Web dashboard (FastAPI + frontend)

---

*Follow this checklist sequentially. Each phase builds on the previous. Test thoroughly before moving forward.*

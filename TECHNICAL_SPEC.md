# 🔧 Young Production - Technical Specification

> **Purpose**: Detailed technical specifications for all skills, workflows, and integrations
>
> **Last Updated**: 2025-12-26
> **For Implementation**: This document provides exact function signatures and requirements

---

## 📑 Table of Contents

1. [Skills Catalog (S01-S21)](#skills-catalog)
2. [Workflow State Machines (WF1-WF5)](#workflow-state-machines)
3. [API Integration Contracts](#api-integration-contracts)
4. [Configuration Schema](#configuration-schema)
5. [Error Handling Matrix](#error-handling-matrix)
6. [Cost Tracking Requirements](#cost-tracking-requirements)

---

## 🎯 Skills Catalog

### Category 1: Core CRUD Operations

#### S01: fetch_db_entries
**Purpose**: Query any Notion database with filters

```python
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class NotionFilter:
    property: str
    condition: str  # "equals", "contains", "is_empty", etc.
    value: Any

@dataclass
class QueryResult:
    pages: List[Dict[str, Any]]
    has_more: bool
    next_cursor: Optional[str]

def fetch_db_entries(
    db_id: str,
    filters: Optional[List[NotionFilter]] = None,
    sorts: Optional[List[Dict[str, str]]] = None,
    page_size: int = 100,
    start_cursor: Optional[str] = None
) -> QueryResult:
    """
    Fetch entries from a Notion database with optional filtering and sorting.

    Args:
        db_id: Database ID (from .env)
        filters: List of filters to apply (AND logic)
        sorts: List of sort objects [{"property": "Title", "direction": "ascending"}]
        page_size: Number of results per page (max 100)
        start_cursor: Pagination cursor for next page

    Returns:
        QueryResult with pages, pagination info

    Raises:
        NotionAPIError: If API call fails
        RateLimitError: If rate limit exceeded (retry with backoff)

    Cost: Free (Notion API only)
    """
    pass
```

**Example Usage**:
```python
# Fetch unprocessed Viral DNA entries
filters = [
    NotionFilter(property="Extracted Perspective", condition="is_empty", value=True)
]
result = fetch_db_entries(
    db_id=VIRAL_DNA_DB_ID,
    filters=filters
)
```

---

#### S02: create_db_entry
**Purpose**: Create a new page in any Notion database

```python
def create_db_entry(
    db_id: str,
    properties: Dict[str, Any],
    page_body: Optional[List[Dict]] = None,
    dry_run: bool = False
) -> str:
    """
    Create a new page in a Notion database.

    Args:
        db_id: Database ID
        properties: Page properties dict (follows Notion API format)
        page_body: Optional list of block objects to append to page body
        dry_run: If True, validate only (no API call)

    Returns:
        str: Page ID of created page

    Raises:
        NotionAPIError: If creation fails
        ValidationError: If properties don't match schema

    Cost: Free

    Example properties format:
    {
        "Title": {"title": [{"text": {"content": "My Title"}}]},
        "Status": {"status": {"name": "Idea"}},
        "Tags (niche)": {"multi_select": [{"name": "AI"}, {"name": "Productivity"}]}
    }
    """
    pass
```

---

#### S03: update_db_entry
**Purpose**: Update properties or page body of existing page

```python
def update_db_entry(
    page_id: str,
    properties: Optional[Dict[str, Any]] = None,
    append_blocks: Optional[List[Dict]] = None,
    clear_body: bool = False,
    dry_run: bool = False
) -> bool:
    """
    Update an existing Notion page (properties and/or body).

    Args:
        page_id: Page ID to update
        properties: Properties to update (partial update supported)
        append_blocks: Blocks to append to page body
        clear_body: If True, clear all existing body content first
        dry_run: If True, validate only

    Returns:
        bool: Success status

    Raises:
        NotionAPIError: If update fails
        PageNotFoundError: If page doesn't exist

    Cost: Free
    """
    pass
```

---

### Category 2: Content Transcription

#### S04: transcribe_content
**Purpose**: Extract text from audio/video/images

```python
from enum import Enum
from pathlib import Path

class ContentType(Enum):
    AUDIO_VIDEO = "audio_video"  # Use Whisper
    VIDEO_VISUAL_ONLY = "video_visual"  # Use Video OCR
    IMAGE = "image"  # Use Image OCR

@dataclass
class TranscriptionResult:
    text: str
    language: str
    confidence: float
    method: str  # "whisper", "video_ocr", "image_ocr"
    duration_sec: Optional[float]  # For audio/video
    cost_usd: float

def transcribe_content(
    file_path: Path,
    content_type: ContentType,
    whisper_model: str = "base",
    device: str = "cuda"
) -> TranscriptionResult:
    """
    Transcribe audio/video or extract text from images.

    Args:
        file_path: Local path to downloaded file
        content_type: Type of content to transcribe
        whisper_model: Whisper model size (tiny/base/small/medium/large)
        device: Device for inference (cuda/cpu)

    Returns:
        TranscriptionResult with extracted text and metadata

    Raises:
        FileNotFoundError: If file doesn't exist
        TranscriptionError: If transcription fails

    Cost: Free (local processing)

    Process:
    - AUDIO_VIDEO: Use faster-whisper for transcription
    - VIDEO_VISUAL_ONLY: Extract frames, run OCR on each, concatenate
    - IMAGE: Run pytesseract + easyocr, combine results
    """
    pass
```

**Video OCR Helper**:
```python
def extract_text_from_video_frames(
    video_path: Path,
    sample_fps: float = 1.0  # Extract 1 frame per second
) -> List[str]:
    """
    Extract text from video frames using OCR.

    Args:
        video_path: Path to video file
        sample_fps: Frames per second to sample

    Returns:
        List of text strings (one per frame)

    Uses opencv to extract frames, pytesseract for OCR
    """
    pass
```

---

#### S18: scrape_url_content
**Purpose**: Download and extract content from URLs

```python
from enum import Enum

class PlatformType(Enum):
    YOUTUBE = "youtube"
    INSTAGRAM = "instagram"
    WEB_ARTICLE = "web"
    UNKNOWN = "unknown"

@dataclass
class ScrapedContent:
    platform: PlatformType
    title: str
    description: str  # IG caption, YouTube description, article meta
    file_paths: List[Path]  # Downloaded media files
    metadata: Dict[str, Any]  # Platform-specific metadata

def scrape_url_content(
    url: str,
    download_dir: Path
) -> ScrapedContent:
    """
    Download and extract content from URL based on platform.

    Args:
        url: Source URL
        download_dir: Directory to save downloaded files

    Returns:
        ScrapedContent with downloaded files and metadata

    Raises:
        UnsupportedPlatformError: If platform not supported
        DownloadError: If download fails

    Cost: Free

    Process:
    - Detect platform from URL
    - Use yt-dlp for YouTube/Instagram
    - Use BeautifulSoup + requests for web articles
    - Extract description/caption for all platforms
    """
    pass
```

---

### Category 3: AI Analysis

#### S05: extract_perspective
**Purpose**: AI-generated analysis of viral content merit

```python
@dataclass
class PerspectiveAnalysis:
    perspective: str  # Main analysis text (markdown)
    key_insights: List[str]  # Bullet points
    virality_factors: List[str]  # What made it viral
    confidence: float  # AI confidence score
    cost_usd: float

def extract_perspective(
    transcript: str,
    description: str,
    title: str,
    model: str = "claude-3-5-sonnet-20241022"
) -> PerspectiveAnalysis:
    """
    Analyze viral content to extract perspective and merit.

    Args:
        transcript: Full content transcript
        description: Platform description/caption
        title: Content title
        model: Claude model to use

    Returns:
        PerspectiveAnalysis with AI-generated insights

    Raises:
        AIError: If AI call fails
        CostLimitExceeded: If daily/monthly limit hit

    AI Prompt Template: prompts/extract_perspective.txt
    Model: Sonnet (balanced quality/cost)
    Expected Cost: ~$0.02-0.05 per analysis

    Prompt should ask:
    - What's the unique angle/perspective?
    - What makes this content viral?
    - What techniques/patterns are used?
    - What merit does this provide to viewers?
    """
    pass
```

---

#### S06: generate_hook
**Purpose**: Extract opening hooks from viral content

```python
@dataclass
class HookAnalysis:
    hooks: List[str]  # Extracted hooks
    patterns: List[str]  # Hook patterns identified
    best_hook: str  # Top recommended hook
    cost_usd: float

def generate_hook(
    transcript: str,
    first_30_seconds: Optional[str] = None,
    model: str = "claude-3-5-haiku-20241022"
) -> HookAnalysis:
    """
    Extract and analyze opening hooks from content.

    Args:
        transcript: Full transcript
        first_30_seconds: Optional isolated first 30s of transcript
        model: Claude model (Haiku for cost optimization)

    Returns:
        HookAnalysis with extracted hooks

    AI Prompt Template: prompts/generate_hook.txt
    Model: Haiku (cheap, simple extraction task)
    Expected Cost: ~$0.001-0.005 per analysis

    Prompt should extract:
    - Opening line verbatim
    - Hook pattern type (question, contrarian, specific number, etc.)
    - Why it works
    """
    pass
```

---

#### S07: generate_open_loop
**Purpose**: Identify curiosity-building patterns

```python
@dataclass
class OpenLoopAnalysis:
    seeds: List[str]  # Open loop phrases
    techniques: List[str]  # Techniques used
    resolution_timing: Dict[str, str]  # When each loop closes
    cost_usd: float

def generate_open_loop(
    transcript: str,
    model: str = "claude-3-5-haiku-20241022"
) -> OpenLoopAnalysis:
    """
    Identify open loops and curiosity gaps in content.

    Args:
        transcript: Full transcript
        model: Claude model (Haiku)

    Returns:
        OpenLoopAnalysis with identified patterns

    AI Prompt Template: prompts/generate_open_loop.txt
    Model: Haiku
    Expected Cost: ~$0.001-0.005 per analysis

    Prompt should identify:
    - Questions planted but not immediately answered
    - "I'll tell you X later" patterns
    - Contrast setups (wrong way → right way)
    - Preview teases
    """
    pass
```

---

#### S08: classify_info_type
**Purpose**: Detect content type from URL/metadata

```python
from typing import List

class InfoType(Enum):
    REEL_AUDIO = "Reel (Audio)"
    REEL_VISUAL_ONLY = "Reel (Visual Only)"
    CAROUSEL = "Carousel"
    STATIC_POST = "Static Post"
    YOUTUBE_SHORT = "Youtube Short"
    LONG_VIDEO = "Long Video"
    UNKNOWN = "Unknown"

def classify_info_type(
    url: str,
    metadata: Optional[Dict[str, Any]] = None,
    model: str = "claude-3-5-haiku-20241022"
) -> List[InfoType]:
    """
    Classify content type from URL and metadata.

    Args:
        url: Source URL
        metadata: Optional metadata from yt-dlp
        model: Claude model for ambiguous cases

    Returns:
        List[InfoType]: Detected types (can be multiple for Notion multi_select)

    Process:
    1. Rule-based detection from URL patterns:
       - youtube.com/shorts/ → Youtube Short
       - youtube.com/watch/ + duration < 60s → Youtube Short
       - youtube.com/watch/ + duration >= 60s → Long Video
       - instagram.com/reel/ → Reel (Audio or Visual Only - needs AI)
       - instagram.com/p/ → Carousel or Static Post (needs metadata)

    2. If ambiguous, use AI (Haiku) to classify from metadata

    Cost: Free (rule-based), ~$0.001 (AI for ambiguous)
    """
    pass
```

---

### Category 4: Production & Script Generation

#### S14: read_writing_style
**Purpose**: Fetch channel writing style from Young Empire page

```python
@dataclass
class WritingStyle:
    channel: str
    tone: str
    audience_avatar: str
    content_philosophy: str
    hook_library: List[Dict[str, str]]  # [{pattern, example, source_dna}]
    open_loop_techniques: List[str]
    anti_patterns: List[str]
    iteration_log: List[Dict[str, str]]
    last_updated: str

def read_writing_style(
    channel: str,
    empire_db_id: str
) -> WritingStyle:
    """
    Read writing style guide from Young Empire page body.

    Args:
        channel: Channel name (e.g., "next10yearz")
        empire_db_id: Young Empire database ID

    Returns:
        WritingStyle dataclass with parsed style guide

    Process:
    1. Query Young Empire DB for page with Channel = channel + has writing style content
    2. Read page blocks using blocks API
    3. Parse markdown structure to extract:
       - Core Identity section
       - Hook Library table
       - Open Loop Techniques
       - Anti-Patterns
       - Iteration Log

    Raises:
        StyleGuideNotFoundError: If no style guide exists for channel
        ParseError: If style guide format invalid

    Cost: Free
    """
    pass
```

---

#### S15: generate_script
**Purpose**: Generate video script using viral patterns

```python
@dataclass
class ScriptGeneration:
    script: str  # Full script (markdown with headings/paragraphs)
    estimated_duration_sec: int
    hook_used: str
    open_loops_count: int
    cost_usd: float

def generate_script(
    title: str,
    format_type: str,  # "shorts" or "Video"
    viral_dna: List[Dict[str, Any]],  # DNA entries with Hook/Perspective/OpenLoop
    writing_style: WritingStyle,
    model: str = "claude-3-5-sonnet-20241022"
) -> ScriptGeneration:
    """
    Generate video script using viral DNA patterns and channel writing style.

    Args:
        title: Video title/topic
        format_type: "shorts" (30-60s) or "Video" (5-15min)
        viral_dna: List of linked Viral DNA entries
        writing_style: Channel writing style guide
        model: Claude model (Sonnet for quality)

    Returns:
        ScriptGeneration with full script

    AI Prompt Template: prompts/generate_script.txt
    Model: Sonnet (critical task)
    Expected Cost: ~$0.10-0.30 per script

    Prompt should:
    - Use hooks from DNA/style guide
    - Integrate open loop techniques
    - Follow channel tone/philosophy
    - Avoid anti-patterns
    - Structure: Hook → Body → CTA
    - Target duration based on format

    Raises:
        AIError: If generation fails
        CostLimitExceeded: If budget exceeded
    """
    pass
```

---

#### S16: link_dna_to_production
**Purpose**: Suggest DNA links for Production entry (AI-ranked)

```python
@dataclass
class DNALinkSuggestion:
    dna_id: str
    dna_title: str
    relevance_score: float  # 0.0-1.0
    reasoning: str
    matching_tags: List[str]

def link_dna_to_production(
    production_title: str,
    production_channel: str,
    available_dna: List[Dict[str, Any]],  # DNA entries with same niche tags
    max_suggestions: int = 5,
    model: str = "claude-3-5-haiku-20241022"
) -> List[DNALinkSuggestion]:
    """
    Generate AI-ranked suggestions for DNA → Production linking.

    Args:
        production_title: Video title/topic
        production_channel: Channel name
        available_dna: DNA entries filtered by matching tags
        max_suggestions: Max number of suggestions to return
        model: Claude model (Haiku for ranking)

    Returns:
        List of DNALinkSuggestion sorted by relevance

    AI Prompt Template: prompts/link_dna_suggestions.txt
    Model: Haiku (simple ranking task)
    Expected Cost: ~$0.01-0.05 per ranking

    Process:
    1. Filter DNA by matching Tags (niche)
    2. Use AI to rank by relevance to production title
    3. Return top N suggestions with reasoning

    User Review: System presents suggestions, user approves/modifies
    """
    pass
```

---

#### S19: generate_scene_breakdown
**Purpose**: Parse script into scene-by-scene breakdown

```python
@dataclass
class Scene:
    scene_number: int
    visual_prompt: str
    script_text: str
    estimated_duration_sec: int

@dataclass
class SceneBreakdown:
    scenes: List[Scene]
    total_duration_sec: int
    cost_usd: float

def generate_scene_breakdown(
    script: str,
    format_type: str,
    model: str = "claude-3-5-sonnet-20241022"
) -> SceneBreakdown:
    """
    Parse script into individual scenes with visual prompts.

    Args:
        script: Full video script
        format_type: "shorts" or "Video"
        model: Claude model (Sonnet)

    Returns:
        SceneBreakdown with list of scenes

    AI Prompt Template: prompts/generate_scene_breakdown.txt
    Model: Sonnet
    Expected Cost: ~$0.05-0.15 per breakdown

    Prompt should:
    - Identify scene transitions in script
    - Generate visual description per scene
    - Estimate scene duration
    - Ensure visual/audio sync makes sense

    Output format:
    [
        {
            "scene_number": 1,
            "visual_prompt": "Wide shot of city skyline at sunset",
            "script_text": "Most people don't realize...",
            "estimated_duration_sec": 5
        },
        ...
    ]
    """
    pass
```

---

#### S20: fetch_scenes_for_video
**Purpose**: Query Scene List for a specific video

```python
def fetch_scenes_for_video(
    production_id: str,
    scene_list_db_id: str
) -> List[Dict[str, Any]]:
    """
    Fetch all scenes for a production entry.

    Args:
        production_id: Production page ID
        scene_list_db_id: Scene List database ID

    Returns:
        List of scene pages sorted by Name (Scene 1, Scene 2, etc.)

    Uses: S01 (fetch_db_entries) with relation filter

    Cost: Free
    """
    filters = [
        NotionFilter(property="Production", condition="contains", value=production_id)
    ]
    result = fetch_db_entries(db_id=scene_list_db_id, filters=filters)

    # Sort by scene number (extract from Name property)
    scenes = sorted(result.pages, key=lambda p: extract_scene_number(p))
    return scenes
```

---

### Category 5: Analytics & Reporting

#### S10: fetch_video_performance
**Purpose**: Get YouTube video statistics

```python
@dataclass
class VideoPerformance:
    video_id: str
    title: str
    views: int
    likes: int
    comments: int
    duration_sec: int
    published_date: str
    thumbnail_url: str

def fetch_video_performance(
    video_url: str,
    use_api: bool = True  # If True, use YouTube API; else yt-dlp
) -> VideoPerformance:
    """
    Fetch performance metrics for a YouTube video.

    Args:
        video_url: YouTube video URL
        use_api: Use YouTube Data API (requires API key) or yt-dlp metadata

    Returns:
        VideoPerformance with metrics

    Process:
    - If use_api=True: Use YouTube Data API v3
    - If use_api=False: Use yt-dlp --dump-json (no API key needed)

    Cost:
    - API: 1 quota unit per request (free tier: 10,000/day)
    - yt-dlp: Free but slower

    Raises:
        VideoNotFoundError: If video doesn't exist
        APIQuotaExceeded: If YouTube API quota exceeded
    """
    pass
```

---

#### S13: generate_report
**Purpose**: Generate Reviewing or Prospecting sections for Empire

```python
from enum import Enum

class ReportType(Enum):
    REVIEWING = "reviewing"  # Performance analysis
    PROSPECTING = "prospecting"  # New ideas from DNA

@dataclass
class ReportSection:
    report_type: ReportType
    content: str  # Markdown report
    cost_usd: float

def generate_report(
    report_type: ReportType,
    data: Dict[str, Any],
    channel: str,
    model: str = "claude-3-5-sonnet-20241022"
) -> ReportSection:
    """
    Generate Empire report section (Reviewing or Prospecting).

    Args:
        report_type: Type of report to generate
        data: Context data
            - For REVIEWING: {"videos": [VideoPerformance], "time_period": str}
            - For PROSPECTING: {"dna_entries": [Dict], "channel_strategy": str}
        channel: Channel name
        model: Claude model (Sonnet)

    Returns:
        ReportSection with markdown content

    AI Prompt Template:
    - prompts/generate_reviewing_report.txt
    - prompts/generate_prospecting_report.txt

    Model: Sonnet
    Expected Cost: ~$0.05-0.20 per report

    REVIEWING report should analyze:
    - Top performers (views, engagement)
    - Trends over time period
    - What worked / what didn't
    - Lessons learned

    PROSPECTING report should generate:
    - New video ideas from DNA perspectives
    - Rationale per idea
    - Suggested titles
    - Expected viral potential
    """
    pass
```

---

#### S17: fetch_unprocessed_dna
**Purpose**: Query Viral DNA entries needing processing

```python
def fetch_unprocessed_dna(
    viral_dna_db_id: str
) -> List[Dict[str, Any]]:
    """
    Fetch Viral DNA entries where Extracted Perspective is empty.

    Args:
        viral_dna_db_id: Viral DNA database ID

    Returns:
        List of unprocessed DNA pages

    Uses: S01 with filter on Extracted Perspective = empty

    Cost: Free
    """
    filters = [
        NotionFilter(property="Extracted Perspective", condition="is_empty", value=True)
    ]
    result = fetch_db_entries(db_id=viral_dna_db_id, filters=filters)
    return result.pages
```

---

### Category 6: Utility Skills

#### S21: validate_scene_continuity
**Purpose**: Check scene order and completeness

```python
@dataclass
class ContinuityIssue:
    issue_type: str  # "missing_scene", "duration_mismatch", "visual_gap"
    scene_number: int
    description: str
    severity: str  # "error", "warning", "info"

def validate_scene_continuity(
    scenes: List[Scene],
    expected_total_duration_sec: int
) -> List[ContinuityIssue]:
    """
    Validate scene breakdown for issues.

    Args:
        scenes: List of scenes
        expected_total_duration_sec: Expected video duration

    Returns:
        List of issues found (empty if valid)

    Checks:
    - Scene numbers sequential (1, 2, 3...)
    - No duplicate scene numbers
    - Total duration matches expected
    - Visual prompts not empty
    - Script text not empty

    Cost: Free (rule-based validation)
    """
    pass
```

---

## 🔄 Workflow State Machines

### WF1: Viral DNA Encoding

**State Machine**:
```
[START] → Fetch Unprocessed DNA (S17)
    ↓
    ├─→ [No entries] → EXIT (Success)
    └─→ [Has entries] → For each entry:
            ↓
        Classify Info Type (S08)
            ↓
        Scrape URL (S18)
            ↓
            ├─→ [Download failed] → Log error → Continue to next
            └─→ [Success] → Transcribe (S04)
                    ↓
                    ├─→ [Transcription failed] → Log error → Continue
                    └─→ [Success] → AI Analysis (S05, S06, S07)
                            ↓
                            ├─→ [AI failed / Cost limit] → Log error → Continue
                            └─→ [Success] → Update DNA (S03)
                                    ↓
                                [NEXT ENTRY]
    ↓
[END] → Return summary (processed, failed, skipped)
```

**Implementation**:
```python
from dataclasses import dataclass
from typing import List

@dataclass
class WF1Result:
    total_processed: int
    successful: int
    failed: int
    skipped: int
    errors: List[str]
    total_cost_usd: float

def wf1_viral_dna_encoding(
    viral_dna_db_id: str,
    dry_run: bool = False,
    max_entries: Optional[int] = None
) -> WF1Result:
    """
    Workflow 1: Process unprocessed Viral DNA entries.

    Args:
        viral_dna_db_id: Viral DNA database ID
        dry_run: If True, simulate without API calls
        max_entries: Max entries to process (None = all)

    Returns:
        WF1Result with processing summary

    Error Handling:
    - Download failures: Log, skip entry, continue
    - Transcription failures: Log, skip entry, continue
    - AI failures: Log, skip entry, continue
    - Cost limit exceeded: Stop workflow, return partial results

    State Persistence:
    - Save progress to state/wf1_last_run.json
    - Track processed entry IDs to avoid reprocessing

    Rollback: No rollback needed (idempotent - skip already processed)
    """
    result = WF1Result(total_processed=0, successful=0, failed=0, skipped=0, errors=[], total_cost_usd=0.0)

    # Step 1: Fetch unprocessed
    unprocessed = fetch_unprocessed_dna(viral_dna_db_id)

    if max_entries:
        unprocessed = unprocessed[:max_entries]

    result.total_processed = len(unprocessed)

    for entry in unprocessed:
        try:
            # Step 2: Classify
            info_types = classify_info_type(entry['properties']['URL']['url'])

            # Step 3: Scrape
            scraped = scrape_url_content(entry['properties']['URL']['url'], download_dir=Path("temp"))

            # Step 4: Transcribe
            transcript_result = transcribe_content(scraped.file_paths[0], determine_content_type(info_types[0]))

            # Step 5-7: AI Analysis
            perspective = extract_perspective(transcript_result.text, scraped.description, entry['properties']['Title']['title'][0]['text']['content'])
            hook = generate_hook(transcript_result.text)
            open_loop = generate_open_loop(transcript_result.text)

            # Step 8: Update
            if not dry_run:
                update_db_entry(
                    page_id=entry['id'],
                    properties={
                        "Extracted Perspective": {"rich_text": [{"text": {"content": perspective.perspective}}]},
                        "Hook Potential": {"rich_text": [{"text": {"content": hook.best_hook}}]},
                        "Open Loop Seed": {"rich_text": [{"text": {"content": "\n".join(open_loop.seeds)}}]},
                        "Info Type": {"multi_select": [{"name": it.value} for it in info_types]}
                    }
                )

            result.successful += 1
            result.total_cost_usd += perspective.cost_usd + hook.cost_usd + open_loop.cost_usd

        except CostLimitExceeded as e:
            result.errors.append(f"Cost limit exceeded: {str(e)}")
            break
        except Exception as e:
            result.failed += 1
            result.errors.append(f"Entry {entry['id']}: {str(e)}")
            continue

    # Save state
    save_workflow_state("WF1", result)

    return result
```

---

### WF2: Production-DNA Linking (Hybrid)

**State Machine**:
```
[START] → Fetch Productions with status="Idea" (S01)
    ↓
    ├─→ [No entries] → EXIT (Success)
    └─→ [Has entries] → For each production:
            ↓
        Query DNA by matching Tags (S01)
            ↓
        Generate Link Suggestions (S16)
            ↓
        **[USER REVIEW]** → Present suggestions
            ↓
            ├─→ [User approves] → Update Production (S03)
            ├─→ [User modifies] → Update with modified links (S03)
            └─→ [User skips] → Continue to next
                    ↓
                Update status → "Researching" (S03)
                    ↓
                [NEXT ENTRY]
    ↓
[END] → Return summary
```

**Implementation**:
```python
@dataclass
class WF2Result:
    total_processed: int
    linked: int
    skipped: int
    user_modified: int
    total_cost_usd: float

def wf2_dna_linking_interactive(
    tracker_db_id: str,
    viral_dna_db_id: str,
    dry_run: bool = False
) -> WF2Result:
    """
    Workflow 2: Suggest DNA links for Productions (Hybrid with user approval).

    Args:
        tracker_db_id: Production Tracker DB ID
        viral_dna_db_id: Viral DNA DB ID
        dry_run: If True, simulate only

    Returns:
        WF2Result with linking summary

    Process:
    1. Fetch Productions with status = "Idea"
    2. For each production:
       a. Query DNA by matching Tags (niche)
       b. Use AI to rank suggestions (S16)
       c. Present to user via CLI
       d. User approves/modifies/skips
       e. Update Production + status

    User Interface:
    - Display production title
    - Show top 5 DNA suggestions with reasoning
    - Options: [A]pprove all, [M]odify, [S]kip
    - If modify: Show checkboxes to select specific DNA entries
    """
    result = WF2Result(total_processed=0, linked=0, skipped=0, user_modified=0, total_cost_usd=0.0)

    # Fetch productions with status = "Idea"
    filters = [NotionFilter(property="Status", condition="equals", value="Idea")]
    productions = fetch_db_entries(db_id=tracker_db_id, filters=filters)

    result.total_processed = len(productions.pages)

    for prod in productions.pages:
        title = prod['properties']['Title']['title'][0]['text']['content']
        channel = prod['properties']['Channel']['select']['name']

        # Get production tags (if any)
        prod_tags = [tag['name'] for tag in prod['properties'].get('Tags', {}).get('multi_select', [])]

        # Query DNA by matching tags
        # (Implementation details...)

        # Generate suggestions
        suggestions = link_dna_to_production(title, channel, available_dna)
        result.total_cost_usd += suggestions_cost

        # Present to user
        print(f"\n📋 Production: {title}")
        print(f"🏷️  Tags: {', '.join(prod_tags)}")
        print(f"\n🧬 Suggested DNA Links ({len(suggestions)}):")
        for i, sug in enumerate(suggestions[:5]):
            print(f"  {i+1}. {sug.dna_title} (Score: {sug.relevance_score:.2f})")
            print(f"     → {sug.reasoning}")

        user_choice = input("\n[A]pprove all / [M]odify / [S]kip? ").strip().upper()

        if user_choice == 'A':
            # Approve all suggestions
            if not dry_run:
                update_db_entry(
                    page_id=prod['id'],
                    properties={
                        "Viral DNA sources": {"relation": [{"id": s.dna_id} for s in suggestions]},
                        "Status": {"status": {"name": "Researching"}}
                    }
                )
            result.linked += 1

        elif user_choice == 'M':
            # User selects specific entries
            selected = prompt_user_selection(suggestions)
            if not dry_run:
                update_db_entry(
                    page_id=prod['id'],
                    properties={
                        "Viral DNA sources": {"relation": [{"id": s.dna_id} for s in selected]},
                        "Status": {"status": {"name": "Researching"}}
                    }
                )
            result.user_modified += 1

        else:  # Skip
            result.skipped += 1

    save_workflow_state("WF2", result)
    return result
```

---

### WF3: Script Generation

**State Machine**:
```
[START] → Fetch Productions with status="Researching" + has DNA sources (S01)
    ↓
    ├─→ [No entries] → EXIT (Success)
    └─→ [Has entries] → For each production:
            ↓
        Read Writing Style (S14)
            ↓
        Fetch linked DNA (S01)
            ↓
        Generate Script (S15)
            ↓
        Write to Page Body (S03)
            ↓
        Update status → "DNA matching" (S03)
            ↓
        [NEXT ENTRY]
    ↓
[END] → Return summary
```

**Implementation**:
```python
@dataclass
class WF3Result:
    total_processed: int
    successful: int
    failed: int
    total_cost_usd: float
    errors: List[str]

def wf3_script_generation(
    tracker_db_id: str,
    empire_db_id: str,
    viral_dna_db_id: str,
    dry_run: bool = False
) -> WF3Result:
    """
    Workflow 3: Generate scripts for Productions.

    Args:
        tracker_db_id: Production Tracker DB ID
        empire_db_id: Young Empire DB ID (for writing style)
        viral_dna_db_id: Viral DNA DB ID
        dry_run: If True, simulate only

    Returns:
        WF3Result with generation summary

    Error Handling:
    - Style guide not found: Use default style
    - AI generation fails: Log error, continue
    - Cost limit exceeded: Stop workflow

    State Persistence: Save last processed production ID
    """
    result = WF3Result(total_processed=0, successful=0, failed=0, total_cost_usd=0.0, errors=[])

    # Fetch productions with status = "Researching" + has DNA sources
    filters = [
        NotionFilter(property="Status", condition="equals", value="Researching"),
        NotionFilter(property="Viral DNA sources", condition="is_not_empty", value=True)
    ]
    productions = fetch_db_entries(db_id=tracker_db_id, filters=filters)

    result.total_processed = len(productions.pages)

    for prod in productions.pages:
        try:
            # Extract production details
            title = prod['properties']['Title']['title'][0]['text']['content']
            channel = prod['properties']['Channel']['select']['name']
            format_type = prod['properties']['Format']['select']['name']
            dna_ids = [rel['id'] for rel in prod['properties']['Viral DNA sources']['relation']]

            # Read writing style
            writing_style = read_writing_style(channel, empire_db_id)

            # Fetch linked DNA
            dna_entries = [fetch_db_entry(dna_id, viral_dna_db_id) for dna_id in dna_ids]

            # Generate script
            script_gen = generate_script(title, format_type, dna_entries, writing_style)
            result.total_cost_usd += script_gen.cost_usd

            # Write to page body
            if not dry_run:
                script_blocks = [
                    {"type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "🎬 Generated Script"}}]}},
                    {"type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": script_gen.script}}]}}
                ]

                update_db_entry(
                    page_id=prod['id'],
                    append_blocks=script_blocks,
                    properties={"Status": {"status": {"name": "DNA matching"}}}
                )

            result.successful += 1

        except CostLimitExceeded as e:
            result.errors.append(f"Cost limit exceeded: {str(e)}")
            break
        except Exception as e:
            result.failed += 1
            result.errors.append(f"Production {prod['id']}: {str(e)}")
            continue

    save_workflow_state("WF3", result)
    return result
```

---

### WF3.1: Scene Breakdown

**State Machine**:
```
[START] → Fetch Productions with status="DNA matching" + has script in body (S01 + read blocks)
    ↓
    ├─→ [No entries] → EXIT (Success)
    └─→ [Has entries] → For each production:
            ↓
        Read script from page body
            ↓
        Generate Scene Breakdown (S19)
            ↓
        Write scene table to page body (S03)
            ↓
        Create Scene List entries (S02) [Optional]
            ↓
        Update status → "Ready to Render" (S03)
            ↓
        [NEXT ENTRY]
    ↓
[END] → Return summary
```

---

### WF4: Empire Week Review

**State Machine**:
```
[START] → Fetch Empire entries with status="Not started" (S01)
    ↓
    ├─→ [No entries] → EXIT (Success)
    └─→ [Has entries] → For each empire entry:
            ↓
        Extract time period (Year, Month, Week)
            ↓
        Query Productions for channel + time period (S01)
            ↓
        Fetch video performance for each (S10)
            ↓
        Generate Reviewing report (S13)
            ↓
        Write to page body (S03)
            ↓
        Update status → "Drafting" (S03)
            ↓
        [NEXT ENTRY]
    ↓
[END] → Return summary
```

---

### WF5: Empire Prospecting

**State Machine**:
```
[START] → Fetch Empire entries with status="Drafting" (S01)
    ↓
    ├─→ [No entries] → EXIT (Success)
    └─→ [Has entries] → For each empire entry:
            ↓
        Extract channel
            ↓
        Query DNA by channel tags (S01)
            ↓
        Generate Prospecting report (S13)
            ↓
        Write to page body (S03)
            ↓
        Optional: Create Production entries (S02)
            ↓
        Update status → "Published" (S03)
            ↓
        [NEXT ENTRY]
    ↓
[END] → Return summary
```

---

## 🔌 API Integration Contracts

### Notion API

**Rate Limits**: 3 requests/second

**Error Handling**:
```python
import time
from typing import Callable, TypeVar, Any

T = TypeVar('T')

def with_retry(
    func: Callable[..., T],
    max_retries: int = 3,
    backoff_factor: float = 2.0
) -> T:
    """
    Retry function with exponential backoff for rate limits.

    Args:
        func: Function to retry
        max_retries: Maximum retry attempts
        backoff_factor: Backoff multiplier (2.0 = double wait time each retry)

    Returns:
        Function result

    Raises:
        Original exception after max_retries exceeded
    """
    for attempt in range(max_retries):
        try:
            return func()
        except NotionRateLimitError as e:
            if attempt == max_retries - 1:
                raise
            wait_time = backoff_factor ** attempt
            time.sleep(wait_time)

    raise Exception("Max retries exceeded")
```

**Common Errors**:
- `400 Bad Request`: Invalid property format → validate before API call
- `404 Not Found`: Page/DB doesn't exist → check IDs
- `429 Too Many Requests`: Rate limit → retry with backoff
- `401 Unauthorized`: Invalid API key → check .env
- `403 Forbidden`: Integration not shared with DB → share DB with integration

---

### Claude AI API

**Models**:
- `claude-3-5-haiku-20241022`: $0.25/MTok input, $1.25/MTok output
- `claude-3-5-sonnet-20241022`: $3/MTok input, $15/MTok output
- `claude-opus-4-20250514`: $15/MTok input, $75/MTok output

**Cost Tracking**:
```python
import json
from pathlib import Path
from datetime import datetime, date

class CostTracker:
    def __init__(self, state_file: Path = Path("state/ai_costs.json")):
        self.state_file = state_file
        self.costs = self.load_costs()

    def load_costs(self) -> Dict:
        if self.state_file.exists():
            return json.loads(self.state_file.read_text())
        return {
            "daily": {},
            "monthly": {},
            "per_skill": {},
            "per_workflow": {}
        }

    def save_costs(self):
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(json.dumps(self.costs, indent=2))

    def add_cost(
        self,
        cost_usd: float,
        skill_name: str,
        workflow_name: Optional[str] = None
    ):
        today = date.today().isoformat()
        month = today[:7]  # YYYY-MM

        # Daily tracking
        self.costs["daily"][today] = self.costs["daily"].get(today, 0.0) + cost_usd

        # Monthly tracking
        self.costs["monthly"][month] = self.costs["monthly"].get(month, 0.0) + cost_usd

        # Per-skill tracking
        self.costs["per_skill"][skill_name] = self.costs["per_skill"].get(skill_name, 0.0) + cost_usd

        # Per-workflow tracking
        if workflow_name:
            self.costs["per_workflow"][workflow_name] = self.costs["per_workflow"].get(workflow_name, 0.0) + cost_usd

        self.save_costs()

        # Check limits
        self.check_limits()

    def check_limits(self):
        import os

        today = date.today().isoformat()
        month = today[:7]

        daily_cost = self.costs["daily"].get(today, 0.0)
        monthly_cost = self.costs["monthly"].get(month, 0.0)

        daily_soft = float(os.getenv("AI_DAILY_SOFT_LIMIT_USD", "5.0"))
        daily_hard = float(os.getenv("AI_DAILY_HARD_LIMIT_USD", "20.0"))
        monthly_soft = float(os.getenv("AI_MONTHLY_SOFT_LIMIT_USD", "100.0"))
        monthly_hard = float(os.getenv("AI_MONTHLY_HARD_LIMIT_USD", "500.0"))

        if daily_cost >= daily_hard or monthly_cost >= monthly_hard:
            raise CostLimitExceeded(f"Hard limit exceeded: Daily ${daily_cost:.2f}, Monthly ${monthly_cost:.2f}")

        if daily_cost >= daily_soft:
            print(f"⚠️  Warning: Daily AI cost ${daily_cost:.2f} exceeded soft limit ${daily_soft:.2f}")

        if monthly_cost >= monthly_soft:
            print(f"⚠️  Warning: Monthly AI cost ${monthly_cost:.2f} exceeded soft limit ${monthly_soft:.2f}")
```

---

## 📋 Configuration Schema

### databases.yaml

```yaml
databases:
  production_tracker:
    id: ${PROD_TRACKER_DB_ID}
    name: "Young Production Tracker"
    properties:
      Title:
        type: title
        required: true
      Status:
        type: status
        options: ["pending", "Idea", "Researching", "DNA matching", "Ready to Render", "Done"]
      Channel:
        type: select
        options: ["next10yearz", "orbity", "BioVibe"]
      Format:
        type: select
        options: ["shorts", "Video"]
      "Viral DNA sources":
        type: relation
        database: viral_dna
      "Published Date":
        type: date
      "production URL":
        type: url
      "Production Date":
        type: date
      "Voice ID":
        type: select
        options: ["Drew", "Adam", "Rachel"]
      "Rendered File":
        type: url

  viral_dna:
    id: ${VIRAL_DNA_DB_ID}
    name: "Viral DNA"
    properties:
      Title:
        type: title
        required: true
      URL:
        type: url
        required: true
      "Extracted Perspective":
        type: rich_text
      "Hook Potential":
        type: rich_text
      "Open Loop Seed":
        type: rich_text
      "Tags (niche)":
        type: multi_select
      "Info Type":
        type: multi_select
        options: ["Reel (Audio)", "Reel (Visual Only)", "Carousel", "Static Post", "Youtube Short", "Long Video"]
      Productions:
        type: relation
        database: production_tracker
      Creator:
        type: rich_text

  young_empire:
    id: ${YOUNG_EMPIRE_DB_ID}
    name: "Young Empire"
    properties:
      "Report Title":
        type: title
        required: true
      Status:
        type: status
        options: ["Not started", "Drafting", "Published"]
      Channel:
        type: select
        options: ["next10yearz", "Orbity", "BioVibe"]
      Year:
        type: select
      Month:
        type: select
      Week:
        type: select
        options: ["W1", "W2", "W3", "W4"]

  scene_list:
    id: ${SCENE_LIST_DB_ID}
    name: "Global Scene List"
    properties:
      Name:
        type: title
        required: true
      Production:
        type: relation
        database: production_tracker
        required: true
      Script:
        type: rich_text
      "Visual Prompt":
        type: rich_text
      Status:
        type: status
        options: ["Pending", "Downloading", "Error", "Ready"]
      Source:
        type: select
        options: ["Pexels", "Youtube", "Manual", "B-Roll Library", "AI-Generate"]
      "Source URL":
        type: url
      "Asset Path":
        type: rich_text
      "Duration (sec)":
        type: number
      "Source Timestamp":
        type: rich_text
```

### ai_config.yaml

```yaml
models:
  cheap: "claude-3-5-haiku-20241022"
  balanced: "claude-3-5-sonnet-20241022"
  premium: "claude-opus-4-20250514"

skill_model_mapping:
  # Classification tasks - cheap
  S08: "cheap"  # classify_info_type

  # Simple extraction - cheap
  S06: "cheap"  # generate_hook
  S07: "cheap"  # generate_open_loop
  S16: "cheap"  # link_dna_to_production (ranking)

  # Complex analysis - balanced
  S05: "balanced"  # extract_perspective
  S13: "balanced"  # generate_report
  S15: "balanced"  # generate_script
  S19: "balanced"  # generate_scene_breakdown

  # Critical decisions - premium (currently none)

cost_limits:
  daily_soft_usd: 5.00
  daily_hard_usd: 20.00
  monthly_soft_usd: 100.00
  monthly_hard_usd: 500.00

retry:
  max_attempts: 3
  backoff_factor: 2.0
```

---

## ⚠️ Error Handling Matrix

| Error Type | Affected Skills | Recovery Strategy | User Notification |
|------------|-----------------|-------------------|-------------------|
| `NotionAPIError` | S01, S02, S03 | Retry with backoff (3x) | Log error, continue |
| `NotionRateLimitError` | S01, S02, S03 | Wait + retry (exponential backoff) | Show progress bar |
| `PageNotFoundError` | S03, S14 | Skip entry, log error | Warning message |
| `PropertyNotFoundError` | S01, S02, S03 | Validate schema first | Fatal error, abort |
| `DownloadError` | S18 | Retry (2x), then skip | Log URL, continue |
| `TranscriptionError` | S04 | Try alternate OCR method, or skip | Log error, continue |
| `AIError` | S05-S08, S13, S15, S16, S19 | Retry (2x), then skip | Log error, continue |
| `CostLimitExceeded` | All AI skills | Stop workflow immediately | Alert user, show costs |
| `ValidationError` | S02, S03 | Abort operation | Show validation errors |
| `FileNotFoundError` | S04, S18 | Skip entry | Log error, continue |
| `StyleGuideNotFoundError` | S14 | Use default style | Warning, continue |

---

## 💰 Cost Tracking Requirements

### Per-Skill Tracking
- Track input tokens, output tokens, cost per call
- Store in `state/ai_costs.json` under `per_skill` key

### Per-Workflow Tracking
- Aggregate skill costs per workflow execution
- Store total workflow cost with timestamp

### Daily/Monthly Aggregation
- Auto-aggregate by date
- Check limits before each AI call
- Raise `CostLimitExceeded` if hard limit hit

### Cost Reporting
- CLI command: `./venv/bin/python3 src/run.py --show-costs`
- Display:
  - Today's cost
  - This month's cost
  - Cost breakdown by skill
  - Cost breakdown by workflow
  - Projected monthly cost (based on daily average)

---

## 🧪 Testing Requirements

### Unit Tests
- Test each skill independently with mock data
- Test error handling for each skill
- Test cost tracking

### Integration Tests
- Test workflows end-to-end with test data
- Test Notion API integration
- Test AI API integration

### Test Data
- Use Production Tracker "Test Entry" checkbox to flag test data
- Test workflows should skip test entries in scheduled runs
- Manual execution can process test entries

---

*This specification is the implementation blueprint. All functions must match these signatures.*

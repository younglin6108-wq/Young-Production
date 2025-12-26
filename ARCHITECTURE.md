# 🏛️ Young Production - System Architecture

> **Purpose**: System design, module structure, and data flows
>
> **Last Updated**: 2025-12-26

---

## 📐 Architecture Principles

### Core Principles
1. **Atomic Skills**: Each skill (S01-S21) does ONE thing well
2. **Stateless Skills**: Skills don't maintain state (state managed externally)
3. **Cost-First Design**: Optimize for minimal AI costs (OCR → rule-based → AI)
4. **Fail-Safe**: Errors in one entry don't break entire workflow
5. **Idempotent**: Workflows can be rerun safely (skip already processed)
6. **Observable**: All costs, errors, and progress are logged/tracked

---

## 🗂️ Module Structure

```
backend/src/
├── core/                    # Core infrastructure modules
│   ├── __init__.py
│   ├── notion_client.py     # Notion API wrapper (rate limiting, retries)
│   ├── ai_client.py         # Claude AI wrapper (cost tracking, model selection)
│   ├── config_loader.py     # Load databases.yaml, ai_config.yaml
│   └── exceptions.py        # Custom exceptions
│
├── skills/                  # Atomic skill functions (S01-S21)
│   ├── __init__.py
│   ├── crud.py              # S01-S03: Notion CRUD operations
│   ├── transcription.py     # S04: Whisper + OCR transcription
│   ├── scraping.py          # S18: yt-dlp + web scraping
│   ├── ai_analysis.py       # S05-S07: AI perspective/hook/loop extraction
│   ├── classification.py    # S08: Content type classification
│   ├── analytics.py         # S10: YouTube performance fetching
│   ├── reporting.py         # S13: Empire report generation
│   └── production.py        # S14-S16, S19-S21: Script/scene generation
│
├── workflows/               # Workflow orchestrators (WF1-WF5)
│   ├── __init__.py
│   ├── base.py              # Base workflow class (state management, dry-run)
│   ├── wf1_viral_dna_encoding.py
│   ├── wf2_dna_linking.py
│   ├── wf3_script_generation.py
│   ├── wf4_empire_review.py
│   └── wf5_empire_prospecting.py
│
├── utils/                   # Utility modules
│   ├── __init__.py
│   ├── logger.py            # Structured logging
│   ├── state_manager.py     # JSON state persistence
│   ├── cost_tracker.py      # AI cost tracking and limits
│   └── validators.py        # Schema validation helpers
│
├── cli/                     # CLI interface
│   ├── __init__.py
│   ├── interactive.py       # Interactive menu (for WF2 user approval)
│   └── commands.py          # Click/Typer command definitions
│
├── run.py                   # Main CLI entry point
├── inspect_db.py            # Schema inspector (existing)
├── check_connection.py      # Connection test (existing)
├── manual_check.py          # Test data creator (existing)
└── clear_dbs.py             # Test data cleanup (existing)
```

---

## 🔄 Data Flow Diagrams

### WF1: Viral DNA Encoding Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│ START: wf1_viral_dna_encoding()                                     │
└─────────────────────┬───────────────────────────────────────────────┘
                      │
                      ▼
         ┌────────────────────────────┐
         │ S17: fetch_unprocessed_dna │
         │ (Extracted Perspective empty)│
         └────────────┬───────────────┘
                      │
                      ▼
         ┌────────────────────────────┐
         │ For each DNA entry:        │
         └────────────┬───────────────┘
                      │
          ┌───────────▼───────────┐
          │ S08: classify_info_type│
          │ (Rule-based + AI)      │
          └───────────┬───────────┘
                      │
          ┌───────────▼───────────┐
          │ S18: scrape_url_content│
          │ (yt-dlp / BeautifulSoup)│
          └───────────┬───────────┘
                      │
          ┌───────────▼───────────┐
          │ S04: transcribe_content│
          │ (Whisper / OCR)        │
          └───────────┬───────────┘
                      │
          ┌───────────▼───────────┐
          │ S05: extract_perspective│
          │ (Claude Sonnet)        │
          ├───────────────────────┤
          │ S06: generate_hook     │
          │ (Claude Haiku)         │
          ├───────────────────────┤
          │ S07: generate_open_loop│
          │ (Claude Haiku)         │
          └───────────┬───────────┘
                      │
          ┌───────────▼───────────┐
          │ S03: update_db_entry   │
          │ (Update Viral DNA)     │
          └───────────┬───────────┘
                      │
                      ▼
         ┌────────────────────────────┐
         │ Save state to              │
         │ state/wf1_last_run.json    │
         └────────────┬───────────────┘
                      │
                      ▼
         ┌────────────────────────────┐
         │ RETURN: WF1Result          │
         │ (processed, failed, cost)  │
         └────────────────────────────┘
```

---

### WF3: Script Generation Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│ START: wf3_script_generation()                                      │
└─────────────────────┬───────────────────────────────────────────────┘
                      │
                      ▼
         ┌────────────────────────────┐
         │ S01: Fetch Productions     │
         │ (Status = "Researching"    │
         │  + has DNA sources)        │
         └────────────┬───────────────┘
                      │
                      ▼
         ┌────────────────────────────┐
         │ For each Production:       │
         └────────────┬───────────────┘
                      │
          ┌───────────▼───────────┐
          │ S14: read_writing_style│
          │ (From Empire page body)│
          └───────────┬───────────┘
                      │
          ┌───────────▼───────────┐
          │ S01: Fetch linked DNA  │
          │ (Relations from Prod)  │
          └───────────┬───────────┘
                      │
          ┌───────────▼───────────┐
          │ S15: generate_script   │
          │ (Claude Sonnet)        │
          │ Inputs:                │
          │ • Title                │
          │ • Format (shorts/video)│
          │ • DNA patterns         │
          │ • Writing style        │
          └───────────┬───────────┘
                      │
          ┌───────────▼───────────┐
          │ S03: Write to page body│
          │ (Append script blocks) │
          └───────────┬───────────┘
                      │
          ┌───────────▼───────────┐
          │ S03: Update status     │
          │ → "DNA matching"       │
          └───────────┬───────────┘
                      │
                      ▼
         ┌────────────────────────────┐
         │ RETURN: WF3Result          │
         └────────────────────────────┘
```

---

## 🧩 Module Dependencies

### Dependency Graph

```
run.py
  ├─→ cli/commands.py
  │     ├─→ workflows/wf1_viral_dna_encoding.py
  │     │     ├─→ skills/crud.py (S01, S03, S17)
  │     │     ├─→ skills/scraping.py (S18)
  │     │     ├─→ skills/transcription.py (S04)
  │     │     ├─→ skills/classification.py (S08)
  │     │     ├─→ skills/ai_analysis.py (S05, S06, S07)
  │     │     └─→ utils/cost_tracker.py
  │     │
  │     ├─→ workflows/wf2_dna_linking.py
  │     │     ├─→ skills/crud.py (S01, S03)
  │     │     ├─→ skills/production.py (S16)
  │     │     └─→ cli/interactive.py (user approval)
  │     │
  │     ├─→ workflows/wf3_script_generation.py
  │     │     ├─→ skills/crud.py (S01, S03)
  │     │     ├─→ skills/production.py (S14, S15)
  │     │     └─→ utils/cost_tracker.py
  │     │
  │     ├─→ workflows/wf4_empire_review.py
  │     │     ├─→ skills/crud.py (S01, S03)
  │     │     ├─→ skills/analytics.py (S10)
  │     │     ├─→ skills/reporting.py (S13)
  │     │     └─→ utils/cost_tracker.py
  │     │
  │     └─→ workflows/wf5_empire_prospecting.py
  │           ├─→ skills/crud.py (S01, S02, S03)
  │           ├─→ skills/reporting.py (S13)
  │           └─→ utils/cost_tracker.py
  │
  └─→ core/
        ├─→ notion_client.py (used by skills/crud.py)
        ├─→ ai_client.py (used by skills/ai_analysis.py, production.py, reporting.py)
        └─→ config_loader.py (used by all modules)
```

---

## 🔧 Core Module Designs

### core/notion_client.py

**Purpose**: Centralized Notion API access with rate limiting and retries

```python
from typing import Dict, Any, Optional, List
import time
import requests
from functools import wraps

class NotionClient:
    """
    Wrapper around Notion API with built-in rate limiting and retry logic.
    """

    def __init__(self, api_key: str, rate_limit_per_sec: float = 2.5):
        """
        Args:
            api_key: Notion integration API key
            rate_limit_per_sec: Requests per second (default 2.5 to stay under 3/sec limit)
        """
        self.api_key = api_key
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        self.min_interval = 1.0 / rate_limit_per_sec
        self.last_request_time = 0

    def _rate_limit(self):
        """Enforce rate limiting between requests."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_request_time = time.time()

    def _request(
        self,
        method: str,
        endpoint: str,
        json_data: Optional[Dict] = None,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """
        Make a rate-limited, retryable request to Notion API.

        Args:
            method: HTTP method (GET, POST, PATCH)
            endpoint: API endpoint (e.g., "/databases/{id}/query")
            json_data: JSON payload
            max_retries: Max retry attempts

        Returns:
            Response JSON

        Raises:
            NotionAPIError: If request fails after retries
        """
        url = f"{self.base_url}{endpoint}"

        for attempt in range(max_retries):
            self._rate_limit()

            try:
                response = requests.request(method, url, headers=self.headers, json=json_data)

                if response.status_code == 429:  # Rate limited
                    retry_after = int(response.headers.get("Retry-After", 2 ** attempt))
                    time.sleep(retry_after)
                    continue

                if response.status_code >= 400:
                    raise NotionAPIError(
                        f"Notion API error {response.status_code}: {response.text}",
                        status_code=response.status_code,
                        response_data=response.json() if response.text else None
                    )

                return response.json()

            except requests.RequestException as e:
                if attempt == max_retries - 1:
                    raise NotionAPIError(f"Request failed: {str(e)}")
                time.sleep(2 ** attempt)

        raise NotionAPIError("Max retries exceeded")

    def query_database(
        self,
        database_id: str,
        filter_obj: Optional[Dict] = None,
        sorts: Optional[List[Dict]] = None,
        start_cursor: Optional[str] = None,
        page_size: int = 100
    ) -> Dict[str, Any]:
        """Query a database with filters and pagination."""
        payload = {"page_size": page_size}
        if filter_obj:
            payload["filter"] = filter_obj
        if sorts:
            payload["sorts"] = sorts
        if start_cursor:
            payload["start_cursor"] = start_cursor

        return self._request("POST", f"/databases/{database_id}/query", json_data=payload)

    def get_page(self, page_id: str) -> Dict[str, Any]:
        """Retrieve a page by ID."""
        return self._request("GET", f"/pages/{page_id}")

    def create_page(self, database_id: str, properties: Dict, children: Optional[List] = None) -> Dict[str, Any]:
        """Create a new page in a database."""
        payload = {
            "parent": {"database_id": database_id},
            "properties": properties
        }
        if children:
            payload["children"] = children

        return self._request("POST", "/pages", json_data=payload)

    def update_page(self, page_id: str, properties: Optional[Dict] = None) -> Dict[str, Any]:
        """Update page properties."""
        payload = {}
        if properties:
            payload["properties"] = properties

        return self._request("PATCH", f"/pages/{page_id}", json_data=payload)

    def get_block_children(self, block_id: str, start_cursor: Optional[str] = None) -> Dict[str, Any]:
        """Get children blocks of a page/block."""
        endpoint = f"/blocks/{block_id}/children"
        if start_cursor:
            endpoint += f"?start_cursor={start_cursor}"

        return self._request("GET", endpoint)

    def append_block_children(self, block_id: str, children: List[Dict]) -> Dict[str, Any]:
        """Append blocks to a page."""
        payload = {"children": children}
        return self._request("PATCH", f"/blocks/{block_id}/children", json_data=payload)


# Singleton instance
_client_instance: Optional[NotionClient] = None

def get_notion_client() -> NotionClient:
    """Get or create NotionClient singleton."""
    global _client_instance
    if _client_instance is None:
        import os
        api_key = os.getenv("NOTION_API_KEY")
        if not api_key:
            raise ValueError("NOTION_API_KEY not found in environment")
        _client_instance = NotionClient(api_key)
    return _client_instance
```

---

### core/ai_client.py

**Purpose**: Claude AI wrapper with cost tracking and model selection

```python
import os
import anthropic
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from utils.cost_tracker import CostTracker

@dataclass
class AIResponse:
    text: str
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float

class AIClient:
    """
    Wrapper around Anthropic Claude API with cost tracking and model selection.
    """

    # Token costs per million tokens (MTok)
    COSTS = {
        "claude-3-5-haiku-20241022": {"input": 0.25, "output": 1.25},
        "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00},
        "claude-opus-4-20250514": {"input": 15.00, "output": 75.00}
    }

    def __init__(self, api_key: str, cost_tracker: Optional[CostTracker] = None):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.cost_tracker = cost_tracker or CostTracker()

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        model: str = "claude-3-5-sonnet-20241022",
        max_tokens: int = 4096,
        temperature: float = 1.0
    ) -> AIResponse:
        """
        Generate text using Claude API.

        Args:
            prompt: User prompt
            system: Optional system prompt
            model: Model ID
            max_tokens: Max output tokens
            temperature: Sampling temperature (0-1)

        Returns:
            AIResponse with generated text and cost

        Raises:
            CostLimitExceeded: If cost limits exceeded
            AIError: If API call fails
        """
        # Check cost limits before making call
        self.cost_tracker.check_limits()

        try:
            messages = [{"role": "user", "content": prompt}]

            kwargs = {
                "model": model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": messages
            }

            if system:
                kwargs["system"] = system

            response = self.client.messages.create(**kwargs)

            # Calculate cost
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            cost_usd = (
                (input_tokens / 1_000_000) * self.COSTS[model]["input"] +
                (output_tokens / 1_000_000) * self.COSTS[model]["output"]
            )

            # Extract text
            text = response.content[0].text

            return AIResponse(
                text=text,
                model=model,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost_usd=cost_usd
            )

        except anthropic.APIError as e:
            raise AIError(f"Claude API error: {str(e)}")

    def generate_with_cost_tracking(
        self,
        prompt: str,
        skill_name: str,
        workflow_name: Optional[str] = None,
        **kwargs
    ) -> AIResponse:
        """
        Generate text and automatically track costs.

        Args:
            prompt: User prompt
            skill_name: Skill identifier (e.g., "S05")
            workflow_name: Optional workflow identifier (e.g., "WF1")
            **kwargs: Passed to generate()

        Returns:
            AIResponse
        """
        response = self.generate(prompt, **kwargs)
        self.cost_tracker.add_cost(response.cost_usd, skill_name, workflow_name)
        return response


# Singleton instance
_ai_client_instance: Optional[AIClient] = None

def get_ai_client() -> AIClient:
    """Get or create AIClient singleton."""
    global _ai_client_instance
    if _ai_client_instance is None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")
        _ai_client_instance = AIClient(api_key)
    return _ai_client_instance
```

---

### core/config_loader.py

**Purpose**: Load and validate configuration files

```python
import os
import yaml
from pathlib import Path
from typing import Dict, Any
from string import Template

class ConfigLoader:
    """
    Load configuration files with environment variable substitution.
    """

    def __init__(self, config_dir: Path = Path("config")):
        self.config_dir = config_dir

    def load_yaml(self, filename: str) -> Dict[str, Any]:
        """
        Load YAML file with ${ENV_VAR} substitution.

        Args:
            filename: Config filename (e.g., "databases.yaml")

        Returns:
            Parsed configuration dict

        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If required env vars missing
        """
        filepath = self.config_dir / filename

        if not filepath.exists():
            raise FileNotFoundError(f"Config file not found: {filepath}")

        # Read file
        content = filepath.read_text()

        # Substitute environment variables
        template = Template(content)
        substituted = template.safe_substitute(os.environ)

        # Parse YAML
        config = yaml.safe_load(substituted)

        return config

    def get_database_config(self, db_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific database.

        Args:
            db_name: Database key (e.g., "production_tracker")

        Returns:
            Database configuration dict

        Raises:
            KeyError: If database not found in config
        """
        databases = self.load_yaml("databases.yaml")
        return databases["databases"][db_name]

    def get_ai_config(self) -> Dict[str, Any]:
        """Get AI configuration (models, costs, limits)."""
        return self.load_yaml("ai_config.yaml")


# Singleton instance
_config_loader_instance: Optional[ConfigLoader] = None

def get_config_loader() -> ConfigLoader:
    """Get or create ConfigLoader singleton."""
    global _config_loader_instance
    if _config_loader_instance is None:
        _config_loader_instance = ConfigLoader()
    return _config_loader_instance
```

---

## 🔀 Workflow Base Class

### workflows/base.py

**Purpose**: Base class for all workflows with common functionality

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar, Optional, Dict, Any
from pathlib import Path
import json
from datetime import datetime

T = TypeVar('T')

@dataclass
class WorkflowResult(Generic[T]):
    """Generic workflow result."""
    workflow_name: str
    total_processed: int
    successful: int
    failed: int
    skipped: int
    total_cost_usd: float
    errors: list[str]
    started_at: str
    completed_at: str
    dry_run: bool
    data: Optional[T] = None  # Workflow-specific data

class BaseWorkflow(ABC):
    """
    Base class for all workflows with state management and dry-run support.
    """

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.state_file = Path(f"state/{self.workflow_name()}_last_run.json")

    @abstractmethod
    def workflow_name(self) -> str:
        """Return workflow identifier (e.g., 'WF1')."""
        pass

    @abstractmethod
    def execute(self, **kwargs) -> WorkflowResult:
        """Execute the workflow logic."""
        pass

    def run(self, **kwargs) -> WorkflowResult:
        """
        Run the workflow with state management.

        Args:
            **kwargs: Workflow-specific arguments

        Returns:
            WorkflowResult
        """
        started_at = datetime.now().isoformat()

        result = self.execute(**kwargs)
        result.started_at = started_at
        result.completed_at = datetime.now().isoformat()
        result.dry_run = self.dry_run

        # Save state
        self.save_state(result)

        return result

    def save_state(self, result: WorkflowResult):
        """Save workflow state to JSON file."""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

        state = {
            "last_run": result.completed_at,
            "total_processed": result.total_processed,
            "successful": result.successful,
            "failed": result.failed,
            "total_cost_usd": result.total_cost_usd,
            "dry_run": result.dry_run
        }

        self.state_file.write_text(json.dumps(state, indent=2))

    def load_state(self) -> Optional[Dict[str, Any]]:
        """Load last workflow state."""
        if self.state_file.exists():
            return json.loads(self.state_file.read_text())
        return None
```

---

## 🎨 CLI Design

### cli/interactive.py

**Purpose**: Interactive user prompts for hybrid workflows (WF2)

```python
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class UserChoice:
    action: str  # "approve", "modify", "skip"
    selected_ids: List[str]  # Selected DNA IDs (if action = "modify")

def prompt_dna_link_approval(
    production_title: str,
    suggestions: List[Dict[str, Any]]
) -> UserChoice:
    """
    Prompt user to approve/modify/skip DNA link suggestions.

    Args:
        production_title: Video title
        suggestions: List of DNALinkSuggestion objects

    Returns:
        UserChoice with user decision
    """
    print(f"\n{'='*70}")
    print(f"📹 Production: {production_title}")
    print(f"{'='*70}")
    print(f"\n🧬 Suggested Viral DNA Sources ({len(suggestions)}):\n")

    for i, sug in enumerate(suggestions):
        print(f"  [{i+1}] {sug.dna_title}")
        print(f"      Relevance: {sug.relevance_score:.0%}")
        print(f"      Reason: {sug.reasoning}")
        print(f"      Matching Tags: {', '.join(sug.matching_tags)}\n")

    print(f"{'='*70}")
    choice = input("\n[A]pprove all / [M]odify selection / [S]kip? ").strip().upper()

    if choice == 'A':
        return UserChoice(action="approve", selected_ids=[s.dna_id for s in suggestions])

    elif choice == 'M':
        print("\nSelect DNA entries to link (space-separated numbers):")
        selected_nums = input("Enter numbers (e.g., 1 3 5): ").strip().split()
        selected_ids = []

        for num_str in selected_nums:
            try:
                idx = int(num_str) - 1
                if 0 <= idx < len(suggestions):
                    selected_ids.append(suggestions[idx].dna_id)
            except ValueError:
                continue

        return UserChoice(action="modify", selected_ids=selected_ids)

    else:  # Skip
        return UserChoice(action="skip", selected_ids=[])
```

---

## 📊 State Management

### State Files Structure

```
state/
├── wf1_last_run.json        # WF1 state
│   {
│     "last_run": "2025-12-26T10:30:00",
│     "total_processed": 15,
│     "successful": 12,
│     "failed": 3,
│     "total_cost_usd": 2.45,
│     "dry_run": false
│   }
│
├── wf2_last_run.json        # WF2 state
├── wf3_last_run.json        # WF3 state
├── wf4_last_run.json        # WF4 state
├── wf5_last_run.json        # WF5 state
│
├── ai_costs.json            # Cost tracking
│   {
│     "daily": {
│       "2025-12-26": 5.67,
│       "2025-12-25": 3.21
│     },
│     "monthly": {
│       "2025-12": 45.32
│     },
│     "per_skill": {
│       "S05": 15.20,
│       "S15": 18.50
│     },
│     "per_workflow": {
│       "WF1": 25.30,
│       "WF3": 20.02
│     }
│   }
│
└── processed_entries.json   # Idempotency tracking
    {
      "viral_dna": [
        "2d3cd90f-688c-...",  # Processed DNA IDs
        "2d4cd90f-688c-..."
      ],
      "productions": [
        "2d5cd90f-688c-..."   # Processed Production IDs
      ]
    }
```

---

## 🧪 Testing Architecture

### Test Structure

```
backend/tests/
├── conftest.py              # Pytest fixtures
├── test_core/
│   ├── test_notion_client.py
│   ├── test_ai_client.py
│   └── test_config_loader.py
├── test_skills/
│   ├── test_crud.py         # S01-S03
│   ├── test_transcription.py # S04
│   ├── test_scraping.py     # S18
│   ├── test_ai_analysis.py  # S05-S07
│   └── test_production.py   # S14-S16
└── test_workflows/
    ├── test_wf1.py
    ├── test_wf2.py
    ├── test_wf3.py
    ├── test_wf4.py
    └── test_wf5.py
```

### Test Fixtures

```python
# conftest.py
import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_notion_client():
    """Mock NotionClient for testing."""
    client = Mock()
    client.query_database.return_value = {"results": [], "has_more": False}
    return client

@pytest.fixture
def mock_ai_client():
    """Mock AIClient for testing."""
    client = Mock()
    client.generate.return_value = AIResponse(
        text="Mocked AI response",
        model="claude-3-5-haiku-20241022",
        input_tokens=100,
        output_tokens=200,
        cost_usd=0.01
    )
    return client

@pytest.fixture
def sample_viral_dna_entry():
    """Sample Viral DNA entry for testing."""
    return {
        "id": "test-dna-id-001",
        "properties": {
            "Title": {"title": [{"text": {"content": "Test Viral Video"}}]},
            "URL": {"url": "https://youtube.com/watch?v=test123"},
            "Extracted Perspective": {"rich_text": []},
            "Tags (niche)": {"multi_select": [{"name": "AI"}, {"name": "Productivity"}]}
        }
    }
```

---

*This architecture document defines the system structure. Follow these patterns when implementing modules.*

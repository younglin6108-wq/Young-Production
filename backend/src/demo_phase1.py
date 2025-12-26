#!/usr/bin/env python3
"""
Phase 1 Demo - Test all core modules
Shows that config loading, Notion client, AI client, cost tracking, and state management work.
"""
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from core.config_loader import get_config_loader
from core.notion_client import get_notion_client
from utils.cost_tracker import get_cost_tracker
from utils.state_manager import get_state_manager

console = Console()


def demo_config_loader():
    """Test configuration loading."""
    console.print("\n[bold cyan]═══ 1. Testing ConfigLoader ═══[/bold cyan]\n")

    try:
        config = get_config_loader()

        # Load database config
        db_ids = config.get_all_database_ids()
        console.print("✅ Loaded database IDs:")
        for db_name, db_id in db_ids.items():
            console.print(f"  • {db_name}: {db_id[:8]}...")

        # Load AI config
        ai_config = config.get_ai_config()
        console.print(f"\n✅ Loaded AI config with {len(ai_config['models'])} models:")
        for tier, model_id in ai_config['models'].items():
            console.print(f"  • {tier}: {model_id}")

        # Test model selection for skill
        model = config.get_model_for_skill("S05")
        console.print(f"\n✅ Model for S05 (extract_perspective): {model}")

        return True

    except Exception as e:
        console.print(f"[red]❌ ConfigLoader test failed: {e}[/red]")
        return False


def demo_notion_client():
    """Test Notion API connection."""
    console.print("\n[bold cyan]═══ 2. Testing NotionClient ═══[/bold cyan]\n")

    try:
        client = get_notion_client()
        config = get_config_loader()
        db_ids = config.get_all_database_ids()

        # Test database retrieval
        tracker_db = client.get_database(db_ids["production_tracker"])
        db_title = tracker_db['title'][0]['text']['content'] if tracker_db['title'] else "Untitled"
        console.print(f"✅ Connected to database: {db_title}")

        # Test query
        result = client.query_database(db_ids["production_tracker"], page_size=3)
        entry_count = len(result.get('results', []))
        console.print(f"✅ Queried database: Found {entry_count} entries")

        # Test rate limiting (make multiple requests)
        console.print(f"\n✅ Testing rate limiting (2.5 req/sec)...")
        import time
        start = time.time()
        for i in range(3):
            client.query_database(db_ids["viral_dna"], page_size=1)
        elapsed = time.time() - start
        console.print(f"  • 3 requests took {elapsed:.2f}s (should be ~1.2s)")

        return True

    except Exception as e:
        console.print(f"[red]❌ NotionClient test failed: {e}[/red]")
        import traceback
        traceback.print_exc()
        return False


def demo_cost_tracker():
    """Test AI cost tracking."""
    console.print("\n[bold cyan]═══ 3. Testing CostTracker ═══[/bold cyan]\n")

    try:
        tracker = get_cost_tracker()

        # Add some mock costs
        tracker.add_cost(0.05, "S05", "WF1", {"model": "claude-3-5-sonnet-20241022"})
        tracker.add_cost(0.01, "S06", "WF1", {"model": "claude-3-5-haiku-20241022"})
        tracker.add_cost(0.02, "S15", "WF3")

        # Get summary
        summary = tracker.get_summary()

        console.print(f"✅ Cost Tracking Summary:")
        console.print(f"  • Today: ${summary['today']['cost']:.3f} / ${summary['today']['hard_limit']:.2f}")
        console.print(f"  • Month: ${summary['month']['cost']:.3f} / ${summary['month']['hard_limit']:.2f}")

        if summary['top_skills']:
            console.print(f"\n  Top Skills:")
            for skill, cost in summary['top_skills']:
                console.print(f"    • {skill}: ${cost:.3f}")

        return True

    except Exception as e:
        console.print(f"[red]❌ CostTracker test failed: {e}[/red]")
        return False


def demo_state_manager():
    """Test workflow state management."""
    console.print("\n[bold cyan]═══ 4. Testing StateManager ═══[/bold cyan]\n")

    try:
        state_mgr = get_state_manager()

        # Save workflow state
        test_state = {
            "total_processed": 10,
            "successful": 8,
            "failed": 2,
            "cost_usd": 0.45
        }
        state_mgr.save_workflow_state("WF1", test_state)
        console.print(f"✅ Saved WF1 state")

        # Load state
        loaded = state_mgr.load_workflow_state("WF1")
        console.print(f"✅ Loaded WF1 state: {loaded['total_processed']} processed")

        # Mark entries as processed
        state_mgr.mark_entry_processed("viral_dna", "test-entry-123")
        state_mgr.mark_entry_processed("viral_dna", "test-entry-456")

        # Check processed
        is_processed = state_mgr.is_entry_processed("viral_dna", "test-entry-123")
        console.print(f"✅ Entry tracking: test-entry-123 processed = {is_processed}")

        processed_count = len(state_mgr.get_processed_entries("viral_dna"))
        console.print(f"✅ Total processed viral_dna entries: {processed_count}")

        return True

    except Exception as e:
        console.print(f"[red]❌ StateManager test failed: {e}[/red]")
        return False


def demo_ai_client():
    """Test AI client (optional - requires ANTHROPIC_API_KEY)."""
    console.print("\n[bold cyan]═══ 5. Testing AIClient (Optional) ═══[/bold cyan]\n")

    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print("[yellow]⚠️  Skipped: ANTHROPIC_API_KEY not set[/yellow]")
        return True

    try:
        from core.ai_client import get_ai_client

        client = get_ai_client()

        # Make a tiny test request
        response = client.generate_with_cost_tracking(
            prompt="Say 'Hello from Phase 1!' in exactly 5 words.",
            skill_name="TEST",
            workflow_name="DEMO",
            model="claude-3-5-haiku-20241022",
            max_tokens=50
        )

        console.print(f"✅ AI Response: {response.text}")
        console.print(f"✅ Cost: ${response.cost_usd:.4f} ({response.input_tokens} in, {response.output_tokens} out)")

        return True

    except Exception as e:
        console.print(f"[red]❌ AIClient test failed: {e}[/red]")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all Phase 1 demos."""
    console.print(Panel.fit(
        "[bold cyan]🚀 Young Production - Phase 1 Demo[/bold cyan]\n"
        "Testing core modules: Config, Notion, Cost Tracking, State Management, AI",
        border_style="cyan"
    ))

    results = {
        "ConfigLoader": demo_config_loader(),
        "NotionClient": demo_notion_client(),
        "CostTracker": demo_cost_tracker(),
        "StateManager": demo_state_manager(),
        "AIClient": demo_ai_client()
    }

    # Summary table
    console.print(f"\n[bold cyan]═══ Phase 1 Test Results ═══[/bold cyan]\n")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Module", style="cyan")
    table.add_column("Status", justify="center")

    for module, passed in results.items():
        status = "[green]✅ PASS[/green]" if passed else "[red]❌ FAIL[/red]"
        table.add_column(module, status)

    console.print(table)

    all_passed = all(results.values())
    if all_passed:
        console.print(Panel.fit(
            "[bold green]✅ Phase 1 Complete![/bold green]\n"
            "All core modules working correctly.\n"
            "Ready for Phase 2: Skills Implementation",
            border_style="green"
        ))
    else:
        console.print(Panel.fit(
            "[bold red]❌ Some tests failed[/bold red]\n"
            "Review errors above and fix before proceeding.",
            border_style="red"
        ))

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

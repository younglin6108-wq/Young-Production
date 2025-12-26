"""
State management for workflows and processed entries (idempotency).
"""
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime


class StateManager:
    """
    Manage workflow state and track processed entries for idempotency.
    """

    def __init__(self, state_dir: Optional[Path] = None):
        """
        Initialize StateManager.

        Args:
            state_dir: Path to state directory. Defaults to backend/state
        """
        if state_dir is None:
            backend_dir = Path(__file__).parent.parent.parent
            state_dir = backend_dir / "state"

        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)

    def save_workflow_state(self, workflow_name: str, state: Dict[str, Any]):
        """
        Save workflow execution state.

        Args:
            workflow_name: Workflow identifier (e.g., "WF1")
            state: State dictionary to save
        """
        state_file = self.state_dir / f"{workflow_name.lower()}_last_run.json"

        # Add timestamp
        state["last_updated"] = datetime.now().isoformat()

        state_file.write_text(json.dumps(state, indent=2))

    def load_workflow_state(self, workflow_name: str) -> Optional[Dict[str, Any]]:
        """
        Load last workflow execution state.

        Args:
            workflow_name: Workflow identifier (e.g., "WF1")

        Returns:
            State dictionary or None if no state exists
        """
        state_file = self.state_dir / f"{workflow_name.lower()}_last_run.json"

        if not state_file.exists():
            return None

        return json.loads(state_file.read_text())

    def mark_entry_processed(self, db_name: str, entry_id: str):
        """
        Mark a database entry as processed (for idempotency).

        Args:
            db_name: Database name (e.g., "viral_dna", "production_tracker")
            entry_id: Notion page ID
        """
        processed_file = self.state_dir / "processed_entries.json"

        if processed_file.exists():
            processed = json.loads(processed_file.read_text())
        else:
            processed = {}

        if db_name not in processed:
            processed[db_name] = []

        if entry_id not in processed[db_name]:
            processed[db_name].append(entry_id)

        processed_file.write_text(json.dumps(processed, indent=2))

    def is_entry_processed(self, db_name: str, entry_id: str) -> bool:
        """
        Check if an entry has been processed.

        Args:
            db_name: Database name
            entry_id: Notion page ID

        Returns:
            True if already processed, False otherwise
        """
        processed_file = self.state_dir / "processed_entries.json"

        if not processed_file.exists():
            return False

        processed = json.loads(processed_file.read_text())
        return entry_id in processed.get(db_name, [])

    def get_processed_entries(self, db_name: str) -> List[str]:
        """
        Get list of processed entry IDs for a database.

        Args:
            db_name: Database name

        Returns:
            List of processed entry IDs
        """
        processed_file = self.state_dir / "processed_entries.json"

        if not processed_file.exists():
            return []

        processed = json.loads(processed_file.read_text())
        return processed.get(db_name, [])

    def clear_processed_entries(self, db_name: Optional[str] = None):
        """
        Clear processed entries tracking.

        Args:
            db_name: If provided, clear only this database. Otherwise clear all.
        """
        processed_file = self.state_dir / "processed_entries.json"

        if not processed_file.exists():
            return

        if db_name is None:
            # Clear all
            processed_file.write_text(json.dumps({}, indent=2))
        else:
            # Clear specific database
            processed = json.loads(processed_file.read_text())
            if db_name in processed:
                processed[db_name] = []
                processed_file.write_text(json.dumps(processed, indent=2))


# Singleton instance
_state_manager_instance: Optional[StateManager] = None


def get_state_manager() -> StateManager:
    """Get or create StateManager singleton."""
    global _state_manager_instance
    if _state_manager_instance is None:
        _state_manager_instance = StateManager()
    return _state_manager_instance

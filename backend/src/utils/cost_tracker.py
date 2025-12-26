"""
AI cost tracking with daily/monthly limits and per-skill/workflow breakdown.
"""
import json
import os
from pathlib import Path
from datetime import datetime, date
from typing import Dict, Optional
from core.exceptions import CostLimitExceeded


class CostTracker:
    """
    Track AI costs with limits and breakdowns.
    State stored in state/ai_costs.json
    """

    def __init__(self, state_file: Optional[Path] = None):
        """
        Initialize CostTracker.

        Args:
            state_file: Path to cost tracking file. Defaults to state/ai_costs.json
        """
        if state_file is None:
            backend_dir = Path(__file__).parent.parent.parent
            state_file = backend_dir / "state" / "ai_costs.json"

        self.state_file = Path(state_file)
        self.costs = self.load_costs()

        # Load limits from environment
        self.daily_soft_limit = float(os.getenv("AI_DAILY_SOFT_LIMIT_USD", "5.00"))
        self.daily_hard_limit = float(os.getenv("AI_DAILY_HARD_LIMIT_USD", "20.00"))
        self.monthly_soft_limit = float(os.getenv("AI_MONTHLY_SOFT_LIMIT_USD", "100.00"))
        self.monthly_hard_limit = float(os.getenv("AI_MONTHLY_HARD_LIMIT_USD", "500.00"))

    def load_costs(self) -> Dict:
        """Load costs from JSON file."""
        if self.state_file.exists():
            return json.loads(self.state_file.read_text())
        return {
            "daily": {},
            "monthly": {},
            "per_skill": {},
            "per_workflow": {},
            "history": []
        }

    def save_costs(self):
        """Save costs to JSON file."""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(json.dumps(self.costs, indent=2))

    def add_cost(
        self,
        cost_usd: float,
        skill_name: str,
        workflow_name: Optional[str] = None,
        details: Optional[Dict] = None
    ):
        """
        Add a cost entry and check limits.

        Args:
            cost_usd: Cost in USD
            skill_name: Skill identifier (e.g., "S05")
            workflow_name: Optional workflow identifier (e.g., "WF1")
            details: Optional additional details (model, tokens, etc.)

        Raises:
            CostLimitExceeded: If hard limit exceeded
        """
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

        # History tracking
        self.costs["history"].append({
            "timestamp": datetime.now().isoformat(),
            "cost_usd": cost_usd,
            "skill": skill_name,
            "workflow": workflow_name,
            "details": details
        })

        # Keep only last 1000 history entries
        if len(self.costs["history"]) > 1000:
            self.costs["history"] = self.costs["history"][-1000:]

        self.save_costs()

        # Check limits
        self.check_limits()

    def check_limits(self):
        """
        Check if cost limits are exceeded.

        Raises:
            CostLimitExceeded: If hard limit exceeded
        """
        today = date.today().isoformat()
        month = today[:7]

        daily_cost = self.costs["daily"].get(today, 0.0)
        monthly_cost = self.costs["monthly"].get(month, 0.0)

        # Hard limits (raise exception)
        if daily_cost >= self.daily_hard_limit:
            raise CostLimitExceeded(
                f"Daily hard limit exceeded: ${daily_cost:.2f} / ${self.daily_hard_limit:.2f}",
                daily_cost=daily_cost,
                monthly_cost=monthly_cost
            )

        if monthly_cost >= self.monthly_hard_limit:
            raise CostLimitExceeded(
                f"Monthly hard limit exceeded: ${monthly_cost:.2f} / ${self.monthly_hard_limit:.2f}",
                daily_cost=daily_cost,
                monthly_cost=monthly_cost
            )

        # Soft limits (warnings only)
        if daily_cost >= self.daily_soft_limit:
            print(f"⚠️  Warning: Daily AI cost ${daily_cost:.2f} exceeded soft limit ${self.daily_soft_limit:.2f}")

        if monthly_cost >= self.monthly_soft_limit:
            print(f"⚠️  Warning: Monthly AI cost ${monthly_cost:.2f} exceeded soft limit ${self.monthly_soft_limit:.2f}")

    def get_today_cost(self) -> float:
        """Get today's total cost."""
        today = date.today().isoformat()
        return self.costs["daily"].get(today, 0.0)

    def get_month_cost(self) -> float:
        """Get this month's total cost."""
        month = date.today().isoformat()[:7]
        return self.costs["monthly"].get(month, 0.0)

    def get_skill_cost(self, skill_name: str) -> float:
        """Get total cost for a specific skill."""
        return self.costs["per_skill"].get(skill_name, 0.0)

    def get_workflow_cost(self, workflow_name: str) -> float:
        """Get total cost for a specific workflow."""
        return self.costs["per_workflow"].get(workflow_name, 0.0)

    def get_summary(self) -> Dict:
        """
        Get cost summary.

        Returns:
            Dict with today's cost, month cost, limits, and top spenders
        """
        today_cost = self.get_today_cost()
        month_cost = self.get_month_cost()

        # Top 5 skills by cost
        top_skills = sorted(
            self.costs["per_skill"].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        # Top 5 workflows by cost
        top_workflows = sorted(
            self.costs["per_workflow"].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        return {
            "today": {
                "cost": today_cost,
                "soft_limit": self.daily_soft_limit,
                "hard_limit": self.daily_hard_limit,
                "remaining": self.daily_hard_limit - today_cost
            },
            "month": {
                "cost": month_cost,
                "soft_limit": self.monthly_soft_limit,
                "hard_limit": self.monthly_hard_limit,
                "remaining": self.monthly_hard_limit - month_cost
            },
            "top_skills": top_skills,
            "top_workflows": top_workflows
        }


# Singleton instance
_cost_tracker_instance: Optional[CostTracker] = None


def get_cost_tracker() -> CostTracker:
    """Get or create CostTracker singleton."""
    global _cost_tracker_instance
    if _cost_tracker_instance is None:
        _cost_tracker_instance = CostTracker()
    return _cost_tracker_instance

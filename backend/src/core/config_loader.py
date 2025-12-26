"""
Configuration loader for YAML files with environment variable substitution.
"""
import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from string import Template


class ConfigLoader:
    """
    Load configuration files with ${ENV_VAR} substitution.
    """

    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize ConfigLoader.

        Args:
            config_dir: Path to config directory. Defaults to backend/config
        """
        if config_dir is None:
            # Default to backend/config relative to this file
            backend_dir = Path(__file__).parent.parent.parent
            config_dir = backend_dir / "config"

        self.config_dir = Path(config_dir)

        if not self.config_dir.exists():
            raise FileNotFoundError(f"Config directory not found: {self.config_dir}")

    def load_yaml(self, filename: str) -> Dict[str, Any]:
        """
        Load YAML file with ${ENV_VAR} substitution.

        Args:
            filename: Config filename (e.g., "databases.yaml")

        Returns:
            Parsed configuration dict

        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If required env vars missing (shows as ${VAR_NAME} in output)
        """
        filepath = self.config_dir / filename

        if not filepath.exists():
            raise FileNotFoundError(f"Config file not found: {filepath}")

        # Read file
        content = filepath.read_text()

        # Substitute environment variables
        template = Template(content)
        substituted = template.safe_substitute(os.environ)

        # Check for unsubstituted variables
        if "${" in substituted:
            # Extract unsubstituted variable names
            import re
            unsubstituted = re.findall(r'\$\{([^}]+)\}', substituted)
            raise ValueError(
                f"Missing environment variables in {filename}: {', '.join(unsubstituted)}"
            )

        # Parse YAML
        config = yaml.safe_load(substituted)

        return config

    def get_database_config(self, db_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific database.

        Args:
            db_name: Database key (e.g., "production_tracker", "viral_dna")

        Returns:
            Database configuration dict with 'id', 'name', 'properties'

        Raises:
            KeyError: If database not found in config
        """
        databases = self.load_yaml("databases.yaml")

        if db_name not in databases.get("databases", {}):
            available = list(databases.get("databases", {}).keys())
            raise KeyError(
                f"Database '{db_name}' not found in databases.yaml. "
                f"Available: {', '.join(available)}"
            )

        return databases["databases"][db_name]

    def get_all_database_ids(self) -> Dict[str, str]:
        """
        Get all database IDs as a dict.

        Returns:
            Dict mapping database names to IDs
            Example: {"production_tracker": "abc123", "viral_dna": "def456"}
        """
        databases = self.load_yaml("databases.yaml")
        return {
            name: db_config["id"]
            for name, db_config in databases.get("databases", {}).items()
        }

    def get_ai_config(self) -> Dict[str, Any]:
        """
        Get AI configuration (models, costs, limits).

        Returns:
            AI configuration dict with 'models', 'skill_model_mapping', 'cost_limits', 'retry'
        """
        return self.load_yaml("ai_config.yaml")

    def get_model_for_skill(self, skill_id: str) -> str:
        """
        Get the AI model to use for a specific skill.

        Args:
            skill_id: Skill identifier (e.g., "S05", "S15")

        Returns:
            Model ID (e.g., "claude-3-5-sonnet-20241022")

        Raises:
            KeyError: If skill not found in mapping
        """
        ai_config = self.get_ai_config()
        model_tier = ai_config["skill_model_mapping"].get(skill_id)

        if model_tier is None:
            raise KeyError(
                f"Skill '{skill_id}' not found in ai_config.yaml skill_model_mapping"
            )

        return ai_config["models"][model_tier]


# Singleton instance
_config_loader_instance: Optional[ConfigLoader] = None


def get_config_loader() -> ConfigLoader:
    """Get or create ConfigLoader singleton."""
    global _config_loader_instance
    if _config_loader_instance is None:
        _config_loader_instance = ConfigLoader()
    return _config_loader_instance

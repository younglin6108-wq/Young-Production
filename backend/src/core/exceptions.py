"""
Custom exceptions for Young Production system.
All exceptions inherit from YoungProductionError base class.
"""

class YoungProductionError(Exception):
    """Base exception for all Young Production errors."""
    pass


# === Notion API Errors ===

class NotionAPIError(YoungProductionError):
    """Base exception for Notion API errors."""
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class NotionRateLimitError(NotionAPIError):
    """Raised when Notion API rate limit is exceeded."""
    def __init__(self, retry_after: int = None):
        super().__init__(f"Notion API rate limit exceeded. Retry after {retry_after}s")
        self.retry_after = retry_after


class PageNotFoundError(NotionAPIError):
    """Raised when a Notion page is not found."""
    pass


class PropertyNotFoundError(NotionAPIError):
    """Raised when a required property is not found in Notion page/database."""
    def __init__(self, property_name: str, page_or_db: str):
        super().__init__(f"Property '{property_name}' not found in {page_or_db}")
        self.property_name = property_name


# === AI Errors ===

class AIError(YoungProductionError):
    """Base exception for AI-related errors."""
    pass


class CostLimitExceeded(AIError):
    """Raised when AI cost limits are exceeded."""
    def __init__(self, message: str, daily_cost: float = None, monthly_cost: float = None):
        super().__init__(message)
        self.daily_cost = daily_cost
        self.monthly_cost = monthly_cost


# === Content Processing Errors ===

class DownloadError(YoungProductionError):
    """Raised when content download fails."""
    def __init__(self, url: str, reason: str):
        super().__init__(f"Failed to download {url}: {reason}")
        self.url = url
        self.reason = reason


class TranscriptionError(YoungProductionError):
    """Raised when transcription fails."""
    def __init__(self, file_path: str, reason: str):
        super().__init__(f"Failed to transcribe {file_path}: {reason}")
        self.file_path = file_path
        self.reason = reason


# === Validation Errors ===

class ValidationError(YoungProductionError):
    """Raised when data validation fails."""
    def __init__(self, field: str, message: str):
        super().__init__(f"Validation error for '{field}': {message}")
        self.field = field


class StyleGuideNotFoundError(YoungProductionError):
    """Raised when channel writing style guide is not found."""
    def __init__(self, channel: str):
        super().__init__(f"Writing style guide not found for channel: {channel}")
        self.channel = channel

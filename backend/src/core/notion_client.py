"""
Notion API client with rate limiting and retry logic.
"""
import time
import requests
from typing import Dict, Any, Optional, List
from core.exceptions import NotionAPIError, NotionRateLimitError, PageNotFoundError


class NotionClient:
    """
    Wrapper around Notion API with built-in rate limiting and retry logic.
    Implements automatic retries with exponential backoff for rate limits.
    """

    def __init__(self, api_key: str, rate_limit_per_sec: float = 2.5):
        """
        Initialize NotionClient.

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
            method: HTTP method (GET, POST, PATCH, DELETE)
            endpoint: API endpoint (e.g., "/databases/{id}/query")
            json_data: JSON payload
            max_retries: Max retry attempts for rate limits

        Returns:
            Response JSON

        Raises:
            NotionAPIError: If request fails after retries
            NotionRateLimitError: If rate limited and retries exhausted
            PageNotFoundError: If page/database not found
        """
        url = f"{self.base_url}{endpoint}"

        for attempt in range(max_retries):
            self._rate_limit()

            try:
                response = requests.request(method, url, headers=self.headers, json=json_data)

                # Handle rate limiting
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 2 ** attempt))
                    if attempt == max_retries - 1:
                        raise NotionRateLimitError(retry_after=retry_after)
                    print(f"Rate limited. Retrying after {retry_after}s...")
                    time.sleep(retry_after)
                    continue

                # Handle 404
                if response.status_code == 404:
                    raise PageNotFoundError(
                        f"Page or database not found: {endpoint}",
                        status_code=404
                    )

                # Handle other errors
                if response.status_code >= 400:
                    error_data = response.json() if response.text else None
                    raise NotionAPIError(
                        f"Notion API error {response.status_code}: {response.text}",
                        status_code=response.status_code,
                        response_data=error_data
                    )

                return response.json()

            except requests.RequestException as e:
                if attempt == max_retries - 1:
                    raise NotionAPIError(f"Request failed after {max_retries} attempts: {str(e)}")
                time.sleep(2 ** attempt)
                continue

        raise NotionAPIError("Max retries exceeded")

    def query_database(
        self,
        database_id: str,
        filter_obj: Optional[Dict] = None,
        sorts: Optional[List[Dict]] = None,
        start_cursor: Optional[str] = None,
        page_size: int = 100
    ) -> Dict[str, Any]:
        """
        Query a database with filters and pagination.

        Args:
            database_id: Database ID
            filter_obj: Filter object (Notion API format)
            sorts: List of sort objects
            start_cursor: Pagination cursor
            page_size: Results per page (max 100)

        Returns:
            Response with 'results', 'has_more', 'next_cursor'
        """
        payload = {"page_size": page_size}
        if filter_obj:
            payload["filter"] = filter_obj
        if sorts:
            payload["sorts"] = sorts
        if start_cursor:
            payload["start_cursor"] = start_cursor

        return self._request("POST", f"/databases/{database_id}/query", json_data=payload)

    def get_database(self, database_id: str) -> Dict[str, Any]:
        """Retrieve database metadata (schema, title)."""
        return self._request("GET", f"/databases/{database_id}")

    def get_page(self, page_id: str) -> Dict[str, Any]:
        """Retrieve a page by ID."""
        return self._request("GET", f"/pages/{page_id}")

    def create_page(
        self,
        database_id: str,
        properties: Dict,
        children: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Create a new page in a database.

        Args:
            database_id: Parent database ID
            properties: Page properties (Notion API format)
            children: Optional list of block objects for page body

        Returns:
            Created page object
        """
        payload = {
            "parent": {"database_id": database_id},
            "properties": properties
        }
        if children:
            payload["children"] = children

        return self._request("POST", "/pages", json_data=payload)

    def update_page(
        self,
        page_id: str,
        properties: Optional[Dict] = None,
        archived: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Update page properties.

        Args:
            page_id: Page ID to update
            properties: Properties to update (partial update)
            archived: Set to True to archive page

        Returns:
            Updated page object
        """
        payload = {}
        if properties:
            payload["properties"] = properties
        if archived is not None:
            payload["archived"] = archived

        return self._request("PATCH", f"/pages/{page_id}", json_data=payload)

    def get_block_children(
        self,
        block_id: str,
        start_cursor: Optional[str] = None,
        page_size: int = 100
    ) -> Dict[str, Any]:
        """
        Get children blocks of a page/block.

        Args:
            block_id: Block or page ID
            start_cursor: Pagination cursor
            page_size: Results per page

        Returns:
            Response with 'results', 'has_more', 'next_cursor'
        """
        endpoint = f"/blocks/{block_id}/children"
        if start_cursor:
            endpoint += f"?start_cursor={start_cursor}&page_size={page_size}"
        else:
            endpoint += f"?page_size={page_size}"

        return self._request("GET", endpoint)

    def append_block_children(self, block_id: str, children: List[Dict]) -> Dict[str, Any]:
        """
        Append blocks to a page.

        Args:
            block_id: Parent block or page ID
            children: List of block objects to append

        Returns:
            Response with appended blocks
        """
        payload = {"children": children}
        return self._request("PATCH", f"/blocks/{block_id}/children", json_data=payload)


# Singleton instance
_client_instance: Optional[NotionClient] = None


def get_notion_client() -> NotionClient:
    """
    Get or create NotionClient singleton.

    Raises:
        ValueError: If NOTION_API_KEY not found in environment
    """
    global _client_instance
    if _client_instance is None:
        import os
        api_key = os.getenv("NOTION_API_KEY")
        if not api_key:
            raise ValueError("NOTION_API_KEY not found in environment")
        _client_instance = NotionClient(api_key)
    return _client_instance

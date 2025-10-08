import logging
from typing import Any, Dict, List, Optional
import requests
from django.conf import settings

logger = logging.getLogger("services")

class GitLabClient:
    """
    Simple GitLab API client using personal access token.

    PUBLIC_INTERFACE
    """
    # PUBLIC_INTERFACE
    def __init__(self, base_url: Optional[str] = None, token: Optional[str] = None):
        """Initialize GitLab client with base URL and personal token."""
        self.base_url = (base_url or settings.GITLAB_BASE_URL).rstrip("/")
        self.token = token or settings.GITLAB_TOKEN
        self.session = requests.Session()
        if self.token:
            self.session.headers.update({"PRIVATE-TOKEN": self.token})

    # PUBLIC_INTERFACE
    def list_commits(self, project_id: str, per_page: int = 20) -> List[Dict[str, Any]]:
        """List recent commits for a GitLab project."""
        url = f"{self.base_url}/api/v4/projects/{requests.utils.quote(project_id, safe='')}/repository/commits"
        try:
            resp = self.session.get(url, params={"per_page": per_page}, timeout=20)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as exc:
            logger.error("GitLab list_commits failed: %s", exc)
            raise

    # PUBLIC_INTERFACE
    def get_project(self, project_id: str) -> Dict[str, Any]:
        """Fetch GitLab project details."""
        url = f"{self.base_url}/api/v4/projects/{requests.utils.quote(project_id, safe='')}"
        try:
            resp = self.session.get(url, timeout=20)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as exc:
            logger.error("GitLab get_project failed: %s", exc)
            raise

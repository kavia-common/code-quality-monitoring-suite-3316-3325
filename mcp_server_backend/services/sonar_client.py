import logging
from typing import Any, Dict, Optional
import requests
from django.conf import settings

logger = logging.getLogger("services")

class SonarQubeClient:
    """
    Simple SonarQube API client using token auth.

    Note: Triggering analyses usually happens via CI (scanner).
    Here we provide a placeholder to request analysis via CE if configured.
    """

    # PUBLIC_INTERFACE
    def __init__(self, base_url: Optional[str] = None, token: Optional[str] = None):
        """Initialize SonarQube client with base URL and token."""
        self.base_url = (base_url or settings.SONARQUBE_BASE_URL).rstrip("/")
        self.token = token or settings.SONARQUBE_TOKEN
        self.session = requests.Session()
        if self.token:
            self.session.auth = (self.token, "")

    # PUBLIC_INTERFACE
    def get_measures(self, project_key: str, metric_keys: str = "code_smells,bugs,vulnerabilities,coverage,sqale_index") -> Dict[str, Any]:
        """Fetch latest measures for a project."""
        url = f"{self.base_url}/api/measures/component"
        try:
            resp = self.session.get(url, params={"component": project_key, "metricKeys": metric_keys}, timeout=20)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as exc:
            logger.error("SonarQube get_measures failed: %s", exc)
            raise

    # PUBLIC_INTERFACE
    def search_issues(self, project_key: str, p: int = 1, ps: int = 50) -> Dict[str, Any]:
        """Search issues for a project."""
        url = f"{self.base_url}/api/issues/search"
        try:
            resp = self.session.get(url, params={"componentKeys": project_key, "p": p, "ps": ps}, timeout=20)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as exc:
            logger.error("SonarQube search_issues failed: %s", exc)
            raise

    # PUBLIC_INTERFACE
    def trigger_analysis_placeholder(self, project_key: str) -> Dict[str, Any]:
        """
        Placeholder for triggering analysis.

        Many SonarQube setups require running sonar-scanner from CI.
        We record the intent and return guidance.
        """
        info = {
            "status": "queued",
            "message": "Triggering analysis typically requires sonar-scanner via CI. Ensure your pipeline runs scanner on demand.",
            "project_key": project_key,
        }
        logger.info("Trigger analysis placeholder for project_key=%s", project_key)
        return info

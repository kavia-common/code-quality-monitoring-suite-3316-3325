import logging
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Project
from .serializers import ProjectSerializer
from services.gitlab_client import GitLabClient
from services.sonar_client import SonarQubeClient
from scans.models import ScanRun
from scans.serializers import ScanRunSerializer

logger = logging.getLogger("projects")

class ProjectViewSet(viewsets.ModelViewSet):
    """
    PUBLIC_INTERFACE
    ViewSet for managing Projects and related integrations.

    Endpoints:
    - GET /api/projects
    - POST /api/projects
    - GET /api/projects/{id}
    - POST /api/projects/{id}/scan
    - GET /api/projects/{id}/quality
    - GET /api/projects/{id}/commits
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        # Allow unauthenticated access to health via api app only; all here require auth
        return super().get_permissions()

    # PUBLIC_INTERFACE
    @action(detail=True, methods=["post"], url_path="scan", permission_classes=[IsAuthenticated])
    def trigger_scan(self, request, pk=None):
        """Trigger a scan placeholder and record a ScanRun for the project."""
        project = get_object_or_404(Project, pk=pk)
        sonar = SonarQubeClient()
        try:
            info = sonar.trigger_analysis_placeholder(project.sonar_project_key)
            sr = ScanRun.objects.create(project=project, status=info.get("status", "queued"), message=info.get("message", ""))
            data = ScanRunSerializer(sr).data
            return Response({"scan": data}, status=status.HTTP_202_ACCEPTED)
        except Exception as exc:
            logger.exception("Failed to trigger scan for project %s: %s", project.id, exc)
            sr = ScanRun.objects.create(project=project, status="failed", message=str(exc))
            return Response({"detail": "Failed to trigger scan", "scan": ScanRunSerializer(sr).data}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # PUBLIC_INTERFACE
    @action(detail=True, methods=["get"], url_path="quality", permission_classes=[IsAuthenticated])
    def quality(self, request, pk=None):
        """Return SonarQube measures and a page of issues for the project."""
        project = get_object_or_404(Project, pk=pk)
        sonar = SonarQubeClient()
        try:
            measures = sonar.get_measures(project.sonar_project_key)
            issues = sonar.search_issues(project.sonar_project_key, p=int(request.GET.get("page", 1)), ps=int(request.GET.get("page_size", 50)))
            return Response({"measures": measures, "issues": issues})
        except Exception as exc:
            logger.exception("Failed fetching quality for project %s: %s", project.id, exc)
            return Response({"detail": "Failed to fetch quality"}, status=status.HTTP_502_BAD_GATEWAY)

    # PUBLIC_INTERFACE
    @action(detail=True, methods=["get"], url_path="commits", permission_classes=[IsAuthenticated])
    def commits(self, request, pk=None):
        """Return recent GitLab commits for the project."""
        project = get_object_or_404(Project, pk=pk)
        gitlab = GitLabClient()
        try:
            commits = gitlab.list_commits(project.gitlab_project_id, per_page=int(request.GET.get("per_page", 20)))
            return Response({"commits": commits})
        except Exception as exc:
            logger.exception("Failed fetching commits for project %s: %s", project.id, exc)
            return Response({"detail": "Failed to fetch commits"}, status=status.HTTP_502_BAD_GATEWAY)

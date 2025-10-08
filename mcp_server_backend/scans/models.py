from django.db import models
from projects.models import Project

class ScanRun(models.Model):
    """
    A record of a requested or executed scan run against a project.
    """
    STATUS_CHOICES = [
        ("queued", "Queued"),
        ("running", "Running"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="scan_runs")
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="queued")
    message = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.project.name} - {self.status} @ {self.created_at}"

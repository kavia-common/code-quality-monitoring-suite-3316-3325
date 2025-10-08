from django.db import models

class Project(models.Model):
    """
    Represents a code project tracked through GitLab and SonarQube.
    """
    name = models.CharField(max_length=255)
    gitlab_project_id = models.CharField(max_length=128, help_text="GitLab project ID or path-with-namespace")
    sonar_project_key = models.CharField(max_length=255, help_text="SonarQube project key")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.name} ({self.gitlab_project_id})"

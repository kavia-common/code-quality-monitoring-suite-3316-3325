from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "gitlab_project_id", "sonar_project_key", "created_at")
    search_fields = ("name", "gitlab_project_id", "sonar_project_key")

from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for Project model.
    """
    class Meta:
        model = Project
        fields = ["id", "name", "gitlab_project_id", "sonar_project_key", "created_at"]
        read_only_fields = ["id", "created_at"]

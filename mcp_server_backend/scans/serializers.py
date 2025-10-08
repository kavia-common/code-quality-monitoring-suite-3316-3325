from rest_framework import serializers
from .models import ScanRun

class ScanRunSerializer(serializers.ModelSerializer):
    """
    Serializer for ScanRun.
    """
    class Meta:
        model = ScanRun
        fields = ["id", "project", "status", "message", "created_at"]
        read_only_fields = ["id", "created_at"]

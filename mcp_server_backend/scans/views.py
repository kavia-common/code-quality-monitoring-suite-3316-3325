from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import ScanRun
from .serializers import ScanRunSerializer

class ScanRunViewSet(viewsets.ReadOnlyModelViewSet):
    """
    PUBLIC_INTERFACE
    Read-only access to scan runs.
    """
    queryset = ScanRun.objects.select_related("project").all()
    serializer_class = ScanRunSerializer
    permission_classes = [IsAuthenticated]

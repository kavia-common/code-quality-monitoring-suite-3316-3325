from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScanRunViewSet

router = DefaultRouter()
router.register(r"scans", ScanRunViewSet, basename="scans")

urlpatterns = [
    path("", include(router.urls)),
]

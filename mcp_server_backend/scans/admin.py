from django.contrib import admin
from .models import ScanRun

@admin.register(ScanRun)
class ScanRunAdmin(admin.ModelAdmin):
    list_display = ("id", "project", "status", "created_at")
    list_filter = ("status",)

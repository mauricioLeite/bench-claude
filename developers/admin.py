from django.contrib import admin
from .models import Developer


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'team', 'job_title', 'availability', 'created_at']
    list_filter = ['availability', 'team']
    search_fields = ['name', 'email', 'team', 'job_title']
    ordering = ['name']

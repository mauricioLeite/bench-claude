from django.contrib import admin
from .models import ConnectionRequest, Endorsement


@admin.register(ConnectionRequest)
class ConnectionRequestAdmin(admin.ModelAdmin):
    list_display = ['requester_name', 'requester_email', 'receiver', 'skill', 'urgency', 'status', 'created_at']
    list_filter = ['status', 'urgency']
    search_fields = ['requester_name', 'requester_email', 'receiver__name']
    ordering = ['-created_at']
    list_editable = ['status']


@admin.register(Endorsement)
class EndorsementAdmin(admin.ModelAdmin):
    list_display = ['from_name', 'to_developer', 'skill', 'created_at']
    search_fields = ['from_name', 'to_developer__name', 'skill__name']
    ordering = ['-created_at']

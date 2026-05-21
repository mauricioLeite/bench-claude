from django.contrib import admin
from .models import Skill, DeveloperSkill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'type', 'created_at']
    list_filter = ['category', 'type']
    search_fields = ['name']
    ordering = ['name']


@admin.register(DeveloperSkill)
class DeveloperSkillAdmin(admin.ModelAdmin):
    list_display = ['developer', 'skill', 'level', 'is_learning', 'is_available_to_help']
    list_filter = ['level', 'is_learning', 'is_available_to_help', 'skill__category']
    search_fields = ['developer__name', 'skill__name']
    ordering = ['developer__name', '-level']

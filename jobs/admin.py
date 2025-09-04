from django.contrib import admin
from .models import Job, Application, Bookmark


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'location', 'status', 'posted_by', 'created_at')
    list_filter = ('status', 'location', 'company_name', 'created_at')
    search_fields = ('title', 'company_name', 'location', 'skills')
    actions = ['mark_approved', 'mark_rejected']

    def mark_approved(self, request, queryset):
        queryset.update(status='approved')
    mark_approved.short_description = 'Approve selected jobs'

    def mark_rejected(self, request, queryset):
        queryset.update(status='rejected')
    mark_rejected.short_description = 'Reject selected jobs'


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('job__title', 'applicant__username')


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'created_at')
    search_fields = ('user__username', 'job__title', 'job__company_name')

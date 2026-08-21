from django.contrib import admin

from .models import AccessLog


@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user_display', 'method', 'path', 'status_code', 'ip_address')
    list_filter = ('created_at', 'method', 'status_code', 'user')
    search_fields = ('path', 'ip_address', 'user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('method', 'path', 'status_code', 'user', 'ip_address', 'user_agent', 'referer', 'created_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    @admin.display(description='usuario')
    def user_display(self, obj):
        return obj.user or 'Anonimo'

# Register your models here.

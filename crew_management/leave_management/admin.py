from django.contrib import admin
from .models import LeaveType, LeaveRequest

@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'days_allowed')
    search_fields = ('name',)

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'leave_type', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'leave_type')
    search_fields = ('user__username', 'user__email', 'reason')
    date_hierarchy = 'start_date'
    
    fieldsets = (
        (None, {
            'fields': ('user', 'leave_type')
        }),
        ('Date Information', {
            'fields': ('start_date', 'end_date')
        }),
        ('Request Details', {
            'fields': ('reason', 'status')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ('user', 'leave_type', 'start_date', 'end_date', 'reason')
        return ()

    def has_delete_permission(self, request, obj=None):
        return False
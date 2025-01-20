from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ServiceRequest, ServiceFeedback
from django import forms
from django.utils import timezone

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'date_joined', 'last_login', 'is_active')
    search_fields = ('username', 'email', 'phone')
    ordering = ('-date_joined',)
    list_filter = ('is_active', 'date_joined')

class ServiceRequestAdminForm(forms.ModelForm):
    status_note = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False,
                                help_text="Add a note about this status change")
    scheduled_date = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    
    class Meta:
        model = ServiceRequest
        fields = '__all__'

class ServiceRequestAdmin(admin.ModelAdmin):
    form = ServiceRequestAdminForm
    list_display = ('id', 'user', 'request_type', 'status', 'assigned_team', 'scheduled_date', 'created_at', 'updated_at')
    list_filter = ('status', 'request_type', 'created_at', 'assigned_team')
    search_fields = ('user__username', 'description', 'id', 'status_notes')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'request_type', 'description', 'attachment')
        }),
        ('Status Information', {
            'fields': ('status', 'status_note', 'assigned_team', 'scheduled_date')
        }),
        ('History', {
            'fields': ('status_notes', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if change and ('status' in form.changed_data or 'assigned_team' in form.changed_data):
            status_note = form.cleaned_data.get('status_note')
            if status_note:
                obj.update_status(
                    obj.status,
                    notes=status_note,
                    team=obj.assigned_team,
                    scheduled_date=form.cleaned_data.get('scheduled_date')
                )
        super().save_model(request, obj, form, change)

class ServiceFeedbackAdmin(admin.ModelAdmin):
    list_display = ('service_request', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('service_request__user__username', 'comment')
    readonly_fields = ('created_at',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(ServiceRequest, ServiceRequestAdmin)
admin.site.register(ServiceFeedback, ServiceFeedbackAdmin)

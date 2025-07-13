from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, TraderProfile, CustomerProfile, ViolationLog


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'is_approved', 'is_active', 'date_joined')
    list_filter = ('role', 'is_approved', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role & Approval', {
            'fields': ('role', 'is_approved')
        }),
        ('Additional Info', {
            'fields': ('phone_number', 'date_of_birth', 'address')
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Role & Additional Info', {
            'fields': ('role', 'phone_number', 'date_of_birth', 'address')
        }),
    )


@admin.register(TraderProfile)
class TraderProfileAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'business_email', 'violation_count', 'is_suspended')
    list_filter = ('is_suspended', 'created_at')
    search_fields = ('business_name', 'user__username', 'business_email')
    readonly_fields = ('violation_count', 'created_at')

    fieldsets = (
        ('Business Information', {
            'fields': ('user', 'business_name', 'business_license', 'tax_id')
        }),
        ('Contact Information', {
            'fields': ('business_address', 'business_phone', 'business_email')
        }),
        ('Banking Information', {
            'fields': ('bank_account_number', 'bank_name')
        }),
        ('Status & Violations', {
            'fields': ('violation_count', 'is_suspended', 'suspension_reason')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'reward_points', 'total_orders', 'total_spent')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('total_orders', 'total_spent', 'created_at')


@admin.register(ViolationLog)
class ViolationLogAdmin(admin.ModelAdmin):
    list_display = ('trader', 'violation_type', 'is_resolved', 'created_at')
    list_filter = ('violation_type', 'is_resolved', 'created_at')
    search_fields = ('trader__username', 'description')
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Violation Details', {
            'fields': ('trader', 'violation_type', 'description', 'reported_by')
        }),
        ('Resolution', {
            'fields': ('action_taken', 'is_resolved', 'resolved_at')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )

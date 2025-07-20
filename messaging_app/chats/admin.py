from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Conversation, Message


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin configuration for User model.
    """
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'created_at']
    list_filter = ['role', 'is_active', 'is_staff', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('phone_number', 'role', 'created_at')
        }),
    )
    readonly_fields = ['user_id', 'created_at']


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """
    Admin configuration for Conversation model.
    """
    list_display = ['conversation_id', 'get_participants', 'created_at']
    list_filter = ['created_at']
    search_fields = ['participants__username', 'participants__email']
    readonly_fields = ['conversation_id', 'created_at']
    filter_horizontal = ['participants']

    def get_participants(self, obj):
        """
        Return a comma-separated list of participants.
        """
        return ", ".join([user.username for user in obj.participants.all()])
    get_participants.short_description = 'Participants'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Admin configuration for Message model.
    """
    list_display = ['message_id', 'sender', 'conversation', 'message_body_preview', 'sent_at']
    list_filter = ['sent_at']
    search_fields = ['sender__username', 'message_body']
    readonly_fields = ['message_id', 'sent_at']
    raw_id_fields = ['sender', 'conversation']

    def message_body_preview(self, obj):
        """
        Return a truncated version of the message body.
        """
        return obj.message_body[:50] + '...' if len(obj.message_body) > 50 else obj.message_body
    message_body_preview.short_description = 'Message Preview'

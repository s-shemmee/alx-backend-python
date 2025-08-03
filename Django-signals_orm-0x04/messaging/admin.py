from django.contrib import admin
from .models import Message, Notification, MessageHistory


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'timestamp', 'edited', 'read')
    list_filter = ('timestamp', 'edited', 'read')
    search_fields = ('sender__username', 'receiver__username', 'content')
    ordering = ('-timestamp',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'timestamp', 'read')
    list_filter = ('timestamp', 'read')
    search_fields = ('user__username', 'content')
    ordering = ('-timestamp',)


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ('message', 'old_content', 'edited_at')
    list_filter = ('edited_at',)
    search_fields = ('message__content', 'old_content')
    ordering = ('-edited_at',)

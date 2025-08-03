from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Conversation(models.Model):
    """Model for threaded conversations - Task 3"""
    participants = models.ManyToManyField(User, related_name='conversations')
    title = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Conversation: {self.title or f'ID {self.id}'}"


class ChatMessage(models.Model):
    """Enhanced message model for threaded conversations - Task 3"""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    edited = models.BooleanField(default=False)
    read_by = models.ManyToManyField(User, blank=True, related_name='read_chat_messages')
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}..."
    
    def get_thread_messages(self):
        """Get all messages in the thread using advanced ORM - Task 3"""
        return ChatMessage.objects.filter(
            conversation=self.conversation,
            parent_message=self.parent_message or self
        ).select_related('sender').prefetch_related('replies', 'read_by')

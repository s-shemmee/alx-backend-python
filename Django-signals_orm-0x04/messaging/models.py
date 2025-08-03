from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UnreadMessagesManager(models.Manager):
    """Custom manager for filtering unread messages - Task 4"""
    def unread_for_user(self, user):
        return self.filter(receiver=user, read=False).only('id', 'sender', 'content', 'timestamp')


class Message(models.Model):
    """Message model for the messaging system"""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    edited = models.BooleanField(default=False)  # Task 1
    read = models.BooleanField(default=False)  # Task 4
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')  # Task 3
    
    # Custom managers
    objects = models.Manager()  # Default manager
    unread_objects = UnreadMessagesManager()  # Custom manager for unread messages
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}: {self.content[:50]}..."


class Notification(models.Model):
    """Notification model to store user notifications"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='notifications')
    content = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Notification for {self.user.username}: {self.content}"


class MessageHistory(models.Model):
    """Model to store message edit history - Task 1"""
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-edited_at']
    
    def __str__(self):
        return f"History for message {self.message.id} at {self.edited_at}"

from django.db import models


class UnreadMessagesManager(models.Manager):
    """Custom manager for filtering unread messages - Task 4"""
    def unread_for_user(self, user):
        return self.filter(receiver=user, read=False).only('id', 'sender', 'content', 'timestamp')

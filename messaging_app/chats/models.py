from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator
import uuid


class User(AbstractUser):
    """
    Extended User model with additional fields for the messaging app.
    """
    user_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False,
        db_index=True
    )
    first_name = models.CharField(max_length=150, null=False, blank=False)
    last_name = models.CharField(max_length=150, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    password = models.CharField(
        max_length=128,
        validators=[MinLengthValidator(8)],
        help_text="Password must be at least 8 characters long"
    )
    
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default='guest',
        null=False,
        blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'auth_user'
        indexes = [
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return self.username


class Conversation(models.Model):
    """
    Model representing a conversation between users.
    """
    conversation_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False,
        db_index=True
    )
    participants = models.ManyToManyField(
        User, 
        related_name='conversations',
        blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Conversation {self.conversation_id}"


class Message(models.Model):
    """
    Model representing a message in a conversation.
    """
    message_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False,
        db_index=True
    )
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='sent_messages'
    )
    conversation = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name='messages'
    )
    message_body = models.TextField(null=False, blank=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sent_at']
        indexes = [
            models.Index(fields=['sender']),
            models.Index(fields=['conversation']),
            models.Index(fields=['sent_at']),
        ]

    def __str__(self):
        return f"Message {self.message_id} from {self.sender}"

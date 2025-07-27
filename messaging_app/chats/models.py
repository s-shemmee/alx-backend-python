from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import MinLengthValidator
import uuid


class UserManager(BaseUserManager):
    """
    Custom user manager for User model with UUID primary key.
    """
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(username, email, password, **extra_fields)


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
        ('member', 'Member'),
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

    objects = UserManager()

    class Meta:
        db_table = 'auth_user'
        indexes = [
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return self.username
    
    @property
    def id(self):
        """JWT compatibility - map user_id to id"""
        return self.user_id


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

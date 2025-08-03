from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification_for_new_message(sender, instance, created, **kwargs):
    """
    Task 0: Signal to create notification when a new message is created
    """
    if created:
        # Create notification for the receiver
        notification_content = f"You have a new message from {instance.sender.username}"
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            content=notification_content
        )


@receiver(pre_save, sender=Message)
def log_message_edit_history(sender, instance, **kwargs):
    """
    Task 1: Signal to log old content before message is updated
    """
    if instance.pk:  # Only for existing messages (updates)
        try:
            old_message = Message.objects.get(pk=instance.pk)
            # Check if content has changed
            if old_message.content != instance.content:
                # Log the old content before it's updated
                MessageHistory.objects.create(
                    message=old_message,
                    old_content=old_message.content
                )
                # Mark message as edited
                instance.edited = True
        except Message.DoesNotExist:
            pass


@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    """
    Task 2: Signal to clean up related data when a user is deleted
    """
    # Delete all messages where user is sender or receiver
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    
    # Delete all notifications for the user
    Notification.objects.filter(user=instance).delete()
    
    # MessageHistory objects will be cascade deleted when messages are deleted
    # due to foreign key relationship

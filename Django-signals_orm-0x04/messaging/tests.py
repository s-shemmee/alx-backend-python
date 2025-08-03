from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save, post_delete
from .models import Message, Notification, MessageHistory
from .signals import create_notification_for_new_message, log_message_edit_history, cleanup_user_related_data


class SignalTestCase(TestCase):
    """Test cases for Django signals"""
    
    def setUp(self):
        """Set up test data"""
        self.user1 = User.objects.create_user(username='testuser1', email='test1@example.com')
        self.user2 = User.objects.create_user(username='testuser2', email='test2@example.com')
    
    def test_notification_created_on_new_message(self):
        """Test that notification is created when a new message is sent (Task 0)"""
        initial_notification_count = Notification.objects.count()
        
        # Create a new message
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Hello, this is a test message"
        )
        
        # Check that notification was created
        self.assertEqual(Notification.objects.count(), initial_notification_count + 1)
        
        # Check notification details
        notification = Notification.objects.get(message=message)
        self.assertEqual(notification.user, self.user2)
        self.assertEqual(notification.message, message)
        self.assertIn(self.user1.username, notification.content)
    
    def test_message_history_created_on_edit(self):
        """Test that message history is created when message is edited (Task 1)"""
        # Create initial message
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Original content"
        )
        
        initial_history_count = MessageHistory.objects.count()
        
        # Edit the message
        message.content = "Updated content"
        message.save()
        
        # Check that history was created
        self.assertEqual(MessageHistory.objects.count(), initial_history_count + 1)
        
        # Check history details
        history = MessageHistory.objects.get(message=message)
        self.assertEqual(history.old_content, "Original content")
        
        # Check that message is marked as edited
        message.refresh_from_db()
        self.assertTrue(message.edited)
    
    def test_user_deletion_cleanup(self):
        """Test that related data is cleaned up when user is deleted (Task 2)"""
        # Create test data
        message1 = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Message from user1 to user2"
        )
        
        message2 = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content="Message from user2 to user1"
        )
        
        # Notifications should be created automatically via signals
        notification_count = Notification.objects.filter(user=self.user1).count()
        
        # Delete user1
        self.user1.delete()
        
        # Check that messages and notifications are cleaned up
        self.assertFalse(Message.objects.filter(sender__username='testuser1').exists())
        self.assertFalse(Message.objects.filter(receiver__username='testuser1').exists())
        self.assertFalse(Notification.objects.filter(user__username='testuser1').exists())


class OrmTestCase(TestCase):
    """Test cases for ORM techniques"""
    
    def setUp(self):
        """Set up test data"""
        self.user1 = User.objects.create_user(username='user1', email='user1@example.com')
        self.user2 = User.objects.create_user(username='user2', email='user2@example.com')
    
    def test_threaded_messages(self):
        """Test threaded conversation functionality (Task 3)"""
        # Create root message
        root_message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Root message"
        )
        
        # Create reply to root message
        reply1 = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content="Reply 1 to root",
            parent_message=root_message
        )
        
        # Create reply to reply1
        reply2 = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Reply to reply 1",
            parent_message=reply1
        )
        
        # Test that relationships are correctly established
        self.assertEqual(root_message.replies.count(), 1)
        self.assertEqual(reply1.parent_message, root_message)
        self.assertEqual(reply2.parent_message, reply1)
        self.assertEqual(reply1.replies.count(), 1)
    
    def test_unread_messages_manager(self):
        """Test custom manager for unread messages (Task 4)"""
        # Create read and unread messages
        read_message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Read message",
            read=True
        )
        
        unread_message1 = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Unread message 1",
            read=False
        )
        
        unread_message2 = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Unread message 2",
            read=False
        )
        
        # Test custom manager
        unread_messages = Message.unread.unread_for_user(self.user2)
        self.assertEqual(unread_messages.count(), 2)
        
        # Test that only unread messages are returned
        unread_ids = list(unread_messages.values_list('id', flat=True))
        self.assertIn(unread_message1.id, unread_ids)
        self.assertIn(unread_message2.id, unread_ids)
        self.assertNotIn(read_message.id, unread_ids)

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Conversation, Message

User = get_user_model()


class UserModelTest(TestCase):
    """Test User model functionality."""

    def setUp(self):
        """Set up test data."""
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '+1234567890',
            'role': 'guest'
        }

    def test_create_user(self):
        """Test user creation."""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.role, 'guest')
        self.assertTrue(user.check_password('testpassword123'))

    def test_user_str_representation(self):
        """Test user string representation."""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), 'testuser')


class ConversationModelTest(TestCase):
    """Test Conversation model functionality."""

    def setUp(self):
        """Set up test data."""
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='password123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='password123'
        )

    def test_create_conversation(self):
        """Test conversation creation."""
        conversation = Conversation.objects.create()
        conversation.participants.add(self.user1, self.user2)
        
        self.assertEqual(conversation.participants.count(), 2)
        self.assertIn(self.user1, conversation.participants.all())
        self.assertIn(self.user2, conversation.participants.all())

    def test_conversation_str_representation(self):
        """Test conversation string representation."""
        conversation = Conversation.objects.create()
        conversation.participants.add(self.user1, self.user2)
        expected_str = f"Conversation {conversation.conversation_id}"
        self.assertEqual(str(conversation), expected_str)


class MessageModelTest(TestCase):
    """Test Message model functionality."""

    def setUp(self):
        """Set up test data."""
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='password123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='password123'
        )
        self.conversation = Conversation.objects.create()
        self.conversation.participants.add(self.user1, self.user2)

    def test_create_message(self):
        """Test message creation."""
        message = Message.objects.create(
            sender=self.user1,
            conversation=self.conversation,
            message_body="Hello, how are you?"
        )
        
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.conversation, self.conversation)
        self.assertEqual(message.message_body, "Hello, how are you?")

    def test_message_str_representation(self):
        """Test message string representation."""
        message = Message.objects.create(
            sender=self.user1,
            conversation=self.conversation,
            message_body="Hello, how are you?"
        )
        expected_str = f"Message {message.message_id} from {self.user1}"
        self.assertEqual(str(message), expected_str)


class APIEndpointsTest(APITestCase):
    """Test API endpoints functionality."""

    def setUp(self):
        """Set up test data."""
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='password123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='password123'
        )

    def test_api_root_accessible(self):
        """Test that API root is accessible."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_endpoint_accessible(self):
        """Test that users endpoint is accessible."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_conversations_endpoint_accessible(self):
        """Test that conversations endpoint is accessible."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/conversations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_messages_endpoint_accessible(self):
        """Test that messages endpoint is accessible."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/messages/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_conversation_via_api(self):
        """Test creating a conversation via API."""
        self.client.force_authenticate(user=self.user1)
        data = {
            'participant_ids': [str(self.user1.user_id), str(self.user2.user_id)]
        }
        response = self.client.post('/api/conversations/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Conversation.objects.count(), 1)

    def test_create_message_via_api(self):
        """Test creating a message via API."""
        # First create a conversation
        conversation = Conversation.objects.create()
        conversation.participants.add(self.user1, self.user2)
        
        self.client.force_authenticate(user=self.user1)
        data = {
            'conversation': str(conversation.conversation_id),
            'message_body': 'Hello from API test!'
        }
        response = self.client.post('/api/messages/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 1)
        
        # Verify the message was created correctly
        message = Message.objects.first()
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.message_body, 'Hello from API test!')

    def test_unauthorized_access_blocked(self):
        """Test that unauthorized access is blocked."""
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

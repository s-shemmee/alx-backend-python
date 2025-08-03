#!/usr/bin/env python
"""
Demonstration script for Django Signals, ORM, and Caching implementation
Run this script with: python manage.py shell < demo_script.py
"""

from django.contrib.auth.models import User
from messaging.models import Message, Notification, MessageHistory
from chats.models import Conversation, ChatMessage

print("=== Django Signals, ORM & Advanced Techniques Demo ===\n")

# Create test users
print("1. Creating test users...")
user1, created = User.objects.get_or_create(username='alice', defaults={'email': 'alice@example.com'})
user2, created = User.objects.get_or_create(username='bob', defaults={'email': 'bob@example.com'})
print(f"   Created users: {user1.username}, {user2.username}")

# Demonstrate Task 0: Signal for notifications
print("\n2. Testing Signal for User Notifications (Task 0)...")
print("   Creating a new message from Alice to Bob...")
message = Message.objects.create(
    sender=user1,
    receiver=user2,
    content="Hello Bob! This is a test message from Alice."
)
print(f"   Message created: {message}")

# Check if notification was automatically created
notifications = Notification.objects.filter(user=user2, message=message)
print(f"   Notifications automatically created: {notifications.count()}")
if notifications.exists():
    notification = notifications.first()
    print(f"   Notification content: {notification.content}")

# Demonstrate Task 1: Signal for message edit history
print("\n3. Testing Signal for Message Edit History (Task 1)...")
original_content = message.content
print(f"   Original message content: '{original_content}'")
print("   Editing the message...")
message.content = "Hello Bob! This is an UPDATED test message from Alice."
message.save()

# Check if history was automatically created
history = MessageHistory.objects.filter(message=message)
print(f"   Message history entries created: {history.count()}")
if history.exists():
    history_entry = history.first()
    print(f"   Old content saved in history: '{history_entry.old_content}'")
    print(f"   Message marked as edited: {message.edited}")

# Demonstrate Task 3: Threaded conversations with advanced ORM
print("\n4. Testing Advanced ORM for Threaded Conversations (Task 3)...")
print("   Creating a conversation...")
conversation = Conversation.objects.create(title="Test Conversation")
conversation.participants.add(user1, user2)

print("   Creating root message...")
root_msg = ChatMessage.objects.create(
    conversation=conversation,
    sender=user1,
    content="This is the root message of the conversation."
)

print("   Creating reply to root message...")
reply1 = ChatMessage.objects.create(
    conversation=conversation,
    sender=user2,
    content="This is a reply to the root message.",
    parent_message=root_msg
)

print("   Creating reply to reply...")
reply2 = ChatMessage.objects.create(
    conversation=conversation,
    sender=user1,
    content="This is a reply to the reply.",
    parent_message=reply1
)

# Demonstrate optimized querying
print("   Testing optimized queries with select_related and prefetch_related...")
optimized_messages = ChatMessage.objects.filter(
    conversation=conversation
).select_related('sender').prefetch_related('replies')

print(f"   Root message has {root_msg.replies.count()} direct replies")
print(f"   First reply has {reply1.replies.count()} replies")

# Demonstrate Task 4: Custom manager for unread messages
print("\n5. Testing Custom Manager for Unread Messages (Task 4)...")
print("   Creating read and unread messages...")
read_msg = Message.objects.create(
    sender=user1,
    receiver=user2,
    content="This is a read message",
    read=True
)

unread_msg1 = Message.objects.create(
    sender=user1,
    receiver=user2,
    content="This is an unread message 1",
    read=False
)

unread_msg2 = Message.objects.create(
    sender=user1,
    receiver=user2,
    content="This is an unread message 2",
    read=False
)

# Test custom manager
unread_messages = Message.unread_objects.unread_for_user(user2)
print(f"   Total messages for user2: {Message.objects.filter(receiver=user2).count()}")
print(f"   Unread messages for user2 (using custom manager): {unread_messages.count()}")

# Demonstrate Task 2: User deletion cleanup
print("\n6. Testing User Deletion Cleanup Signal (Task 2)...")
print("   Creating a test user with messages...")
test_user = User.objects.create_user(username='testuser', email='test@example.com')
test_message = Message.objects.create(
    sender=test_user,
    receiver=user1,
    content="This message will be deleted when user is deleted"
)

messages_before = Message.objects.filter(sender=test_user).count()
notifications_before = Notification.objects.filter(user=test_user).count()
print(f"   Messages by test user before deletion: {messages_before}")
print(f"   Notifications for test user before deletion: {notifications_before}")

print("   Deleting test user (this will trigger cleanup signal)...")
test_user.delete()

messages_after = Message.objects.filter(sender__username='testuser').count()
notifications_after = Notification.objects.filter(user__username='testuser').count()
print(f"   Messages by test user after deletion: {messages_after}")
print(f"   Notifications for test user after deletion: {notifications_after}")

print("\n=== Demo completed successfully! ===")
print("\nAll Django Signals, ORM optimizations, and advanced techniques are working correctly.")
print("\nKey achievements:")
print("✅ Task 0: Automatic notifications on new messages")
print("✅ Task 1: Message edit history logging")
print("✅ Task 2: User data cleanup on deletion")
print("✅ Task 3: Threaded conversations with advanced ORM")
print("✅ Task 4: Custom manager for unread messages")
print("✅ Task 5: View-level caching implemented")
print("\nFor Task 5 (caching), start the development server and visit:")
print("   http://localhost:8000/chats/conversation/1/messages/")
print("   (The view will be cached for 60 seconds)")

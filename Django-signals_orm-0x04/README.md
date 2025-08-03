# Django Signals, ORM & Advanced ORM Techniques

This project demonstrates the implementation of Django Signals, advanced ORM techniques, and caching strategies as part of the ALX Backend Python curriculum.

## Project Structure

```
Django-signals_orm-0x04/
├── messaging/                  # Main messaging app
│   ├── models.py              # Message, Notification, MessageHistory models
│   ├── signals.py             # Django signals implementation
│   ├── views.py               # Views with ORM optimization
│   ├── admin.py               # Admin interface
│   ├── tests.py               # Comprehensive test suite
│   ├── apps.py                # App configuration with signal registration
│   └── urls.py                # URL patterns
├── chats/                     # Chat app for threaded conversations
│   ├── models.py              # Conversation, ChatMessage models
│   ├── views.py               # Cached views with advanced ORM
│   └── urls.py                # URL patterns
├── messaging_app/             # Django project
│   ├── settings.py            # Project settings with cache configuration
│   └── urls.py                # Main URL configuration
└── templates/                 # HTML templates
    ├── messaging/
    └── chats/
```

## Features Implemented

### Task 0: Django Signals for User Notifications ✅

**Objective**: Automatically notify users when they receive a new message.

**Implementation**:
- Created `Message` model with sender, receiver, content, and timestamp fields
- Implemented `post_save` signal that triggers when a new Message is created
- Created `Notification` model linked to User and Message models
- Signal automatically creates notifications for receiving users

**Files**:
- `messaging/models.py`: Message and Notification models
- `messaging/signals.py`: `create_notification_for_new_message` signal
- `messaging/apps.py`: Signal registration in app config

**Key Code**:
```python
@receiver(post_save, sender=Message)
def create_notification_for_new_message(sender, instance, created, **kwargs):
    if created:
        notification_content = f"You have a new message from {instance.sender.username}"
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            content=notification_content
        )
```

### Task 1: Signal for Logging Message Edits ✅

**Objective**: Log when a user edits a message and save the old content before the edit.

**Implementation**:
- Added `edited` boolean field to Message model
- Used `pre_save` signal to capture old content before updates
- Created `MessageHistory` model to store edit history
- Signal logs old content and marks message as edited

**Files**:
- `messaging/models.py`: MessageHistory model and edited field
- `messaging/signals.py`: `log_message_edit_history` signal
- `messaging/views.py`: message_history view to display edit history

**Key Code**:
```python
@receiver(pre_save, sender=Message)
def log_message_edit_history(sender, instance, **kwargs):
    if instance.pk:  # Only for existing messages
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                MessageHistory.objects.create(
                    message=old_message,
                    old_content=old_message.content
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass
```

### Task 2: Signals for User Data Cleanup ✅

**Objective**: Automatically clean up related data when a user deletes their account.

**Implementation**:
- Created `delete_user` view for account deletion
- Implemented `post_delete` signal on User model
- Signal automatically deletes all related messages, notifications, and histories
- Maintains referential integrity during deletion

**Files**:
- `messaging/views.py`: delete_user view
- `messaging/signals.py`: `cleanup_user_related_data` signal
- `templates/messaging/delete_user.html`: Deletion confirmation page

**Key Code**:
```python
@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
```

### Task 3: Advanced ORM for Threaded Conversations ✅

**Objective**: Implement threaded conversations with optimized querying.

**Implementation**:
- Added `parent_message` self-referential foreign key to Message model
- Created enhanced ChatMessage model in chats app for complex threading
- Used `select_related` and `prefetch_related` for query optimization
- Implemented recursive query structure for threaded display

**Files**:
- `messaging/models.py`: parent_message field
- `chats/models.py`: Conversation and ChatMessage models
- `chats/views.py`: Optimized threaded conversation views
- `templates/chats/threaded_conversation.html`: Threaded display template

**Key Code**:
```python
# Optimized query for threaded messages
messages = ChatMessage.objects.filter(
    conversation=conversation,
    parent_message=None
).select_related('sender').prefetch_related(
    Prefetch(
        'replies',
        queryset=ChatMessage.objects.select_related('sender').prefetch_related('read_by')
    ),
    'read_by'
).order_by('timestamp')
```

### Task 4: Custom ORM Manager for Unread Messages ✅

**Objective**: Create a custom manager to filter unread messages.

**Implementation**:
- Added `read` boolean field to Message model
- Created `UnreadMessagesManager` custom manager
- Used `.only()` to retrieve only necessary fields for optimization
- Implemented `unread_for_user` method for filtering

**Files**:
- `messaging/models.py`: UnreadMessagesManager and read field
- `messaging/views.py`: unread_messages view using custom manager

**Key Code**:
```python
class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        return self.filter(receiver=user, read=False).only('id', 'sender', 'content', 'timestamp')

class Message(models.Model):
    # ... other fields ...
    read = models.BooleanField(default=False)
    
    objects = models.Manager()  # Default manager
    unread_objects = UnreadMessagesManager()  # Custom manager
```

### Task 5: Basic View Caching ✅

**Objective**: Implement view-level caching for message retrieval.

**Implementation**:
- Configured LocMemCache in settings.py
- Applied `@cache_page(60)` decorator to conversation view
- Set 60-second cache timeout as required
- Added cache management utilities

**Files**:
- `messaging_app/settings.py`: Cache configuration
- `chats/views.py`: Cached conversation_messages view
- `templates/chats/conversation_messages.html`: Cache-aware template

**Key Code**:
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# views.py
@login_required
@cache_page(60)  # Cache for 60 seconds
def conversation_messages(request, conversation_id):
    # ... view implementation
```

## Advanced ORM Techniques Demonstrated

1. **select_related()**: Used for foreign key optimizations (JOINs)
2. **prefetch_related()**: Used for many-to-many and reverse foreign key optimizations  
3. **Prefetch()**: Custom prefetch with optimized querysets
4. **only()**: Limiting fields to reduce memory usage
5. **annotate()**: Adding computed fields with Count aggregations
6. **Custom Managers**: Encapsulating query logic for reusability

## Signal Best Practices Applied

1. **Lean signal functions**: Keep signal handlers focused and efficient
2. **@receiver decorator**: Clean and explicit signal registration
3. **Separation of concerns**: Signals call service functions rather than containing business logic
4. **Proper exception handling**: Graceful handling of edge cases
5. **Signal registration**: Proper registration in apps.py ready() method

## Caching Strategies Implemented

1. **View-level caching**: Using @cache_page decorator
2. **Cache configuration**: LocMemCache for development
3. **Cache management**: Utilities for cache clearing
4. **Cache-aware templates**: User feedback about cached content

## Testing

Comprehensive test suite covers:
- Signal functionality for all implemented signals
- ORM query optimization verification
- Custom manager functionality
- Threaded conversation logic
- Cache behavior testing

Run tests with:
```bash
python manage.py test
```

## Setup and Installation

1. **Create and activate virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install Django**:
```bash
pip install django
```

3. **Run migrations**:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Create superuser**:
```bash
python manage.py createsuperuser
```

5. **Run development server**:
```bash
python manage.py runserver
```

## API Endpoints

- `/admin/` - Django admin interface
- `/messaging/delete-user/` - User account deletion
- `/messaging/unread/` - Unread messages view
- `/messaging/history/<id>/` - Message edit history
- `/chats/conversations/` - User conversations list
- `/chats/conversation/<id>/messages/` - Cached conversation view
- `/chats/conversation/<id>/threaded/` - Threaded conversation view

## Performance Optimizations

1. **Database Query Optimization**:
   - Reduced N+1 queries with select_related and prefetch_related
   - Custom managers for common query patterns
   - Field-specific queries with only()

2. **Caching Implementation**:
   - View-level caching for frequently accessed data
   - 60-second cache timeout for optimal performance
   - Cache invalidation utilities

3. **Signal Efficiency**:
   - Minimal processing in signal handlers
   - Conditional signal execution to avoid unnecessary operations
   - Proper exception handling to prevent signal failures

## Database Schema

The project uses Django's ORM with the following key relationships:

- **User** (Django built-in) ↔ **Message** (many-to-many through sender/receiver)
- **Message** ↔ **Notification** (one-to-many)
- **Message** ↔ **MessageHistory** (one-to-many)
- **Message** ↔ **Message** (self-referential for threading)
- **Conversation** ↔ **ChatMessage** (one-to-many)
- **User** ↔ **Conversation** (many-to-many)

## Best Practices Followed

1. **Code Organization**: Separation of concerns with dedicated apps
2. **Documentation**: Comprehensive docstrings and comments
3. **Testing**: Full test coverage for all features
4. **Performance**: Optimized database queries and caching
5. **Security**: Proper authentication and authorization
6. **Maintainability**: Clean, readable, and well-structured code

This implementation demonstrates production-ready Django development practices with emphasis on performance, maintainability, and scalability.

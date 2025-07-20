# Django Messaging App - Building Robust APIs

This is a complete Django REST API messaging application built as part of the **Building Robust APIs** project.

## 🚀 Project Overview

A fully functional messaging system with user management, conversations, and real-time messaging capabilities.

## 📋 Tasks Completed

### ✅ Task 1: Project Setup and Configuration
- Created Django project `messaging_app`
- Configured Django settings with REST framework
- Set up custom user model
- Configured database with SQLite

### ✅ Task 2: Database Models
- **User Model**: Extended AbstractUser with additional fields
  - UUID primary key
  - Phone number field
  - Role field (guest, host, admin)
  - Created and updated timestamps

- **Conversation Model**: Many-to-many relationships
  - UUID primary key
  - Participants (ManyToMany with User)
  - Created timestamp

- **Message Model**: Foreign key relationships
  - UUID primary key
  - Sender (ForeignKey to User)
  - Conversation (ForeignKey to Conversation)
  - Message body and timestamp

### ✅ Task 3: API Serializers
- **UserSerializer**: Handles user data serialization
- **ConversationSerializer**: Manages conversation data with participant handling
- **MessageSerializer**: Processes message data with auto-sender assignment

### ✅ Task 4: API Views and ViewSets
- **UserViewSet**: CRUD operations for users
- **ConversationViewSet**: Conversation management with custom actions
- **MessageViewSet**: Message handling with permission checks

### ✅ Task 5: URL Configuration and Routing
- Configured Django REST router
- Set up API endpoints:
  - `/api/users/` - User management
  - `/api/conversations/` - Conversation management
  - `/api/messages/` - Message management
- Added admin interface access at `/admin/`

### ✅ Task 6: Testing and Quality Assurance
- Comprehensive test suite with 13 tests
- Model tests for all entities
- API endpoint tests
- Authentication and authorization tests
- All tests passing ✅

## 🛠️ Technology Stack

- **Backend**: Django 5.2.4
- **API Framework**: Django REST Framework 3.16.0
- **Database**: SQLite (development)
- **Authentication**: Django's built-in authentication
- **Testing**: Django TestCase and DRF APITestCase

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/` | API root with available endpoints |
| GET/POST | `/api/users/` | List users / Create user |
| GET/PUT/DELETE | `/api/users/{id}/` | User detail operations |
| GET/POST | `/api/conversations/` | List/Create conversations |
| GET/PUT/DELETE | `/api/conversations/{id}/` | Conversation operations |
| POST | `/api/conversations/{id}/add_participant/` | Add participant to conversation |
| GET/POST | `/api/messages/` | List/Create messages |
| GET/PUT/DELETE | `/api/messages/{id}/` | Message operations |

## 🔐 Security Features

- Session-based authentication
- Permission-based access control
- CSRF protection
- SQL injection protection (Django ORM)
- XSS protection

## 🗄️ Database Schema

### Users Table
- Primary Key: UUID
- Fields: username, email, first_name, last_name, phone_number, role
- Indexes: email, user_id

### Conversations Table  
- Primary Key: UUID
- Relationships: ManyToMany with Users
- Indexes: conversation_id

### Messages Table
- Primary Key: UUID
- Foreign Keys: sender_id, conversation_id
- Indexes: sender, conversation, sent_at

## 🧪 Testing Coverage

- **13 Tests Total**: All passing ✅
- Model functionality tests
- API endpoint accessibility tests
- Authentication/authorization tests
- Data creation and validation tests

## 🚀 Running the Application

1. **Start the server**:
   ```bash
   cd messaging_app
   python manage.py runserver
   ```

2. **Access the application**:
   - API Root: http://127.0.0.1:8000/api/
   - Admin Panel: http://127.0.0.1:8000/admin/ (admin/admin123)

3. **Run tests**:
   ```bash
   python manage.py test
   ```

## 📈 Performance Considerations

- Database indexes on frequently queried fields
- UUID primary keys for better scalability
- Efficient querysets with select_related/prefetch_related
- Proper pagination support
- Optimized serializers

## 🔮 Future Enhancements

- WebSocket support for real-time messaging
- File/media message support
- Message encryption
- Push notifications
- Message search functionality
- API rate limiting
- Caching layer

## ✨ Key Features Implemented

- ✅ User registration and authentication
- ✅ Conversation creation and management
- ✅ Message sending and retrieval
- ✅ Participant management
- ✅ RESTful API design
- ✅ Comprehensive admin interface
- ✅ Full test coverage
- ✅ Production-ready structure

---

**Project Status**: ✅ **COMPLETE**

All 6 tasks have been successfully implemented and tested. The messaging app is fully functional with a robust API, comprehensive testing, and proper documentation.

from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('delete-user/', views.delete_user, name='delete_user'),
    path('conversation/<int:message_id>/', views.threaded_conversation, name='threaded_conversation'),
    path('unread/', views.unread_messages, name='unread_messages'),
    path('history/<int:message_id>/', views.message_history, name='message_history'),
    path('conversation-messages/<int:conversation_id>/', views.conversation_messages, name='conversation_messages'),
]

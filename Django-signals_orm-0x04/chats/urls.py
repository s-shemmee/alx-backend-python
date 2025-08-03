from django.urls import path
from . import views

app_name = 'chats'

urlpatterns = [
    path('conversation/<int:conversation_id>/messages/', views.conversation_messages, name='conversation_messages'),
    path('conversation/<int:conversation_id>/threaded/', views.threaded_conversation_detail, name='threaded_conversation_detail'),
    path('conversations/', views.user_conversations, name='user_conversations'),
    path('conversation/<int:conversation_id>/clear-cache/', views.clear_conversation_cache, name='clear_conversation_cache'),
]

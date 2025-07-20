from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import UserViewSet, ConversationViewSet, MessageViewSet

# Create a router and register our viewsets with it
router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# Create nested routers for conversations -> messages
conversations_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# Combine both routers
urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
]

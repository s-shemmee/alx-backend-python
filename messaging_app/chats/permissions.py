from rest_framework import permissions
from rest_framework.permissions import BasePermission
from .models import Conversation, Message


class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """
    
    def has_permission(self, request, view):
        """
        Check if user is authenticated.
        """
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Check if user is a participant in the conversation or message conversation.
        """
        if isinstance(obj, Conversation):
            return obj.participants.filter(user_id=request.user.user_id).exists()
        elif isinstance(obj, Message):
            return obj.conversation.participants.filter(user_id=request.user.user_id).exists()
        return False


class IsOwnerOrParticipant(BasePermission):
    """
    Custom permission to only allow owners of a message or conversation participants.
    """
    
    def has_permission(self, request, view):
        """
        Check if user is authenticated.
        """
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Check if user is owner of the message or participant in conversation.
        """
        if isinstance(obj, Message):
            # For messages, check if user is sender or participant in conversation
            return (obj.sender == request.user or 
                   obj.conversation.participants.filter(user_id=request.user.user_id).exists())
        elif isinstance(obj, Conversation):
            # For conversations, check if user is participant
            return obj.participants.filter(user_id=request.user.user_id).exists()
        return False


class IsMessageSenderOrParticipant(BasePermission):
    """
    Permission for message operations - sender can edit/delete, participants can view.
    """
    
    def has_permission(self, request, view):
        """
        Check if user is authenticated.
        """
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Check permissions based on the HTTP method.
        """
        if isinstance(obj, Message):
            # Anyone who is a participant can view messages
            is_participant = obj.conversation.participants.filter(
                user_id=request.user.user_id
            ).exists()
            
            if request.method in permissions.SAFE_METHODS:
                # Read permissions for participants
                return is_participant
            else:
                # Write permissions only for message sender
                return obj.sender == request.user
        
        return False


class IsConversationParticipant(BasePermission):
    """
    Permission for conversation operations.
    """
    
    def has_permission(self, request, view):
        """
        Check if user is authenticated.
        """
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Check if user is a participant in the conversation.
        """
        if isinstance(obj, Conversation):
            return obj.participants.filter(user_id=request.user.user_id).exists()
        return False


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the object.
        return obj.sender == request.user if hasattr(obj, 'sender') else obj == request.user

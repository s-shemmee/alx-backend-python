from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import User, Conversation, Message
from .serializers import (
    UserSerializer, 
    ConversationSerializer, 
    ConversationListSerializer,
    MessageSerializer
)
from .permissions import (
    IsParticipantOfConversation,
    IsOwnerOrParticipant,
    IsMessageSenderOrParticipant,
    IsConversationParticipant
)
from .pagination import MessagePagination, ConversationPagination, UserPagination
from .filters import MessageFilter, ConversationFilter, UserFilter


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = UserPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = UserFilter
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering_fields = ['username', 'created_at']
    ordering = ['-created_at']


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing conversations.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsConversationParticipant]
    pagination_class = ConversationPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ConversationFilter
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Return conversations that the current user participates in.
        """
        return Conversation.objects.filter(
            participants=self.request.user
        ).prefetch_related('participants', 'messages')

    def get_serializer_class(self):
        """
        Return appropriate serializer class based on action.
        """
        if self.action == 'list':
            return ConversationListSerializer
        return ConversationSerializer

    def perform_create(self, serializer):
        """
        Create a new conversation and add the current user as a participant.
        """
        serializer.save()

    @action(detail=True, methods=['post'], url_path='add-participant')
    def add_participant(self, request, pk=None):
        """
        Add a participant to an existing conversation.
        """
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(user_id=user_id)
            conversation.participants.add(user)
            return Response(
                {'message': f'User {user.username} added to conversation'},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """
        Get all messages for a specific conversation.
        """
        conversation = self.get_object()
        messages = conversation.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsMessageSenderOrParticipant]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MessageFilter
    search_fields = ['message_body']
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']

    def get_queryset(self):
        """
        Return messages from conversations the current user participates in.
        """
        user_conversations = Conversation.objects.filter(
            participants=self.request.user
        )
        return Message.objects.filter(
            conversation__in=user_conversations
        ).select_related('sender', 'conversation')

    def perform_create(self, serializer):
        """
        Create a new message with the current user as sender.
        """
        conversation_id = serializer.validated_data.get('conversation').conversation_id
        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
        
        # Verify that the user is a participant in the conversation
        if not conversation.participants.filter(user_id=self.request.user.user_id).exists():
            raise PermissionError("You are not a participant in this conversation")
        
        serializer.save(sender=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a new message with permission checks.
        """
        try:
            return super().create(request, *args, **kwargs)
        except PermissionError:
            return Response(
                {"detail": "You are not a participant in this conversation"}, 
                status=status.HTTP_403_FORBIDDEN
            )

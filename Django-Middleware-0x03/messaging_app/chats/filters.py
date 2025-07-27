import django_filters
from django_filters import rest_framework as filters
from django.db.models import Q
from .models import Message, Conversation, User


class MessageFilter(filters.FilterSet):
    """
    Filter class for Message model.
    """
    # Filter by conversation
    conversation = filters.UUIDFilter(field_name='conversation__conversation_id')
    
    # Filter by sender
    sender = filters.UUIDFilter(field_name='sender__user_id')
    sender_username = filters.CharFilter(field_name='sender__username', lookup_expr='icontains')
    
    # Filter by date range
    sent_after = filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    sent_before = filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')
    date_range = filters.DateFromToRangeFilter(field_name='sent_at')
    
    # Filter by message content
    message_body = filters.CharFilter(field_name='message_body', lookup_expr='icontains')
    
    # Filter by specific users in conversation
    with_user = filters.UUIDFilter(method='filter_with_user')
    
    def filter_with_user(self, queryset, name, value):
        """
        Filter messages from conversations that include a specific user.
        """
        try:
            user = User.objects.get(user_id=value)
            conversations_with_user = Conversation.objects.filter(participants=user)
            return queryset.filter(conversation__in=conversations_with_user)
        except User.DoesNotExist:
            return queryset.none()
    
    class Meta:
        model = Message
        fields = {
            'message_body': ['exact', 'icontains'],
            'sent_at': ['exact', 'gte', 'lte'],
        }


class ConversationFilter(filters.FilterSet):
    """
    Filter class for Conversation model.
    """
    # Filter by participant
    participant = filters.UUIDFilter(field_name='participants__user_id')
    participant_username = filters.CharFilter(
        field_name='participants__username', 
        lookup_expr='icontains'
    )
    
    # Filter by creation date
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    date_range = filters.DateFromToRangeFilter(field_name='created_at')
    
    # Filter conversations with specific number of participants
    min_participants = filters.NumberFilter(method='filter_min_participants')
    max_participants = filters.NumberFilter(method='filter_max_participants')
    
    def filter_min_participants(self, queryset, name, value):
        """
        Filter conversations with at least specified number of participants.
        """
        return queryset.annotate(
            participant_count=filters.Count('participants')
        ).filter(participant_count__gte=value)
    
    def filter_max_participants(self, queryset, name, value):
        """
        Filter conversations with at most specified number of participants.
        """
        return queryset.annotate(
            participant_count=filters.Count('participants')
        ).filter(participant_count__lte=value)
    
    class Meta:
        model = Conversation
        fields = {
            'created_at': ['exact', 'gte', 'lte'],
        }


class UserFilter(filters.FilterSet):
    """
    Filter class for User model.
    """
    # Filter by role
    role = filters.ChoiceFilter(choices=User.ROLE_CHOICES)
    
    # Filter by name
    name = filters.CharFilter(method='filter_by_name')
    
    # Filter by email domain
    email_domain = filters.CharFilter(method='filter_by_email_domain')
    
    # Filter by creation date
    joined_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    joined_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    # Filter active users
    is_active = filters.BooleanFilter(field_name='is_active')
    
    def filter_by_name(self, queryset, name, value):
        """
        Filter by first name or last name.
        """
        return queryset.filter(
            Q(first_name__icontains=value) | Q(last_name__icontains=value)
        )
    
    def filter_by_email_domain(self, queryset, name, value):
        """
        Filter by email domain.
        """
        return queryset.filter(email__iendswith=value)
    
    class Meta:
        model = User
        fields = {
            'username': ['exact', 'icontains'],
            'email': ['exact', 'icontains'],
            'first_name': ['exact', 'icontains'],
            'last_name': ['exact', 'icontains'],
            'role': ['exact'],
            'is_active': ['exact'],
            'created_at': ['exact', 'gte', 'lte'],
        }

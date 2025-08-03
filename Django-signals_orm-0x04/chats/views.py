from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.db.models import Prefetch, Q, Count
from .models import Conversation, ChatMessage


@login_required
@cache_page(60)  # Task 5: Cache the view for 60 seconds
def conversation_messages(request, conversation_id):
    """
    Task 5: Cached view that displays messages in a conversation
    Uses advanced ORM techniques for efficient querying
    """
    # Get conversation with optimized queries using select_related and prefetch_related
    conversation = get_object_or_404(
        Conversation.objects.prefetch_related('participants'),
        id=conversation_id
    )
    
    # Check if user is a participant
    if request.user not in conversation.participants.all():
        return render(request, 'chats/access_denied.html')
    
    # Get messages with threaded structure using advanced ORM techniques
    # Task 3: Use prefetch_related and select_related for optimization
    messages = ChatMessage.objects.filter(
        conversation=conversation,
        parent_message=None  # Get root messages only
    ).select_related('sender').prefetch_related(
        Prefetch(
            'replies',
            queryset=ChatMessage.objects.select_related('sender').prefetch_related('read_by')
        ),
        'read_by'
    ).order_by('timestamp')
    
    context = {
        'conversation': conversation,
        'messages': messages,
        'user': request.user,
    }
    
    return render(request, 'chats/conversation_messages.html', context)


@login_required
def threaded_conversation_detail(request, conversation_id):
    """
    Task 3: Advanced ORM view for threaded conversations
    Demonstrates recursive query optimization
    """
    conversation = get_object_or_404(
        Conversation.objects.select_related().prefetch_related('participants'),
        id=conversation_id
    )
    
    # Optimized query for threaded messages
    all_messages = ChatMessage.objects.filter(
        conversation=conversation
    ).select_related('sender').prefetch_related('read_by').order_by('timestamp')
    
    # Build thread structure
    message_dict = {}
    root_messages = []
    
    for message in all_messages:
        message_dict[message.id] = {
            'message': message,
            'replies': []
        }
    
    # Build the thread hierarchy
    for message in all_messages:
        if message.parent_message:
            parent_id = message.parent_message.id
            if parent_id in message_dict:
                message_dict[parent_id]['replies'].append(message_dict[message.id])
        else:
            root_messages.append(message_dict[message.id])
    
    context = {
        'conversation': conversation,
        'threaded_messages': root_messages,
    }
    
    return render(request, 'chats/threaded_conversation.html', context)


@login_required
def user_conversations(request):
    """
    View to list all conversations for a user with optimized queries
    """
    conversations = Conversation.objects.filter(
        participants=request.user
    ).prefetch_related('participants').annotate(
        message_count=Count('messages')
    ).order_by('-updated_at')
    
    context = {
        'conversations': conversations,
    }
    
    return render(request, 'chats/user_conversations.html', context)


def clear_conversation_cache(request, conversation_id):
    """
    Utility view to clear cache for a specific conversation
    """
    from django.core.cache import cache
    from django.urls import reverse
    
    # Clear the cached view
    cache_key = f'views.decorators.cache.cache_page.{reverse("conversation_messages", args=[conversation_id])}'
    cache.delete(cache_key)
    
    return render(request, 'chats/cache_cleared.html')

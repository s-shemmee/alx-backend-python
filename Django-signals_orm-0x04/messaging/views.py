from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Prefetch
from .models import Message, Notification, MessageHistory


@login_required
def delete_user(request):
    """
    Task 2: View to delete user account and trigger cleanup signal
    """
    if request.method == 'POST':
        user = request.user
        # Log out the user before deletion
        from django.contrib.auth import logout
        logout(request)
        # Delete the user (this will trigger the post_delete signal)
        user.delete()
        messages.success(request, 'Your account has been successfully deleted.')
        return redirect('home')
    
    return render(request, 'messaging/delete_user.html')


@login_required
def threaded_conversation(request, message_id=None):
    """
    Task 3: View to display threaded conversations using advanced ORM techniques
    """
    if message_id:
        # Get the root message and all its replies using prefetch_related
        root_message = get_object_or_404(
            Message.objects.select_related('sender', 'receiver')
            .prefetch_related(
                Prefetch(
                    'replies',
                    queryset=Message.objects.select_related('sender', 'receiver')
                    .order_by('timestamp')
                )
            ),
            id=message_id,
            parent_message=None  # Ensure it's a root message
        )
        
        # Get all replies recursively
        def get_all_replies(message):
            replies = []
            for reply in message.replies.all():
                replies.append({
                    'message': reply,
                    'replies': get_all_replies(reply)
                })
            return replies
        
        conversation = {
            'root_message': root_message,
            'replies': get_all_replies(root_message)
        }
    else:
        conversation = None
    
    return render(request, 'messaging/threaded_conversation.html', {
        'conversation': conversation
    })


@login_required
def unread_messages(request):
    """
    Task 4: View to display unread messages using custom manager
    """
    # Use custom manager to get unread messages with optimized query
    unread_msgs = Message.unread_objects.unread_for_user(request.user)
    
    return render(request, 'messaging/unread_messages.html', {
        'unread_messages': unread_msgs
    })


@login_required
def message_history(request, message_id):
    """
    View to display message edit history for Task 1
    """
    message = get_object_or_404(Message, id=message_id)
    history = MessageHistory.objects.filter(message=message).order_by('-edited_at')
    
    return render(request, 'messaging/message_history.html', {
        'message': message,
        'history': history
    })

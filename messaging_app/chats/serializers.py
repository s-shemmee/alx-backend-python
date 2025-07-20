from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    class Meta:
        model = User
        fields = [
            'user_id', 'username', 'first_name', 'last_name', 
            'email', 'phone_number', 'role', 'created_at'
        ]
        read_only_fields = ['user_id', 'created_at']

    def create(self, validated_data):
        """
        Create and return a new User instance.
        """
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model.
    """
    sender = UserSerializer(read_only=True)
    sender_id = serializers.UUIDField(write_only=True, required=False)

    class Meta:
        model = Message
        fields = [
            'message_id', 'sender', 'sender_id', 'conversation', 
            'message_body', 'sent_at'
        ]
        read_only_fields = ['message_id', 'sent_at']

    def create(self, validated_data):
        """
        Create and return a new Message instance.
        """
        # Set sender from request user if not provided
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['sender'] = request.user
        return super().create(validated_data)


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation model with nested relationships.
    """
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'participants', 'participant_ids', 
            'messages', 'message_count', 'created_at'
        ]
        read_only_fields = ['conversation_id', 'created_at']

    def get_message_count(self, obj):
        """
        Return the count of messages in this conversation.
        """
        return obj.messages.count()

    def create(self, validated_data):
        """
        Create and return a new Conversation instance with participants.
        """
        participant_ids = validated_data.pop('participant_ids', [])
        conversation = Conversation.objects.create(**validated_data)
        
        # Add participants
        if participant_ids:
            participants = User.objects.filter(user_id__in=participant_ids)
            conversation.participants.set(participants)
        
        # Add request user as participant if not already included
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            conversation.participants.add(request.user)
        
        return conversation


class ConversationListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing conversations.
    """
    participants = UserSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'participants', 'last_message', 
            'message_count', 'created_at'
        ]

    def get_last_message(self, obj):
        """
        Return the last message in this conversation.
        """
        last_message = obj.messages.first()  # Already ordered by -sent_at
        if last_message:
            return {
                'message_id': last_message.message_id,
                'sender': last_message.sender.username,
                'message_body': last_message.message_body,
                'sent_at': last_message.sent_at
            }
        return None

    def get_message_count(self, obj):
        """
        Return the count of messages in this conversation.
        """
        return obj.messages.count()

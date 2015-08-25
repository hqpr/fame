from django.shortcuts import render
from apps.artist.models import UserConnections
from .models import Conversation, Message
from django.db.models import Q

def messages(request):
    connections = UserConnections.objects.filter(user=request.user)
    conversations = Conversation.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
    data = {'connections': connections,
            'conversations': conversations}
    return render(request, 'messages.html', data)


def conversation(request, pk):
    conversation = Message.objects.filter(conversation=pk)
    receiver = Conversation.objects.get(id=pk, active=True)
    conversation_id = pk
    return render(request, 'single_conversation.html', {
        'conversation': conversation,
        'receiver': receiver,
        'conversation_id': conversation_id
    })

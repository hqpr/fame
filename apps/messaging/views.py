from django.shortcuts import render
from apps.artist.models import UserConnections
from .models import Conversation, Message

def messages(request):
    connections = UserConnections.objects.filter(user=request.user)
    conversations = Conversation.objects.filter(sender=request.user, active=True)
    data = {'connections': connections,
            'conversations': conversations}
    return render(request, 'messages.html', data)


def conversation(request, pk):
    conversation = Message.objects.get(converstaion=pk, sender=request.user)
    return render(request, 'single_conversation.html', {'conversation': conversation})

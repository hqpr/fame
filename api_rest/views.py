import pytz
from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from media.models import AudioLike, AudioComment, AudioPlaylist, PlaylistItem
from userprofile.models import UserProfile, UserStatus
from artist.models import UserConnections
from .serializers import AudioCommentSerializer, AudioLikeSerializer, AudioPlaylistSerializer, PlaylistItemSerializer, UserProfileSerializer,\
                         UserStatusSerializer, UserConnectionsSerializer
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@api_view(['GET','POST'])
def audio_like(request):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = AudioLike.objects.all()
        serializer = AudioLikeSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AudioLikeSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(fan=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
                return Response("Can't like the same track twice", status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def audio_comment(request):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = AudioComment.objects.all()
        serializer = AudioCommentSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AudioCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(fan=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def playlists(request):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = AudioPlaylist.objects.all()
        serializer = AudioPlaylistSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AudioPlaylistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def playlist(request, **kwargs):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        try:
            playlist = AudioPlaylist.objects.get(id=kwargs["playlist_id"])
        except:
            return Response("No such playlist", status=status.HTTP_400_BAD_REQUEST)
        snippets = PlaylistItem.objects.filter(playlist=playlist)
        serializer = PlaylistItemSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        try:
            playlist = AudioPlaylist.objects.get(id=kwargs["playlist_id"], user=request.user)
        except:
            return Response("Permission denied", status=status.HTTP_400_BAD_REQUEST)

        serializer = PlaylistItemSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(playlist=playlist)
            except:
                return Response("Cannot add the same track more than once to a playlist", status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def profile_details(request, **kwargs):
    """
    List all snippets, or create a new snippet.
    """
    try:
        user = request.user
        profile = UserProfile.objects.get(user=user)
    except:
        return Response("Permission denied", status=status.HTTP_400_BAD_REQUEST)


    if "about" in request.POST:
        serializer = UserProfileSerializer(profile, data={'about': request.POST["about"]}, partial=True)
    elif "display_name" in request.POST:
        serializer = UserProfileSerializer(profile, data={'display_name': request.POST["display_name"]}, partial=True)
    else:
        return Response("Cannot update this profile", status=status.HTTP_400_BAD_REQUEST)
    if serializer.is_valid():
        try:
            serializer.save(user=request.user)
        except:
            return Response("Cannot update this profile", status=status.HTTP_400_BAD_REQUEST)
        return Response("Successfully updated", status=status.HTTP_201_CREATED)
    return Response("Cannot update this profile", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST'])
def user_status(request, **kwargs):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        try:
            snippets = UserStatus.objects.filter(user=UserProfile.objects.get(user=request.user))
        except:
            return Response("No statuses", status=status.HTTP_400_BAD_REQUEST)
        serializer = UserStatusSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        try:
            user = request.user
            profile = UserProfile.objects.get(user=user)
        except:
            return Response("Permission denied", status=status.HTTP_400_BAD_REQUEST)

        serializer = UserStatusSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(user=UserProfile.objects.get(user=request.user),created=datetime.now(tz=pytz.UTC))
            except:
                return Response("Cannot update this profile", status=status.HTTP_400_BAD_REQUEST)
            return Response("Successfully updated", status=status.HTTP_201_CREATED)
        return Response("Cannot update this profile", status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def user_connect(request, **kwargs):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        try:
            snippets = UserConnections.objects.filter(user=request.user)
        except:
            return Response("No statuses", status=status.HTTP_400_BAD_REQUEST)
        serializer = UserConnectionsSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        try:
            user = request.user
        except:
            return Response("Permission denied", status=status.HTTP_400_BAD_REQUEST)

        if kwargs["user_id"] == request.user.id:
            return Response("Permission denied", status=status.HTTP_400_BAD_REQUEST)
            
        serializer = UserConnectionsSerializer(data={"connection": kwargs["user_id"]})
        if serializer.is_valid():
            try:
                serializer.save(user=request.user)
            except:
                return Response("Cannot update this profile", status=status.HTTP_400_BAD_REQUEST)
            return Response("Successfully updated", status=status.HTTP_201_CREATED)
        return Response("Cannot update this profile", status=status.HTTP_400_BAD_REQUEST)
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from media.models import AudioLike, AudioComment, AudioPlaylist, PlaylistItem
from .serializers import AudioCommentSerializer, AudioLikeSerializer, AudioPlaylistSerializer, PlaylistItemSerializer

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

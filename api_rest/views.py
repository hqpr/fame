import pytz
from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from media.models import Audio, AudioLike, AudioComment, AudioPlaylist, PlaylistItem, Video, VideoLike, VideoComment
from userprofile.models import UserProfile, UserStatus
from artist.models import UserConnections
from competition.models import Competition
from .serializers import AudioCommentSerializer, AudioLikeSerializer, AudioPlaylistSerializer, PlaylistItemSerializer, UserProfileSerializer,\
                         UserStatusSerializer, UserConnectionsSerializer, VideoCommentSerializer, VideoLikeSerializer, \
                         CompetitionSerializer
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# Artist Views

@api_view(['GET'])
def list_artists(request, **kwargs):
    """
    Handle display of artists

    Accepts:

        c - country, CSV
        g - genre, CSV
    """
    filters = {
        "account_type": 1
    }
    if "c" in request.GET and len(request.GET["c"]):
        filters["country__in"] = request.GET["c"].split(",")
    if "g" in request.GET and len(request.GET["g"]):
        filters["usergenre__genre__in"] = request.GET["g"].split(",")
    try:
        snippets = UserProfile.objects.filter(**filters)
    except:
        return Response("No users", status=status.HTTP_400_BAD_REQUEST)
    serializer = UserProfileSerializer(snippets, many=True)
    return Response(serializer.data)


@api_view(['GET','POST'])
def user_status(request, **kwargs):
    """
    Handle update of current user status
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


@api_view(['POST'])
def profile_details(request, **kwargs):
    """
    Handle updating profile details via Ajax

    Covers: About and Display Name
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
def user_connect(request, **kwargs):
    """
    Handle connecting with other user
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



# Competition Views

@api_view(['GET'])
def list_competitions(request, **kwargs):
    """
    Handle display of competitions

    Accepts:
    
        c - country, CSV
        g - genre, CSV
        s - status, BOOL (0,1)
    """
    filters = {
        "public": True,
        "active": True,
        "date_end__gte": datetime.now(tz=pytz.UTC)
    }
    if "c" in request.GET and len(request.GET["c"]):
        filters["competitioncountry__country__in"] = request.GET["c"].split(",")
    if "g" in request.GET and len(request.GET["g"]):
        filters["competitiongenre__genre__name__in"] = request.GET["g"].split(",")
    if "s" in request.GET and request.GET["s"] == "0":
        del(filters["date_end__gte"])
        filters["date_end__lte"] = datetime.now(tz=pytz.UTC)
    print filters
    try:
        snippets = Competition.objects.filter(**filters)
    except:
        return Response("No competitions", status=status.HTTP_400_BAD_REQUEST)
    serializer = CompetitionSerializer(snippets, many=True)
    return Response(serializer.data)


# Media Views
@api_view(['DELETE'])
def audio(request, *args, **kwargs):
    """
    Handle audio
    """
    if request.method == 'DELETE':
        
        try:
            audio = Audio.objects.get(id=kwargs["audio_id"], user=request.user)
        except:
            return Response("Permission denied", status=status.HTTP_400_BAD_REQUEST)

        try:
            audio.delete()
            return Response("Track deleted", status=status.HTTP_201_CREATED)
        except:
            return Response("Cannot delete this track", status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def video(request, *args, **kwargs):
    """
    Handle video
    """
    if request.method == 'DELETE':
        
        try:
            video = Video.objects.get(id=kwargs["video_id"], user=request.user)
        except:
            return Response("Permission denied", status=status.HTTP_400_BAD_REQUEST)

        try:
            video.delete()
            return Response("Video deleted", status=status.HTTP_201_CREATED)
        except:
            return Response("Cannot delete this video", status=status.HTTP_400_BAD_REQUEST)

    

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
def video_like(request):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = VideoLike.objects.all()
        serializer = VideoLikeSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = VideoLikeSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(fan=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
                return Response("Can't like the same video twice", status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def video_comment(request):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = VideoComment.objects.all()
        serializer = VideoCommentSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = VideoCommentSerializer(data=request.data)
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

@api_view(['GET','POST','DELETE'])
def playlist(request, *args, **kwargs):
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

    elif request.method == 'DELETE':
        try:
            playlist = AudioPlaylist.objects.get(id=kwargs["playlist_id"], user=request.user)
        except:
            return Response("Permission denied", status=status.HTTP_400_BAD_REQUEST)

        playlist_items = PlaylistItem.objects.filter(playlist=playlist)
        if len(playlist_items):
            playlist_items.delete()
        playlist.delete()
        return Response("Playlist deleted", status=status.HTTP_201_CREATED)



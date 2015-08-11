from datetime import datetime

import pytz
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.media.models import Audio, AudioLike, AudioComment, AudioPlaylist, PlaylistItem, Video, VideoLike, VideoComment
from apps.userprofile.models import UserProfile, UserStatus
from apps.artist.models import UserConnections
from apps.competition.models import Competition, CompetitionChart, CompetitionEntryRating, CompetitionJudge,\
                               CompetitionEntry
from .serializers import AudioCommentSerializer, AudioLikeSerializer, AudioPlaylistSerializer, PlaylistItemSerializer, UserProfileSerializer,\
                         UserStatusSerializer, UserConnectionsSerializer, VideoCommentSerializer, VideoLikeSerializer, \
                         CompetitionSerializer, CompetitionChartSerializer, AudioSerializer, VideoSerializer


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

        profiles = UserProfile.objects.filter(user__id__in=[i.connection.id for i in snippets])
        serializer = UserProfileSerializer(profiles, many=True)
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

@api_view(['GET'])
def chart_list(request, *args, **kwargs):
    """Handle display of chart
    
    expects competition_slug"""
    try:
        competition_slug = kwargs["competition_slug"]
    except:
        return Response("No competition set", status=status.HTTP_400_BAD_REQUEST)

    try:
        snippets = CompetitionChart.objects.filter(entry__competition=Competition.objects.get(slug=competition_slug)).order_by('-current_score')
    except:
        return Response("No chart entries", status=status.HTTP_400_BAD_REQUEST)
    
    serializer = CompetitionChartSerializer(snippets, many=True)
    # return Response(chart_items, status=status.HTTP_201_CREATED)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def chart_update(request, *args, **kwargs):
    """Handle display of chart
    
    expects competition_slug"""
    try:
        competition_slug = kwargs["competition_slug"]
        competition = Competition.objects.get(slug=competition_slug)
    except:
        return Response("No competition set", status=status.HTTP_400_BAD_REQUEST)

    competition_chart = CompetitionChart()
    competition_chart.create_chart(competition)
    try:
        snippets = CompetitionChart.objects.filter(entry__competition=Competition.objects.get(slug=competition_slug)).order_by('-current_score')
    except:
        return Response("No chart entries", status=status.HTTP_400_BAD_REQUEST)
    serializer = CompetitionChartSerializer(snippets, many=True)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def competition_entry_rating(request, *args, **kwargs):
    """Handle rating"""
    try:
        competition = Competition.objects.get(slug=kwargs["competition_slug"])
        competition_entry = CompetitionEntry.objects.get(id=kwargs["competition_entry_id"],competition=competition)
        judge = CompetitionJudge.objects.get(competition=competition, judge=request.user)
    except:
        return Response("You are not allowed to rate", status=status.HTTP_400_BAD_REQUEST)
    
    rating = request.data["rating"]
    try:
        competition_entry_rating = CompetitionEntryRating.objects.get(judge=judge,competition_entry=competition_entry)
        return Response("You are only allowed to rate once", status=status.HTTP_400_BAD_REQUEST)
    except:
        pass

    description = ""
    if "description" in request.data:
        description = request.data["description"]

    competition_entry_rating = CompetitionEntryRating(**{"judge":judge,"competition_entry":competition_entry,"rating":rating,"description":description})
    competition_entry_rating.save()
    return Response("Updated", status=status.HTTP_201_CREATED)


# Media Views


@api_view(['GET'])
def all_media(request, *args, **kwargs):
    """
    Handle all media
    """
    tracks = []
    videos = []
    playlists = []

    if not "media_type" in kwargs or kwargs["media_type"] == "track":
        audio_objects = Audio.public_objects.all().order_by('-added')
        tracks = AudioSerializer(audio_objects, many=True).data

    if not "media_type" in kwargs or kwargs["media_type"] == "video":
        video_objects = Video.public_objects.all().order_by('-added')
        videos = VideoSerializer(video_objects, many=True).data

    if not "media_type" in kwargs or kwargs["media_type"] == "playlist":
        playlist_objects = AudioPlaylist.objects.all().order_by('-added')
        playlists = AudioPlaylistSerializer(playlist_objects, many=True).data

    media = {
        "tracks": tracks,
        "videos": videos,
        "playlists": playlists,
    }
    return Response(media, status=status.HTTP_201_CREATED)

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



from datetime import datetime

import pytz
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

from apps.competition.models import Competition, CompetitionChart, CompetitionGenre,\
                               CompetitionCountry, CompetitionEntryAudio, CompetitionEntryVideo,\
                               CompetitionEntryRating, CompetitionStage
from apps.media.models import Audio, AudioLike, AudioComment, AudioPlaylist, PlaylistItem, Video, VideoLike, VideoComment
from apps.userprofile.models import UserProfile, UserStatus
from apps.artist.models import UserConnections


# Handle Media updates

class UserNameSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=100)
    name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, user):
        userprofile = UserProfile.objects.get(user=user)
        return userprofile.display_name


class AudioSerializer(serializers.ModelSerializer):
    user = UserNameSerializer()
    genre = serializers.ReadOnlyField(source='genre.name')
    likes = serializers.SerializerMethodField('get_total_likes')
    cover_200 = serializers.SerializerMethodField('get_200_thumbnail')

    def get_total_likes(self, audio):
        return len(AudioLike.objects.filter(audio=audio))

    def get_200_thumbnail(self, audio):
        im = get_thumbnail(audio.cover, '200x200', crop='center', quality=99)
        return im.url

    class Meta:
        model = Audio

    def perform_create(self, serializer):
        serializer.save()

class VideoSerializer(serializers.ModelSerializer):
    user = UserNameSerializer()
    genre = serializers.ReadOnlyField(source='genre.name')
    cover_400 = serializers.SerializerMethodField('get_400_thumbnail')

    def get_400_thumbnail(self, audio):
        im = get_thumbnail(audio.cover, '400x200', crop='center', quality=99)
        return im.url

    class Meta:
        model = Video

    def perform_create(self, serializer):
        serializer.save()

class AudioLikeSerializer(serializers.ModelSerializer):
    fan = serializers.ReadOnlyField(source='fan.username')

    class Meta:
        model = AudioLike

    def perform_create(self, serializer):
        serializer.save()

class AudioCommentSerializer(serializers.ModelSerializer):
    fan = serializers.ReadOnlyField(source='fan.username')
    approved = serializers.ReadOnlyField()

    class Meta:
        model = AudioComment

    def perform_create(self, serializer):
        serializer.save()

class VideoLikeSerializer(serializers.ModelSerializer):
    fan = serializers.ReadOnlyField(source='fan.username')

    class Meta:
        model = VideoLike

    def perform_create(self, serializer):
        serializer.save()

class VideoCommentSerializer(serializers.ModelSerializer):
    fan = serializers.ReadOnlyField(source='fan.username')
    approved = serializers.ReadOnlyField()

    class Meta:
        model = VideoComment

    def perform_create(self, serializer):
        serializer.save()

class AudioPlaylistSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    cover_200 = serializers.SerializerMethodField('get_200_thumbnail')
    playlist_items = serializers.SerializerMethodField('get_playlist_tracks')

    def get_200_thumbnail(self, playlist):
        im = get_thumbnail(playlist.cover, '200x200', crop='center', quality=99)
        return im.url

    def get_playlist_tracks(self, playlist):
        items = PlaylistItem.objects.filter(playlist=playlist)
        return PlaylistItemSerializer(items, many=True).data

    class Meta:
        model = AudioPlaylist

    def perform_create(self, serializer):
        serializer.save()

class CompetitionCountrySerializer(serializers.ModelSerializer):
    country_full = serializers.ReadOnlyField(source='country.name')

    class Meta:
        model = CompetitionCountry
        fields = ("country","country_full",)

class CompetitionGenreSerializer(serializers.ModelSerializer):
    genre_name = serializers.ReadOnlyField(source='genre.name')
    class Meta:
        model = CompetitionGenre
        fields = ("genre","genre_name",)

class CompetitionSerializer(serializers.ModelSerializer):
    countries = serializers.SerializerMethodField('get_country_information')
    genres = serializers.SerializerMethodField('get_genre_information')
    current_stage = serializers.SerializerMethodField('get_current_stage_information')

    def get_country_information(self, competition):
        countries = CompetitionCountry.objects.filter(competition=competition)
        return CompetitionCountrySerializer(countries, many=True).data

    def get_genre_information(self, competition):
        genres = CompetitionGenre.objects.filter(competition=competition)
        return CompetitionGenreSerializer(genres, many=True).data

    def get_current_stage_information(self, competition):
        if not competition.active:
            return {"text": "Not accepting entries"}
        if datetime.now(tz=pytz.UTC) < competition.date_start:
            return {"text": "Submissions open in", "timing": (competition.date_start-datetime.now(tz=pytz.UTC)).total_seconds()}
        if datetime.now(tz=pytz.UTC) > competition.date_end:
            return {"text":"Competition Ended"}
            
        stages = CompetitionStage.objects.filter(competition=competition,date_start__lte=datetime.now(tz=pytz.UTC),date_end__gte=datetime.now(tz=pytz.UTC))
        if not len(stages):
            return {"text": "Not accepting entries"}
        stage = stages[0]
        if stage.new_entries_open:
            return {"text": "Submissions open", "timing": (stage.date_end-datetime.now(tz=pytz.UTC)).total_seconds()}
        else:
            return {"text": "Submissions closed"}


    
    class Meta:
        model = Competition

class CompetitionChartSerializer(serializers.ModelSerializer):
    track = serializers.SerializerMethodField('get_audio_information')
    video = serializers.SerializerMethodField('get_video_information')
    position = serializers.SerializerMethodField('get_current_position')
    competition_entry_id = serializers.SerializerMethodField('get_entry_id')

    def get_audio_information(self, chart_item):
        competition_entry_audio = CompetitionEntryAudio.objects.get(competition_entry=chart_item.entry)
        return AudioSerializer(competition_entry_audio.entry).data

    def get_video_information(self, chart_item):
        competition_entry_video = CompetitionEntryVideo.objects.get(competition_entry=chart_item.entry)
        return VideoSerializer(competition_entry_video.entry).data

    def get_current_position(self, chart_item):
        current_items = len(CompetitionChart.objects.filter(entry__competition=chart_item.entry.competition, current_score__gt=chart_item.current_score))
        return current_items + 1

    def get_entry_id(self, chart_item):
        return chart_item.entry.id

    class Meta:
        model = CompetitionChart

class CompetitionEntryAudioSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompetitionEntryAudio

class CompetitionEntryRatingSerializer(serializers.ModelSerializer):
    judge = serializers.ReadOnlyField(source='judge.judge.user.username')

    class Meta:
        model = CompetitionEntryRating
        

class PlaylistItemSerializer(serializers.ModelSerializer):
    playlist = serializers.ReadOnlyField(source='playlist.title')
    audio = serializers.SerializerMethodField('get_audio_information')

    def get_audio_information(self, playlist_item):
        return AudioSerializer(playlist_item.audio).data

    class Meta:
        model = PlaylistItem

    def perform_create(self, serializer):
        serializer.save()

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = UserProfile

    def perform_create(self, serializer):
        serializer.save()

class UserStatusSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    created = serializers.ReadOnlyField()

    class Meta:
        model = UserStatus

    def perform_create(self, serializer):
        serializer.save()

class UserConnectionsSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = UserConnections

    def perform_create(self, serializer):
        serializer.save()

class UserConnectionsProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = UserProfile

    def perform_create(self, serializer):
        serializer.save()
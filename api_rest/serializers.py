from django.forms import widgets
from rest_framework import serializers

from media.models import AudioLike, AudioComment, AudioPlaylist, PlaylistItem
from userprofile.models import UserProfile, UserStatus
from artist.models import UserConnections

# Handle Media updates
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

class AudioPlaylistSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = AudioPlaylist

    def perform_create(self, serializer):
        serializer.save()

class PlaylistItemSerializer(serializers.ModelSerializer):
    playlist = serializers.ReadOnlyField(source='playlist.title')

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
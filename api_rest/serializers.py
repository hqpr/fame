from django.forms import widgets
from rest_framework import serializers

from media.models import AudioLike, AudioComment, AudioPlaylist, PlaylistItem

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
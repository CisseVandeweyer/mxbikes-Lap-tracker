from rest_framework import serializers
from .models import *

class LapSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    discord_id = serializers.CharField(write_only=True)  # Nieuw veld
    track_name = serializers.CharField(write_only=True)
    time_string = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Lap
        fields = ['id', 'username', 'discord_id', 'track_name', 'time_string', 'lap_time', 'timestamp']
        read_only_fields = ['lap_time', 'timestamp']

    def create(self, validated_data):
        username = validated_data.pop('username')
        discord_id = validated_data.pop('discord_id')  # Nieuwe variabele
        track_name = validated_data.pop('track_name')
        time_string = validated_data.pop('time_string')

        try:
            if ":" in time_string:
                minutes, seconds = time_string.split(":")
                total_time = int(minutes) * 60 + float(seconds)
            else:
                total_time = float(time_string)
        except ValueError:
            raise serializers.ValidationError({"time_string": "Invalid time format. Use mm:ss.xxx"})

        validated_data['lap_time'] = total_time

        # Lookup of create op basis van discord_id
        user, _ = User.objects.get_or_create(discord_id=discord_id, defaults={'username': username})
        track, _ = Track.objects.get_or_create(name=track_name)

        lap = Lap.objects.create(user=user, track=track, **validated_data)
        return lap

from rest_framework import serializers
from .models import VideoSession
from authApp.serializers import UserSerializer

class VideoSessionSerializer(serializers.ModelSerializer):
    therapist = UserSerializer(read_only=True)
    patient = UserSerializer(read_only=True)
    patient_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = VideoSession
        fields = ['id', 'therapist', 'patient', 'patient_id', 'room_id', 'created_at', 'is_active']
        read_only_fields = ['id', 'therapist', 'room_id', 'created_at']
        
    def create(self, validated_data):
        validated_data['therapist'] = self.context['request'].user
        return super().create(validated_data) 
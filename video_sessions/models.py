from django.db import models
from authApp.models import Therapist, Patient
import uuid

class VideoSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE, related_name='video_sessions')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='video_sessions')
    room_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    email_sent = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Video Session between {self.therapist.user.email} and {self.patient.user.email}" 
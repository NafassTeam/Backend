from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from .models import VideoSession
from .serializers import VideoSessionSerializer
from authApp.models import User, Patient, Therapist
import uuid
import hmac
import hashlib
import base64
import struct
import time
import urllib.parse

class VideoSessionViewSet(viewsets.ModelViewSet):
    serializer_class = VideoSessionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'therapist'):
            return VideoSession.objects.filter(therapist=user.therapist)
        elif hasattr(user, 'patient'):
            return VideoSession.objects.filter(patient=user.patient)
        return VideoSession.objects.none()

    def generate_zego_token(self, user_id, effective_time=3600):
        """
        Generate a ZEGOCLOUD token for video session
        """
        app_id = int(settings.ZEGO_APP_ID)
        server_secret = settings.ZEGO_SERVER_SECRET
        
        # Token parameters
        payload = ""
        create_time = int(time.time())
        
        # Combine information to be signed
        header = struct.pack(">I", app_id) 
        header += struct.pack(">H", len(user_id)) + user_id.encode()
        header += struct.pack(">Q", create_time)
        header += struct.pack(">Q", create_time + effective_time)
        header += struct.pack(">H", len(payload)) + payload.encode()
        
        # Sign the header using HMAC-SHA256
        sign_content = hmac.new(server_secret.encode(), header, hashlib.sha256).digest()
        
        # Combine all components and encode
        content = header + sign_content
        return base64.b64encode(content).decode()
    
    @action(detail=False, methods=['post'])
    def create_room(self, request):
        """
        Create a new video session and send invitation to patient
        """
        try:
            # Ensure the requesting user is a therapist
            if not hasattr(request.user, 'therapist'):
                return Response({
                    'error': 'Only therapists can create video sessions'
                }, status=status.HTTP_403_FORBIDDEN)
                
            therapist = request.user.therapist
            patient_id = request.data.get('patient_id')
            
            try:
                patient = Patient.objects.get(id=patient_id)
                
                # Check if patient is associated with this therapist through a match
                if not patient.matches.filter(therapist=therapist).exists():
                    return Response({
                        'error': 'This patient is not associated with you'
                    }, status=status.HTTP_403_FORBIDDEN)
                    
            except Patient.DoesNotExist:
                return Response({
                    'error': 'Patient not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Create video session
            room_id = str(uuid.uuid4())
            session = VideoSession.objects.create(
                therapist=therapist,
                patient=patient,
                room_id=room_id
            )
            
            # Generate patient token (valid for 24 hours)
            user_id = str(patient.user.id)
            token = self.generate_zego_token(user_id, effective_time=3600 * 24)
            app_id = settings.ZEGO_APP_ID
            
            # Generate room URL with all parameters
            room_url = (
                f"{settings.FRONTEND_URL}/video-room/{room_id}?"
                f"token={token}&"
                f"user_id={user_id}&"
                f"user_name={urllib.parse.quote(patient.user.get_full_name())}&"
                f"app_id={app_id}"
            )
            
            # Send email to patient
            send_mail(
                'Video Session Invitation',
                f'You have been invited to a video session with Dr. {request.user.get_full_name()}.\n\n'
                f'Click here to join instantly: {room_url}\n\n'
                f'This link will be valid for the next 24 hours.',
                settings.DEFAULT_FROM_EMAIL,
                [patient.user.email],
                fail_silently=False,
            )
            
            # Mark email as sent
            session.email_sent = True
            session.save()
            
            return Response({
                'room_id': room_id,
                'room_url': room_url,
                'message': 'Room created and invitation sent successfully'
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def get_token(self, request):
        """
        Get a token for joining a video session (used by therapist)
        """
        room_id = request.query_params.get('room_id')
        if not room_id:
            return Response({
                'error': 'Room ID is required'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            session = VideoSession.objects.get(room_id=room_id)
            
            # Check if user is either the therapist or patient
            user_is_therapist = hasattr(request.user, 'therapist') and request.user.therapist == session.therapist
            user_is_patient = hasattr(request.user, 'patient') and request.user.patient == session.patient
            
            if not (user_is_therapist or user_is_patient):
                return Response({
                    'error': 'You are not authorized to join this session'
                }, status=status.HTTP_403_FORBIDDEN)
            
            if not session.is_active:
                return Response({
                    'error': 'This session is no longer active'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Generate token
            user_id = str(request.user.id)
            token = self.generate_zego_token(user_id)
            app_id = settings.ZEGO_APP_ID
            
            return Response({
                'token': token,
                'room_id': room_id,
                'user_id': user_id,
                'user_name': request.user.get_full_name(),
                'app_id': app_id
            })
            
        except VideoSession.DoesNotExist:
            return Response({
                'error': 'Session not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def validate_url_token(self, request):
        """
        Validate a token provided in the URL (used for patient direct join)
        """
        room_id = request.query_params.get('room_id')
        token = request.query_params.get('token')
        user_id = request.query_params.get('user_id')
        
        if not all([room_id, token, user_id]):
            return Response({
                'error': 'Missing required parameters'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            # Decode token
            decoded = base64.b64decode(token)
            
            # Extract timestamp from token
            app_id_bytes = decoded[:4]
            user_id_len = struct.unpack(">H", decoded[4:6])[0]
            token_user_id = decoded[6:6+user_id_len].decode()
            create_time = struct.unpack(">Q", decoded[6+user_id_len:14+user_id_len])[0]
            expire_time = struct.unpack(">Q", decoded[14+user_id_len:22+user_id_len])[0]
            
            # Verify token hasn't expired
            current_time = int(time.time())
            if current_time > expire_time:
                return Response({
                    'error': 'Token has expired'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            # Verify user_id matches
            if token_user_id != user_id:
                return Response({
                    'error': 'Invalid token'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            # Verify session exists and is active
            session = VideoSession.objects.get(room_id=room_id)
            if not session.is_active:
                return Response({
                    'error': 'Session is no longer active'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            return Response({
                'valid': True,
                'message': 'Token is valid'
            })
            
        except Exception as e:
            return Response({
                'error': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST) 
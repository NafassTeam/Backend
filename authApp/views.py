from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import (
    PatientCreateSerializer,
    TherapistCreateSerializer,
    UserSerializer,
    PatientSerializer,
    TherapistSerializer,
    LoginSerializer,
    MatchSerializer,
    SessionSerializer
)
from .models import User, Patient, Therapist, Match, Session
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsAdmin, IsAdminOrSelfPatient, IsAdminOrSelfTherapist
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import HttpResponse


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]


class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAdminOrSelfPatient]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Patient.objects.all()
        return Patient.objects.filter(user=user)

    @action(detail=False, methods=["get", "put", "patch", "delete"], url_path="me")
    def me(self, request):
        try:
            patient = Patient.objects.get(user=request.user)
        except Patient.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.method == "GET":
            serializer = self.get_serializer(patient)
            return Response(serializer.data)

        elif request.method in ["PUT", "PATCH"]:
            serializer = self.get_serializer(
                patient, data=request.data, partial=(request.method == "PATCH")
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        elif request.method == "DELETE":
            patient.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class TherapistViewSet(ModelViewSet):
    queryset = Therapist.objects.all()
    serializer_class = TherapistSerializer
    permission_classes = [IsAdminOrSelfTherapist]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Therapist.objects.all()
        return Therapist.objects.filter(user=user)

    @action(detail=False, methods=["get", "put", "patch", "delete"], url_path="me")
    def me(self, request):
        try:
            therapist = Therapist.objects.get(user=request.user)
        except Therapist.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.method == "GET":
            serializer = self.get_serializer(therapist)
            return Response(serializer.data)

        elif request.method in ["PUT", "PATCH"]:
            serializer = self.get_serializer(
                therapist, data=request.data, partial=(request.method == "PATCH")
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        elif request.method == "DELETE":
            therapist.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class PatientCreateView(generics.CreateAPIView):
    serializer_class = PatientCreateSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Send verification email
        send_verification_email(user)

        return Response(
            {
                "message": "Patient registered successfully. Please log in.",
                "login_url": "auth/api/login/",
            },
            status=status.HTTP_201_CREATED,
        )


class TherapistCreateView(generics.CreateAPIView):
    serializer_class = TherapistCreateSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Send verification email
        try:
            send_verification_email(user)
        except Exception as e:
            print(f"Email send error: {e}")  # or use logging

        return Response(
            {"message": "Therapist registered successfully. Please log in."},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]

            # Check if email is verified
            if not user.is_verified:
                return Response(
                    {"detail": "Email not verified. Please check your inbox."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            refresh = RefreshToken.for_user(user)
            role = user.role if user.role else "unknown"
            return Response(
                {
                    "user": {"email": user.email, "role": role},
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_verification_email(user):

    token = user.email_verification_token
    verification_url = f"{settings.FRONTEND_URL}/verify-email/{token}/"
    print("Token:", user.email_verification_token)  # debug
    print("Email:", user.email)  # debug

    send_mail(
        subject="Verify Your Email",
        message=f"Please verify your email by clicking the following link: {verification_url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )


def verify_email(request, token):
    user = get_object_or_404(User, email_verification_token=token)
    user.is_verified = True
    user.save()
    return HttpResponse("Email successfully verified!")


# view to create, update, delete and get matches
class MatchViewSet(ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Match.objects.all()
        if hasattr(user, 'therapist'):
            return Match.objects.filter(therapist=user.therapist)
        elif hasattr(user, 'patient'):
            return Match.objects.filter(patient=user.patient)
        return Match.objects.none()

    @action(detail=False, methods=["get", "put", "patch", "delete"], url_path="me")
    def me(self, request):
        user = request.user

        if hasattr(user, "patient"):
            matches = Match.objects.filter(patient=user.patient)
        elif hasattr(user, "therapist"):
            matches = Match.objects.filter(therapist=user.therapist)
        else:
            return Response(
                {"detail": "No associated profile found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if request.method == "GET":
            serializer = self.get_serializer(matches, many=True)
            return Response(serializer.data)

        if not matches.exists():
            return Response(
                {"detail": "No matches found."}, status=status.HTTP_404_NOT_FOUND
            )

        match = matches.first()  # or logic to choose the correct one

        if request.method in ["PUT", "PATCH"]:
            serializer = self.get_serializer(
                match, data=request.data, partial=(request.method == "PATCH")
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        elif request.method == "DELETE":
            match.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    
class SessionViewSet(ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        if user.is_staff or user.is_superuser:
            return Session.objects.all()
        
        if hasattr(user, 'therapist'):
            return Session.objects.filter(therapist=user.therapist)
        elif hasattr(user, 'patient'):
            return Session.objects.filter(patient=user.patient)
        return Session.objects.none()

    def perform_create(self, serializer):
        user = self.request.user

        if user.is_superuser:
            serializer.save()
        elif hasattr(user, 'patient'):
            serializer.save(patient=user.patient)
        elif hasattr(user, 'therapist'):
            serializer.save(therapist=user.therapist)
        else:
            raise PermissionDenied("Only superadmins, patients, or therapists can create sessions.")

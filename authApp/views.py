from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import PatientCreateSerializer, TherapistCreateSerializer, UserSerializer,PatientSerializer,TherapistSerializer,LoginSerializer
from .models import User, Patient, Therapist
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsAdmin, IsAdminOrSelfPatient, IsAdminOrSelfTherapist


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]



class PatientViewSet(ModelViewSet):
    #will be overriden by the get_queryset method anyway:
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAdminOrSelfPatient]

    def get_queryset(self):
        # If the user is a patient, return only their own data
        if self.request.user.role == 'patient':
            return Patient.objects.filter(user=self.request.user)
        # Admins/staff can access all patient data
        return Patient.objects.all()

class TherapistViewSet(ModelViewSet):   
    #will be overriden by the get_queryset method anyway:
    queryset = Therapist.objects.all()
    serializer_class = TherapistSerializer
    permission_classes = [IsAdminOrSelfTherapist]

    def get_queryset(self):
        # If the user is a THERAPIST, return only their own data
        if self.request.user.role == 'therapist':
            return Therapist.objects.filter(user=self.request.user)
        # Admins/staff can access all patient data
        return Patient.objects.all()
    
class PatientCreateView(generics.CreateAPIView):
    serializer_class = PatientCreateSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Patient registered successfully. Please log in.',
            'login_url': 'auth/api/login/'
        }, status=status.HTTP_201_CREATED)

class TherapistCreateView(generics.CreateAPIView):
    serializer_class = TherapistCreateSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Therapist registered successfully. Please log in.'
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            role = user.role if user.role else 'unknown'
            return Response({
                'user': {
                    'email': user.email,
                    'role': role
                },
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


















# class UserProfileView(generics.RetrieveUpdateAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         return self.request.user

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)

#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         if serializer.is_valid():
#             self.perform_update(serializer)
#             return Response(
#                 {"message": "Profile updated successfully", "data": serializer.data},
#                 status=status.HTTP_200_OK
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView
from rest_framework.response import Response
from .views import UserViewSet, PatientCreateView, TherapistCreateView, PatientViewSet, TherapistViewSet, LoginView, verify_email, MatchViewSet, SessionViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'therapists', TherapistViewSet)
router.register(r'users', UserViewSet)
router.register(r'matches', MatchViewSet)
router.register(r'sessions', SessionViewSet)
class CustomAPIRootView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({
            'patients': request.build_absolute_uri('patients/'),
            'therapists': request.build_absolute_uri('therapists/'),
            'users': request.build_absolute_uri('users/'),
            'matches': request.build_absolute_uri('matches/'), # MatchViewSet
            'sessions': request.build_absolute_uri('sessions/'), # SessionViewSet
            'register_patient': request.build_absolute_uri('register/patient/'),
            'register_therapist': request.build_absolute_uri('register/therapist/'),
            'login': request.build_absolute_uri('login/'),
            'token_refresh': request.build_absolute_uri('token/refresh/')
        })

urlpatterns = [
    path('', CustomAPIRootView.as_view(), name='api_root'),
    path('', include(router.urls)),
    path('register/patient/', PatientCreateView.as_view(), name='patient_register'),
    path('register/therapist/', TherapistCreateView.as_view(), name='therapist_register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-email/<uuid:token>/', verify_email, name='verify_email'),

]
from django.urls import path
from .views import PatientCreateView, TherapistCreateView, UserProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('Create/patient/', PatientCreateView.as_view(), name='patient_Create'),
    path('Create/therapist/', TherapistCreateView.as_view(), name='therapist_Create'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]
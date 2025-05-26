from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VideoSessionViewSet

router = DefaultRouter()
router.register(r'sessions', VideoSessionViewSet, basename='video-session')

# The following URLs will be available:
# /sessions/ - List sessions (GET) or create session (POST)
# /sessions/{id}/ - Retrieve, update or delete session
# /sessions/create_room/ - Create a new video session (POST)
# /sessions/get_token/ - Get token for joining session (GET)
# /sessions/validate_url_token/ - Validate URL token for direct join (GET)

urlpatterns = [
    path('', include(router.urls)),
] 
# profiles/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, LinkViewSet, UserCreateView, ProfileMeView # <-- Import new view

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'links', LinkViewSet, basename='link')

urlpatterns = router.urls + [
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('me/', ProfileMeView.as_view(), name='profile-me'), # <-- Add this line for the 'me' endpoint
]
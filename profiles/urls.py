# profiles/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
# Make sure to import the new view
from .views import ProfileViewSet, LinkViewSet, UserCreateView, ProfileMeView, GenerateBioView 

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'links', LinkViewSet, basename='link')

urlpatterns = router.urls + [
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('me/', ProfileMeView.as_view(), name='profile-me'),
    path('generate-bio/', GenerateBioView.as_view(), name='generate-bio'), # <-- Add this line
]
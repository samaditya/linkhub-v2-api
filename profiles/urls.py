# profiles/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, LinkViewSet,UserCreateView

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'links', LinkViewSet, basename='link')

urlpatterns = router.urls + [
    path('register/', UserCreateView.as_view(), name='user-register'),
]
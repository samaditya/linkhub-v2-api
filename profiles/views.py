# profiles/views.py

from rest_framework import viewsets, generics
from django.contrib.auth.models import User
from .models import Profile, Link
from .serializers import ProfileSerializer, LinkSerializer,UserCreateSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly,isAuthenticated
from .permissions import IsOwnerOrReadOnly

# We will add permissions later
# from rest_framework.permissions import IsAuthenticated
# from .permissions import IsOwnerOrReadOnly

class ProfileMeView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # We need to find the user's profile to link the link to
        profile = Profile.objects.get(owner=self.request.user)
        serializer.save(profile=profile)

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
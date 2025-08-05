# profiles/views.py

from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly # <-- Update import
from .models import Profile, Link, User
from .serializers import ProfileSerializer, LinkSerializer, UserCreateSerializer
from .permissions import IsOwnerOrReadOnly

# --- This is our new view ---
class ProfileMeView(generics.RetrieveUpdateAPIView):
    """
    A view for the logged-in user to retrieve and update their own profile.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated] # <-- Only authenticated users can access this

    def get_object(self):
        # This method returns the profile object associated with the request.user
        return self.request.user.profile
# ----------------------------

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filterset_fields = ['owner__username', 'slug'] # <-- Let's add slug filtering here

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        profile = Profile.objects.get(owner=self.request.user)
        serializer.save(profile=profile)

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
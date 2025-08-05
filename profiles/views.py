# profiles/views.py

import os
import random # Import the random library for the mock generator
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile, Link, User
from .serializers import ProfileSerializer, LinkSerializer, UserCreateSerializer
from .permissions import IsOwnerOrReadOnly


class ProfileMeView(generics.RetrieveUpdateAPIView):
    """
    A view for the logged-in user to retrieve and update their own profile.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


class ProfileViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing public profiles.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filterset_fields = ['owner__username', 'slug']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LinkViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing links associated with a profile.
    """
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        profile = Profile.objects.get(owner=self.request.user)
        serializer.save(profile=profile)


class UserCreateView(generics.CreateAPIView):
    """
    A view for public user registration.
    """
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


# --- MOCK AI FUNCTION (Free) ---
def generate_mock_bio(keywords):
    templates = [
        "Seasoned {keywords} specialist, crafting robust digital solutions. Passionate about building the future of the web.",
        "Expert in {keywords}. Dedicated to creating clean, efficient code and solving complex problems.",
        "A {keywords} enthusiast with a knack for backend development. Always learning and exploring new technologies.",
        "Driven by a passion for {keywords}. Let's connect and build something amazing together.",
    ]
    template = random.choice(templates)
    return template.format(keywords=keywords)


class GenerateBioView(APIView):
    """
    A view to handle AI Bio Generation requests (using a free, mock generator).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        keywords = request.data.get('keywords')
        if not keywords:
            return Response(
                {"error": "Keywords are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Call our local, free mock function instead of OpenAI
            generated_bio = generate_mock_bio(keywords)
            
            return Response({"bio": generated_bio}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error in mock generator: {e}") 
            return Response(
                {"error": "Failed to generate bio."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
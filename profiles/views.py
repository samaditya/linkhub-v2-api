# profiles/views.py

import os
from openai import OpenAI
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
    permission_classes = [IsAuthenticated] # Only authenticated users can access this

    def get_object(self):
        # This method returns the profile object associated with the request.user
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
        # Find the user's profile and associate the new link with it
        profile = Profile.objects.get(owner=self.request.user)
        serializer.save(profile=profile)


class UserCreateView(generics.CreateAPIView):
    """
    A view for public user registration.
    """
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class GenerateBioView(APIView):
    """
    A view to handle AI Bio Generation requests.
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
            client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
            prompt = f"You are a professional branding expert. Write a short, engaging bio (under 160 characters) for a person with these keywords: {keywords}"

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                n=1,
                stop=None,
                temperature=0.7,
            )
            generated_bio = response.choices[0].message.content.strip()
            return Response({"bio": generated_bio}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error calling OpenAI: {e}") 
            return Response(
                {"error": "Failed to generate bio from AI service."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
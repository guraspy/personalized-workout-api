from django.contrib.auth import get_user_model
User = get_user_model() 

from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Exercise, WorkoutPlan, Goal, UserTracking
from .serializers import (
    RegisterSerializer, UserSerializer, ExerciseSerializer,
    WorkoutPlanSerializer, GoalSerializer, UserTrackingSerializer
    )


class RegistrationView(generics.CreateAPIView):
    """
    Creates a new user account.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [] 
    
class LogoutView(APIView):
    """
    Blacklists the provided refresh token.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
            
        except Exception as e:
            return Response({"error": "Invalid token or token not provided."}, status=status.HTTP_400_BAD_REQUEST)

class ExerciseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A read-only endpoint for viewing the list of predefined exercises.
    All authenticated users can view, but only admins can add them via admin panel or seed script.
    """
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]

class WorkoutPlanViewSet(viewsets.ModelViewSet):
    """
    This ViewSet allows a user to create, view, update, and delete their own workout plans.
    """
    serializer_class = WorkoutPlanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Overriding this method to filter the
        plans and return only the ones belonging to the currently logged-in user.
        """
        if getattr(self, 'swagger_fake_view', False):# this is for safe swagger load
            return WorkoutPlan.objects.none() # return an empty queryset for the docs builder
        
        return WorkoutPlan.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        When a new plan is created, we override this method to automatically
        set the user to the currently logged-in user.
        """
        serializer.save(user=self.request.user)

class GoalViewSet(viewsets.ModelViewSet):
    """
    Allows users to manage their own fitness goals.
    """
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Only return goals for the current user."""
        if getattr(self, 'swagger_fake_view', False):
            return Goal.objects.none() # return an empty queryset for the docs builder
            
        return Goal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Set the user automatically on creation."""
        serializer.save(user=self.request.user)

class UserTrackingViewSet(viewsets.ModelViewSet):
    """
    Allows users to log and view their own weight/tracking data.
    """
    serializer_class = UserTrackingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Only return tracking data for the current user."""
        if getattr(self, 'swagger_fake_view', False):
            return UserTracking.objects.none() # return an empty queryset for the docs builder
            
        return UserTracking.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        """Set the user automatically on creation."""
        serializer.save(user=self.request.user)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ExerciseViewSet,
    WorkoutPlanViewSet,
    GoalViewSet,
    UserTrackingViewSet,
    RegistrationView,
    LogoutView
)

router = DefaultRouter()
router.register(r'exercises', ExerciseViewSet, basename='exercise')
router.register(r'workout-plans', WorkoutPlanViewSet, basename='workoutplan')
router.register(r'goals', GoalViewSet, basename='goal')
router.register(r'tracking', UserTrackingViewSet, basename='usertracking')

urlpatterns = [
    path('', include(router.urls)),
    
    path('auth/register/', RegistrationView.as_view(), name='register'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
]

from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Exercise, WorkoutPlan, PlanExercise, UserTracking, Goal

User = get_user_model()

#User & Auth serializers
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model, used for displaying user info.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}} 

    def create(self, validated_data):
        #Overriding cteate because 'create_user' correctly hashes the password
        user = User.objects.create_user(validated_data['username'], email=validated_data['email'], password=validated_data['password'])
        return user

# Main app serializers
class ExerciseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Exercise model.
    """
    class Meta:
        model = Exercise
        fields = '__all__'

class GoalSerializer(serializers.ModelSerializer):
    """
    Serializer for user goals.
    """
    user = serializers.ReadOnlyField(source='user.username') 

    class Meta:
        model = Goal
        fields = '__all__'

class UserTrackingSerializer(serializers.ModelSerializer):
    """
    Serializer for tracking user weight.
    """
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = UserTracking
        fields = '__all__'

class PlanExerciseSerializer(serializers.ModelSerializer):
    """
    Serializer for a specific exercise within a plan.
    This shows the details of the exercise, not just its ID.
    """
    # Using a nested serializer to show the full exercise details.
    exercise = ExerciseSerializer(read_only=True) 
    # An ID field to specify which exercise to add to the plan on creation.
    exercise_id = serializers.PrimaryKeyRelatedField(
        queryset=Exercise.objects.all(), source='exercise', write_only=True
    )

    class Meta:
        model = PlanExercise
        fields = ('id', 'exercise', 'exercise_id', 'sets', 'reps_or_duration', 'order')

class WorkoutPlanSerializer(serializers.ModelSerializer):
    """
    Serializer for a user's workout plan, including all its exercises.
    """
    user = serializers.ReadOnlyField(source='user.username')
    plan_exercises = PlanExerciseSerializer(many=True)

    class Meta:
        model = WorkoutPlan
        fields = ('id', 'user', 'name', 'goal', 'frequency', 'is_active', 'plan_exercises')

    def create(self, validated_data):
        # This custom create method handles the nested `plan_exercises`.
        exercises_data = validated_data.pop('plan_exercises')
        workout_plan = WorkoutPlan.objects.create(**validated_data)
        for exercise_data in exercises_data:
            PlanExercise.objects.create(workout_plan=workout_plan, **exercise_data)
        return workout_plan

    def update(self, instance, validated_data):
        # This custom update handles updating the plan and its exercises.
        exercises_data = validated_data.pop('plan_exercises')
        instance.name = validated_data.get('name', instance.name)
        instance.goal = validated_data.get('goal', instance.goal)
        instance.frequency = validated_data.get('frequency', instance.frequency)
        instance.save()

        # Clear existing exercises and add the new ones
        instance.plan_exercises.all().delete()
        for exercise_data in exercises_data:
            PlanExercise.objects.create(workout_plan=instance, **exercise_data)

        return instance
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model() 

class Exercise(models.Model):
    """
    Predefined exercise library.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    
    target_muscles = models.JSONField(
        default=list,
        blank=True,
        help_text="A list of muscle groups targeted, e.g., ['Chest', 'Triceps']"
    )
    equipment = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class WorkoutPlan(models.Model):
    """
    The user's overall plan containing multiple exercises.
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='workout_plans'
    )
    name = models.CharField(max_length=150)
    goal = models.TextField(blank=True, null=True, help_text="e.g., 'Build Strength', 'Weight Loss'")
    frequency = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        help_text="E.g., 3 times a week, daily."
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'name') # A user can not have two plans with the same name

    def __str__(self):
        return f"{self.user.username}'s Plan: {self.name}"

class PlanExercise(models.Model):
    """
    A concrete exercise instance within a specific Workout Plan. 
    This is the M:M relationship with extra data (sets/reps).
    """
    workout_plan = models.ForeignKey(
        WorkoutPlan, 
        on_delete=models.CASCADE, 
        related_name='plan_exercises'
    )
    exercise = models.ForeignKey(
        Exercise, 
        on_delete=models.CASCADE, 
        related_name='plans'
    )
    sets = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    reps_or_duration = models.CharField(
        max_length=50, 
        help_text="E.g., '10 reps', '30 seconds', 'Failure'"
    )
    order = models.PositiveSmallIntegerField(
        help_text="The sequence of the exercise in the workout."
    )

    class Meta:
        ordering = ['order']
        # Ensures an exercise can only appear once in a plan at a specific order
        unique_together = ('workout_plan', 'order') 

    def __str__(self):
        return f"{self.workout_plan.name} - {self.exercise.name}"

class UserTracking(models.Model):
    """
    Records a user's weight or other metric on a specific date.
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='tracking_data'
    )
    date = models.DateField()
    weight_kg = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        blank=True, 
        null=True
    )
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'date') # A user can only log weight once per day
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class Goal(models.Model):
    """
    Fitness goals set by the user.
    """
    GOAL_TYPES = (
        ('WEIGHT', 'Weight Loss/Gain'),
        ('EXERCISE', 'Exercise Performance'),
        ('OTHER', 'Other Fitness Goal'),
    )

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='goals'
    )
    name = models.CharField(max_length=150, help_text="Short name for the goal.")
    goal_type = models.CharField(max_length=10, choices=GOAL_TYPES)
    target_value = models.CharField(
        max_length=100, 
        help_text="E.g., '80 kg', '50 pushups', 'Run 5k'"
    )
    is_achieved = models.BooleanField(default=False)
    target_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Goal: {self.name}"
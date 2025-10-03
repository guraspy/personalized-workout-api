from django.contrib import admin
from .models import (
    Exercise, 
    WorkoutPlan, 
    PlanExercise, 
    UserTracking, 
    Goal
)

admin.site.register(UserTracking)
admin.site.register(Goal)
admin.site.register(Exercise)
# admin.site.register(WorkoutPlan)
# admin.site.register(PlanExercise)


#Add planexercise as an inline to workoutplan
class PlanExerciseInline(admin.TabularInline):
    """
    Allows editing PlanExercise objects directly within the WorkoutPlan form.
    """
    model = PlanExercise
    extra = 1
    fields = ('exercise', 'sets', 'reps_or_duration', 'order')

@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    """
    Customizing the WorkoutPlan admin view.
    """
    list_display = ('name', 'user', 'frequency', 'is_active', 'created_at')
    list_filter = ('is_active', 'user')
    search_fields = ('name', 'user__username', 'goal')
    # inline planexercise to manage exercises inside the workoutplan
    inlines = [PlanExerciseInline]
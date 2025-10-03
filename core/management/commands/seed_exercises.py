from django.core.management.base import BaseCommand
from core.models import Exercise
import json

class Command(BaseCommand):
    help = 'Seeds the database with predefined exercises'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding exercises...'))

        exercises = [
            {'name': 'Push-up', 'description': 'A classic bodyweight exercise.', 'instructions': '...', 'target_muscles': ['Chest', 'Shoulders', 'Triceps'], 'equipment': 'None'},
            {'name': 'Squat', 'description': 'A fundamental lower body exercise.', 'instructions': '...', 'target_muscles': ['Quadriceps', 'Glutes', 'Hamstrings'], 'equipment': 'None'},
            {'name': 'Pull-up', 'description': 'An upper body exercise targeting the back.', 'instructions': '...', 'target_muscles': ['Back', 'Biceps'], 'equipment': 'Pull-up bar'},
            {'name': 'Plank', 'description': 'An isometric core strength exercise.', 'instructions': '...', 'target_muscles': ['Core', 'Abdominals'], 'equipment': 'None'},
            {'name': 'Lunge', 'description': 'A single-leg bodyweight exercise.', 'instructions': '...', 'target_muscles': ['Quadriceps', 'Glutes'], 'equipment': 'None'},
            {'name': 'Dumbbell Bench Press', 'description': 'Chest press using dumbbells.', 'instructions': '...', 'target_muscles': ['Chest', 'Shoulders', 'Triceps'], 'equipment': 'Dumbbells, Bench'},
            {'name': 'Barbell Deadlift', 'description': 'A full-body compound lift.', 'instructions': '...', 'target_muscles': ['Back', 'Glutes', 'Hamstrings'], 'equipment': 'Barbell'},
            {'name': 'Overhead Press', 'description': 'A shoulder strength exercise.', 'instructions': '...', 'target_muscles': ['Shoulders', 'Triceps'], 'equipment': 'Barbell/Dumbbells'},
            {'name': 'Bent-Over Row', 'description': 'A back-strengthening exercise.', 'instructions': '...', 'target_muscles': ['Back', 'Biceps'], 'equipment': 'Barbell/Dumbbells'},
            {'name': 'Leg Press', 'description': 'A machine-based lower body exercise.', 'instructions': '...', 'target_muscles': ['Quadriceps', 'Glutes'], 'equipment': 'Leg Press Machine'},
            {'name': 'Bicep Curl', 'description': 'An isolation exercise for the biceps.', 'instructions': '...', 'target_muscles': ['Biceps'], 'equipment': 'Dumbbells/Barbell'},
            {'name': 'Tricep Extension', 'description': 'An isolation exercise for the triceps.', 'instructions': '...', 'target_muscles': ['Triceps'], 'equipment': 'Dumbbells/Cable Machine'},
            {'name': 'Lat Pulldown', 'description': 'A machine exercise for the back.', 'instructions': '...', 'target_muscles': ['Back', 'Biceps'], 'equipment': 'Lat Pulldown Machine'},
            {'name': 'Calf Raise', 'description': 'An exercise for strengthening the calves.', 'instructions': '...', 'target_muscles': ['Calves'], 'equipment': 'None/Weights'},
            {'name': 'Russian Twist', 'description': 'A core exercise for the obliques.', 'instructions': '...', 'target_muscles': ['Core', 'Obliques'], 'equipment': 'None/Weight'},
            {'name': 'Burpee', 'description': 'A full-body calisthenics exercise.', 'instructions': '...', 'target_muscles': ['Full Body', 'Cardio'], 'equipment': 'None'},
            {'name': 'Kettlebell Swing', 'description': 'A ballistic exercise for power.', 'instructions': '...', 'target_muscles': ['Glutes', 'Hamstrings', 'Back'], 'equipment': 'Kettlebell'},
            {'name': 'Hanging Leg Raise', 'description': 'An advanced core exercise.', 'instructions': '...', 'target_muscles': ['Core', 'Abdominals'], 'equipment': 'Pull-up bar'},
            {'name': 'Running', 'description': 'Cardiovascular exercise.', 'instructions': '...', 'target_muscles': ['Cardio', 'Legs'], 'equipment': 'None'},
            {'name': 'Cycling', 'description': 'Low-impact cardiovascular exercise.', 'instructions': '...', 'target_muscles': ['Cardio', 'Legs'], 'equipment': 'Bicycle/Stationary Bike'},
        ]

        for exercise_data in exercises:
            # `get_or_create` prevents creating duplicates if the script is run multiple times.
            exercise, created = Exercise.objects.get_or_create(
                name=exercise_data['name'],
                defaults={
                    'description': exercise_data['description'],
                    'instructions': exercise_data['instructions'],
                    'target_muscles': exercise_data['target_muscles'],
                    'equipment': exercise_data['equipment']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created exercise: {exercise.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Exercise already exists: {exercise.name}'))

        self.stdout.write(self.style.SUCCESS('Finished seeding exercises.'))
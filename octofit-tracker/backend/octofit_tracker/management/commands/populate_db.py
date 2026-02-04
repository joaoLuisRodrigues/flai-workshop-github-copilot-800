from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database population...'))
        
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        
        # Create Teams
        self.stdout.write('Creating teams...')
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Avengers assemble! The mightiest heroes of Earth.',
            members=[]
        )
        
        team_dc = Team.objects.create(
            name='Team DC',
            description='Justice League - Defenders of truth and justice.',
            members=[]
        )
        
        # Create Users (Superheroes)
        self.stdout.write('Creating superhero users...')
        
        # Marvel Heroes
        marvel_heroes = [
            {'username': 'Iron Man', 'email': 'tony.stark@marvel.com', 'password': 'arc_reactor_2026'},
            {'username': 'Captain America', 'email': 'steve.rogers@marvel.com', 'password': 'shield_forever'},
            {'username': 'Thor', 'email': 'thor.odinson@asgard.marvel.com', 'password': 'mjolnir_power'},
            {'username': 'Black Widow', 'email': 'natasha.romanoff@marvel.com', 'password': 'red_room_grad'},
            {'username': 'Hulk', 'email': 'bruce.banner@marvel.com', 'password': 'smash_time'},
            {'username': 'Spider-Man', 'email': 'peter.parker@marvel.com', 'password': 'web_slinger'},
        ]
        
        # DC Heroes
        dc_heroes = [
            {'username': 'Superman', 'email': 'clark.kent@dc.com', 'password': 'krypton_lives'},
            {'username': 'Batman', 'email': 'bruce.wayne@dc.com', 'password': 'dark_knight_rises'},
            {'username': 'Wonder Woman', 'email': 'diana.prince@themyscira.dc.com', 'password': 'amazon_warrior'},
            {'username': 'Flash', 'email': 'barry.allen@dc.com', 'password': 'speed_force'},
            {'username': 'Aquaman', 'email': 'arthur.curry@atlantis.dc.com', 'password': 'king_of_seas'},
            {'username': 'Green Lantern', 'email': 'hal.jordan@dc.com', 'password': 'willpower_ring'},
        ]
        
        marvel_users = []
        for hero in marvel_heroes:
            user = User.objects.create(
                username=hero['username'],
                email=hero['email'],
                password=hero['password'],
                team='Team Marvel'
            )
            marvel_users.append(user)
        
        dc_users = []
        for hero in dc_heroes:
            user = User.objects.create(
                username=hero['username'],
                email=hero['email'],
                password=hero['password'],
                team='Team DC'
            )
            dc_users.append(user)
        
        # Update team members
        team_marvel.members = [user.email for user in marvel_users]
        team_marvel.save()
        
        team_dc.members = [user.email for user in dc_users]
        team_dc.save()
        
        # Create Activities
        self.stdout.write('Creating activities...')
        activity_types = ['Running', 'Cycling', 'Swimming', 'Weightlifting', 'Boxing', 'Yoga', 'HIIT', 'CrossFit']
        
        all_users = marvel_users + dc_users
        for user in all_users:
            # Create 5-10 random activities for each user
            num_activities = random.randint(5, 10)
            for i in range(num_activities):
                activity_type = random.choice(activity_types)
                duration = random.randint(30, 120)  # 30 to 120 minutes
                distance = round(random.uniform(3, 15), 2) if activity_type in ['Running', 'Cycling', 'Swimming'] else None
                calories = duration * random.randint(8, 15)  # Rough calorie calculation
                days_ago = random.randint(0, 30)
                activity_date = timezone.now() - timedelta(days=days_ago)
                
                Activity.objects.create(
                    user_email=user.email,
                    activity_type=activity_type,
                    duration=duration,
                    distance=distance,
                    calories=calories,
                    date=activity_date,
                    notes=f'{user.username} completed {activity_type} workout'
                )
        
        # Create Leaderboard
        self.stdout.write('Creating leaderboard entries...')
        for user in all_users:
            activities = Activity.objects.filter(user_email=user.email)
            total_activities = activities.count()
            total_calories = sum(activity.calories for activity in activities)
            total_duration = sum(activity.duration for activity in activities)
            
            Leaderboard.objects.create(
                user_email=user.email,
                username=user.username,
                team=user.team,
                total_activities=total_activities,
                total_calories=total_calories,
                total_duration=total_duration,
                rank=0  # Will be calculated later
            )
        
        # Update ranks
        leaderboard_entries = Leaderboard.objects.all().order_by('-total_calories')
        for rank, entry in enumerate(leaderboard_entries, start=1):
            entry.rank = rank
            entry.save()
        
        # Create Workouts
        self.stdout.write('Creating workout suggestions...')
        workouts = [
            {
                'name': 'Iron Man\'s Arc Reactor Circuit',
                'description': 'High-intensity circuit training inspired by Tony Stark\'s engineering precision.',
                'difficulty': 'advanced',
                'duration': 45,
                'calories_estimate': 600,
                'exercises': [
                    {'name': 'Burpees', 'reps': 20},
                    {'name': 'Push-ups', 'reps': 30},
                    {'name': 'Mountain Climbers', 'reps': 40},
                    {'name': 'Jump Squats', 'reps': 25}
                ],
                'target_audience': 'Team Marvel'
            },
            {
                'name': 'Captain America\'s Super Soldier Strength',
                'description': 'Build strength and endurance worthy of the First Avenger.',
                'difficulty': 'intermediate',
                'duration': 60,
                'calories_estimate': 500,
                'exercises': [
                    {'name': 'Shield Throws (Medicine Ball)', 'reps': 15},
                    {'name': 'Pull-ups', 'reps': 12},
                    {'name': 'Lunges', 'reps': 20},
                    {'name': 'Plank Hold', 'duration': '60 seconds'}
                ],
                'target_audience': 'Team Marvel'
            },
            {
                'name': 'Thor\'s Asgardian Hammer Workout',
                'description': 'Legendary strength training fit for the God of Thunder.',
                'difficulty': 'advanced',
                'duration': 50,
                'calories_estimate': 700,
                'exercises': [
                    {'name': 'Hammer Curls', 'reps': 15},
                    {'name': 'Overhead Press', 'reps': 12},
                    {'name': 'Deadlifts', 'reps': 10},
                    {'name': 'Battle Ropes', 'duration': '45 seconds'}
                ],
                'target_audience': 'Team Marvel'
            },
            {
                'name': 'Batman\'s Dark Knight Training',
                'description': 'Stealth, strength, and agility training from Gotham\'s guardian.',
                'difficulty': 'advanced',
                'duration': 55,
                'calories_estimate': 650,
                'exercises': [
                    {'name': 'Ninja Jumps', 'reps': 20},
                    {'name': 'Hanging Leg Raises', 'reps': 15},
                    {'name': 'Shadow Boxing', 'duration': '3 minutes'},
                    {'name': 'Grappling Rope Climbs', 'reps': 5}
                ],
                'target_audience': 'Team DC'
            },
            {
                'name': 'Superman\'s Kryptonian Power',
                'description': 'Build super strength with this high-intensity power workout.',
                'difficulty': 'advanced',
                'duration': 40,
                'calories_estimate': 800,
                'exercises': [
                    {'name': 'Flying Push-ups (Plyometric)', 'reps': 15},
                    {'name': 'Box Jumps', 'reps': 20},
                    {'name': 'Weighted Squats', 'reps': 15},
                    {'name': 'Farmer\'s Carry', 'distance': '100 meters'}
                ],
                'target_audience': 'Team DC'
            },
            {
                'name': 'Wonder Woman\'s Warrior Training',
                'description': 'Amazon warrior training for strength and grace.',
                'difficulty': 'intermediate',
                'duration': 45,
                'calories_estimate': 550,
                'exercises': [
                    {'name': 'Lasso Swings (Resistance Band)', 'reps': 20},
                    {'name': 'Warrior Pose Hold', 'duration': '90 seconds'},
                    {'name': 'Shield Blocks (Medicine Ball)', 'reps': 25},
                    {'name': 'Sword Lunges', 'reps': 30}
                ],
                'target_audience': 'Team DC'
            },
            {
                'name': 'Flash\'s Speed Force Cardio',
                'description': 'Lightning-fast cardio workout to maximize speed and endurance.',
                'difficulty': 'intermediate',
                'duration': 35,
                'calories_estimate': 600,
                'exercises': [
                    {'name': 'Sprint Intervals', 'duration': '30 seconds on/30 off'},
                    {'name': 'High Knees', 'reps': 50},
                    {'name': 'Lateral Shuffles', 'reps': 40},
                    {'name': 'Agility Ladder Drills', 'duration': '5 minutes'}
                ],
                'target_audience': 'Team DC'
            },
            {
                'name': 'Spider-Man\'s Web-Slinger Agility',
                'description': 'Develop spider-like agility and flexibility.',
                'difficulty': 'beginner',
                'duration': 30,
                'calories_estimate': 400,
                'exercises': [
                    {'name': 'Wall Climbs', 'reps': 10},
                    {'name': 'Spider Crawls', 'duration': '2 minutes'},
                    {'name': 'Hanging Stretches', 'duration': '60 seconds'},
                    {'name': 'Jump Rope', 'duration': '5 minutes'}
                ],
                'target_audience': 'Team Marvel'
            },
            {
                'name': 'Black Widow\'s Spy Conditioning',
                'description': 'Elite spy conditioning for flexibility and combat readiness.',
                'difficulty': 'intermediate',
                'duration': 40,
                'calories_estimate': 450,
                'exercises': [
                    {'name': 'Martial Arts Combos', 'duration': '5 minutes'},
                    {'name': 'Split Stretches', 'duration': '3 minutes'},
                    {'name': 'Core Twists', 'reps': 30},
                    {'name': 'Parkour Vaults', 'reps': 15}
                ],
                'target_audience': 'Team Marvel'
            },
            {
                'name': 'Aquaman\'s Atlantean Swim',
                'description': 'Build endurance and strength with aquatic-inspired exercises.',
                'difficulty': 'beginner',
                'duration': 35,
                'calories_estimate': 400,
                'exercises': [
                    {'name': 'Swimming (if available)', 'duration': '20 minutes'},
                    {'name': 'Resistance Band Pulls', 'reps': 20},
                    {'name': 'Aqua Lunges', 'reps': 25},
                    {'name': 'Trident Thrusts (Medicine Ball)', 'reps': 15}
                ],
                'target_audience': 'Team DC'
            }
        ]
        
        for workout_data in workouts:
            Workout.objects.create(**workout_data)
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n=== Database Population Complete ==='))
        self.stdout.write(f'Users created: {User.objects.count()}')
        self.stdout.write(f'Teams created: {Team.objects.count()}')
        self.stdout.write(f'Activities created: {Activity.objects.count()}')
        self.stdout.write(f'Leaderboard entries: {Leaderboard.objects.count()}')
        self.stdout.write(f'Workouts created: {Workout.objects.count()}')
        self.stdout.write(self.style.SUCCESS('\n✓ Test data populated successfully with superheroes!'))

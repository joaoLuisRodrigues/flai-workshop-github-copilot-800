from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Team, Activity, Leaderboard, Workout


class UserModelTest(TestCase):
    """Test cases for User model"""
    
    def setUp(self):
        self.user = User.objects.create(
            email='test@example.com',
            username='testuser',
            password='testpass123',
            team='Test Team'
        )
    
    def test_user_creation(self):
        """Test user is created correctly"""
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(str(self.user), 'testuser')


class TeamModelTest(TestCase):
    """Test cases for Team model"""
    
    def setUp(self):
        self.team = Team.objects.create(
            name='Test Team',
            description='A test team',
            members=['test1@example.com', 'test2@example.com']
        )
    
    def test_team_creation(self):
        """Test team is created correctly"""
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(str(self.team), 'Test Team')


class ActivityModelTest(TestCase):
    """Test cases for Activity model"""
    
    def setUp(self):
        self.activity = Activity.objects.create(
            user_email='test@example.com',
            activity_type='Running',
            duration=30,
            distance=5.0,
            calories=300,
            date=timezone.now(),
            notes='Morning run'
        )
    
    def test_activity_creation(self):
        """Test activity is created correctly"""
        self.assertEqual(self.activity.user_email, 'test@example.com')
        self.assertEqual(self.activity.activity_type, 'Running')
        self.assertEqual(self.activity.duration, 30)


class LeaderboardModelTest(TestCase):
    """Test cases for Leaderboard model"""
    
    def setUp(self):
        self.leaderboard = Leaderboard.objects.create(
            user_email='test@example.com',
            username='testuser',
            team='Test Team',
            total_activities=10,
            total_calories=3000,
            total_duration=300,
            rank=1
        )
    
    def test_leaderboard_creation(self):
        """Test leaderboard entry is created correctly"""
        self.assertEqual(self.leaderboard.username, 'testuser')
        self.assertEqual(self.leaderboard.rank, 1)


class WorkoutModelTest(TestCase):
    """Test cases for Workout model"""
    
    def setUp(self):
        self.workout = Workout.objects.create(
            name='Test Workout',
            description='A test workout',
            difficulty='intermediate',
            duration=45,
            calories_estimate=500,
            exercises=[{'name': 'Push-ups', 'reps': 20}],
            target_audience='All'
        )
    
    def test_workout_creation(self):
        """Test workout is created correctly"""
        self.assertEqual(self.workout.name, 'Test Workout')
        self.assertEqual(self.workout.difficulty, 'intermediate')


class UserAPITest(APITestCase):
    """Test cases for User API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create(
            email='api@example.com',
            username='apiuser',
            password='apipass123',
            team='API Team'
        )
    
    def test_get_users_list(self):
        """Test retrieving users list"""
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_user_detail(self):
        """Test retrieving a specific user"""
        response = self.client.get(f'/api/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'api@example.com')


class TeamAPITest(APITestCase):
    """Test cases for Team API endpoints"""
    
    def setUp(self):
        self.team = Team.objects.create(
            name='API Test Team',
            description='Team for API testing',
            members=['member1@example.com']
        )
    
    def test_get_teams_list(self):
        """Test retrieving teams list"""
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ActivityAPITest(APITestCase):
    """Test cases for Activity API endpoints"""
    
    def setUp(self):
        self.activity = Activity.objects.create(
            user_email='api@example.com',
            activity_type='Cycling',
            duration=60,
            distance=15.0,
            calories=600,
            date=timezone.now()
        )
    
    def test_get_activities_list(self):
        """Test retrieving activities list"""
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LeaderboardAPITest(APITestCase):
    """Test cases for Leaderboard API endpoints"""
    
    def setUp(self):
        self.leaderboard = Leaderboard.objects.create(
            user_email='api@example.com',
            username='apiuser',
            team='API Team',
            total_activities=5,
            total_calories=2500,
            total_duration=150,
            rank=1
        )
    
    def test_get_leaderboard_list(self):
        """Test retrieving leaderboard"""
        response = self.client.get('/api/leaderboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WorkoutAPITest(APITestCase):
    """Test cases for Workout API endpoints"""
    
    def setUp(self):
        self.workout = Workout.objects.create(
            name='API Test Workout',
            description='Workout for API testing',
            difficulty='beginner',
            duration=30,
            calories_estimate=400,
            exercises=[{'name': 'Squats', 'reps': 15}],
            target_audience='Beginners'
        )
    
    def test_get_workouts_list(self):
        """Test retrieving workouts list"""
        response = self.client.get('/api/workouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

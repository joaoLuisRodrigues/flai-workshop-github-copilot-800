from django.db import models
from django.contrib.auth.models import AbstractUser


class User(models.Model):
    """User model for Octofit Tracker"""
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    team = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return self.username


class Team(models.Model):
    """Team model for Octofit Tracker"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    members = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'teams'
    
    def __str__(self):
        return self.name


class Activity(models.Model):
    """Activity model for tracking user fitness activities"""
    user_email = models.EmailField(max_length=255)
    activity_type = models.CharField(max_length=100)
    duration = models.IntegerField()  # in minutes
    distance = models.FloatField(null=True, blank=True)  # in km
    calories = models.IntegerField()
    date = models.DateTimeField()
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'activities'
        verbose_name_plural = 'Activities'
    
    def __str__(self):
        return f"{self.user_email} - {self.activity_type}"


class Leaderboard(models.Model):
    """Leaderboard model for team and individual rankings"""
    user_email = models.EmailField(max_length=255)
    username = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    total_activities = models.IntegerField(default=0)
    total_calories = models.IntegerField(default=0)
    total_duration = models.IntegerField(default=0)  # in minutes
    rank = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'leaderboard'
        ordering = ['-total_calories']
    
    def __str__(self):
        return f"{self.username} - Rank #{self.rank}"


class Workout(models.Model):
    """Workout model for personalized workout suggestions"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=50)  # beginner, intermediate, advanced
    duration = models.IntegerField()  # in minutes
    calories_estimate = models.IntegerField()
    exercises = models.JSONField(default=list)
    target_audience = models.CharField(max_length=100, blank=True)
    
    class Meta:
        db_table = 'workouts'
    
    def __str__(self):
        return self.name

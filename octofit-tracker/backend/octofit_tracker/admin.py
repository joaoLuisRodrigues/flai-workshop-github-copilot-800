from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin interface for User model"""
    list_display = ('username', 'email', 'team', 'created_at')
    list_filter = ('team', 'created_at')
    search_fields = ('username', 'email')
    ordering = ('-created_at',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Admin interface for Team model"""
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin interface for Activity model"""
    list_display = ('user_email', 'activity_type', 'duration', 'calories', 'date')
    list_filter = ('activity_type', 'date')
    search_fields = ('user_email', 'activity_type')
    ordering = ('-date',)


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    """Admin interface for Leaderboard model"""
    list_display = ('rank', 'username', 'team', 'total_calories', 'total_activities', 'total_duration')
    list_filter = ('team',)
    search_fields = ('username', 'user_email')
    ordering = ('rank',)
    readonly_fields = ('last_updated',)


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    """Admin interface for Workout model"""
    list_display = ('name', 'difficulty', 'duration', 'calories_estimate', 'target_audience')
    list_filter = ('difficulty', 'target_audience')
    search_fields = ('name', 'description')
    ordering = ('name',)

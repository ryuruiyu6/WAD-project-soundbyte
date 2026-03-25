# views.py - Add this function to provide analytics data
def get_analytics_context(user):
    """Generate analytics data for an artist"""
    from django.db.models import Sum, Count
    
    # This is mock data - replace with actual database queries
    return {
        'monthly_listeners': '78.4M',
        'countries': '156',
        'total_hours': '2.4M',
        'total_streams': '18.2M',
        'new_listeners': '342K',
        'top_region': 'United States',
        'top_region_percent': 42,
        'top_regions': [
            {'flag': '🇺🇸', 'name': 'United States', 'percent': 82},
            {'flag': '🇬🇧', 'name': 'United Kingdom', 'percent': 67},
        ],
        'discovery_rate': 34,
        'active_day': 'Friday',
        'active_day_multiplier': '2.8',
    }

# Update your profile_view to include analytics
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    
    # Increment profile views
    if request.user.is_authenticated and request.user != user:
        profile.profile_views += 1
        profile.save(update_fields=['profile_views'])
    
    # Check if user is following
    is_following = request.user.is_authenticated and request.user in profile.followers.all()
    
    # Get analytics data (only for artists)
    analytics = get_analytics_context(user) if profile.is_artist() else None
    
    context = {
        'profile_user': user,
        'profile': profile,
        'is_own_profile': request.user.is_authenticated and request.user == user,
        'is_following': is_following,
        'analytics': analytics,
        'demographics': get_demographics() if profile.is_artist() else None,
        'top_songs': get_top_songs() if profile.is_artist() else None,
        'engagement': get_engagement() if profile.is_artist() else None,
    }
    return render(request, 'analytics.html' if profile.is_artist() else 'profile.html', context)
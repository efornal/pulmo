from django.conf import settings

def allow_view_users_requests(request):
    allow = False
    if hasattr(settings, 'ALLOW_VIEW_USERS_REQUESTS'):
        allow = settings.ALLOW_VIEW_USERS_REQUESTS
        
    return {'allow_view_users_requests': allow}


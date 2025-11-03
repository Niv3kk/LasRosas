# backend/api/urls.py
from django.urls import path
from .views import health
from .auth_views import LoginView, MeView


urlpatterns = [
    path('health/', health, name='health'),
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/me/', MeView.as_view(), name='auth-me'),
    
]
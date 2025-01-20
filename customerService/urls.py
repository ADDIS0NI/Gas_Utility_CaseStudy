from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_request, name='create_request'),
    path('track/', views.track_requests, name='track_requests'),
    path('submit-request/', views.submit_request, name='submit_request'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('feedback/<int:request_id>/', views.submit_feedback, name='submit_feedback'),
]


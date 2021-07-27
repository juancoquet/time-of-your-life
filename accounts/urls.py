from django.urls import path

from .views import SignupPageView, ProfileView

urlpatterns = [
    path('signup/', SignupPageView.as_view(), name='account_signup'),
    path('profile/<slug:pk>/', ProfileView.as_view(), name='profile'),
]

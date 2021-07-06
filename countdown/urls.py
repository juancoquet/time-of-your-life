from django.urls import path

from countdown import views

urlpatterns = [
    path('<str:dob>', views.grid, name='grid'),
    path('<str:dob>/<str:event_name>=<str:event_date>', views.grid, name='event'),
]

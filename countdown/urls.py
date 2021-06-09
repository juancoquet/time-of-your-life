from django.urls import path

from countdown import views

urlpatterns = [
    path('<slug:dob>', views.grid, name='grid'),
]
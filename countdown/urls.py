from django.urls import path

from countdown import views

urlpatterns = [
    path('<str:dob>', views.grid, name='grid'),
    path('<str:dob>/<str:event_name>=<str:event_date>', views.grid, name='event'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit/<uuid:pk>/', views.EventUpdateView.as_view(), name='event_update'),
    path('delete/<uuid:pk>/', views.EventDeleteView.as_view(), name='event_delete'),
]

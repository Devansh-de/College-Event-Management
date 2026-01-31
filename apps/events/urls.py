from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('<int:pk>/', views.event_detail, name='event_detail'),
    path('create/', views.event_create, name='event_create'),
    path('<int:pk>/update/', views.event_update, name='event_update'),
    path('<int:pk>/delete/', views.event_delete, name='event_delete'),
    path('participants/', views.participant_list, name='participant_list'),
    path('<int:pk>/register/', views.event_register, name='event_register'),
    path('<int:pk>/approve/', views.event_approve, name='event_approve'),
    path('<int:pk>/reject/', views.event_reject, name='event_reject'),
]

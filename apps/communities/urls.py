from django.urls import path
from . import views

urlpatterns = [
    path('', views.club_list, name='club_list'),
    path('<int:club_id>/', views.club_detail, name='club_detail'),
    path('<int:club_id>/join/', views.join_club, name='join_club'),
]

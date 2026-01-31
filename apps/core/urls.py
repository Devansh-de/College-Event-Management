from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('reports/', views.reports, name='reports'),
    path('reports/export/csv/', views.export_reports_csv, name='export_reports_csv'),
    path('reports/export/excel/', views.export_reports_excel, name='export_reports_excel'),
]

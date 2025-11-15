from django.urls import path
from . import views

urlpatterns = [
    path('', views.vehicle_list, name='vehicle_list'),
    path('create/', views.vehicle_create, name='vehicle_create'),
    path('update/<int:pk>/', views.vehicle_update, name='vehicle_update'),
    path('delete/<int:pk>/', views.vehicle_delete, name='vehicle_delete'),
]

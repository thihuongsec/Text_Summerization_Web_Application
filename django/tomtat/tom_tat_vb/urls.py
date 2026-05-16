from django.urls import path
from . import views

urlpatterns = [
    path('', views.giao_dien, name='giao_dien'),
    path('delete-history/<int:id>/', views.delete_history, name='delete_history'),
]
from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListCloth.as_view()),
    path('<int:pk>/', views.DetailCloth.as_view()),
]
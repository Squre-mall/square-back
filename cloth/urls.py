from django.urls import path

from . import views
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register('',)

urlpatterns = [
    path('', views.ListCloth.as_view()),
    path('<int:pk>/', views.DetailCloth.as_view()),
]
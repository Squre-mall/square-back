from django.urls import path, re_path, include


from . import views
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register('alls', views.AllViewSet)
# router.register('outer', views.OuterViewSet)


urlpatterns = [
    # path('', include(router.urls)),

    path('', views.ListCloth.as_view()),
    path('<int:pk>/', views.DetailCloth.as_view()),
    path('detail/', views.ListClothDetailMusinsa.as_view()),
    path('detail/<int:pk>/', views.DetailClothDetailMusinsa.as_view()),
]
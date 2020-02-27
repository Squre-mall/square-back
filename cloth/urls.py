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
    # path('<str:category>/', views.ListCategory.as_view()),
    # path('<str:category>/<int:pk>/', views.DetailCategory.as_view()),
]
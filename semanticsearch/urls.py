from django.urls import path, include
from rest_framework import routers
from semanticsearch import views

router = routers.DefaultRouter()
router.register(r'semanticsearch', views.QueryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import path, include
from rest_framework import routers
from semanticsearch import views

router = routers.DefaultRouter()
router.register(r'semanticsearch', views.QueryViewSet)
router.register(r'topics', views.TopicViewSet)
router.register(r'filtertopics', views.FilterTopicsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

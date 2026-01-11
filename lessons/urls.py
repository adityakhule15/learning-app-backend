from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LessonViewSet, LessonStepViewSet

router = DefaultRouter()
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'steps', LessonStepViewSet, basename='step')

urlpatterns = [
    path('', include(router.urls)),
]


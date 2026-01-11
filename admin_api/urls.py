from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminLessonViewSet, AdminStatsViewSet

router = DefaultRouter()
router.register(r'lessons', AdminLessonViewSet, basename='admin-lesson')
router.register(r'stats', AdminStatsViewSet, basename='admin-stats')

urlpatterns = [
    path('admin/', include(router.urls)),
]


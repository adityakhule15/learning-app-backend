from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from lessons.models import Lesson, LessonStep
from lessons.serializers import LessonSerializer, LessonStepSerializer
from progress_tracker.models import UserProgress
from rest_framework.permissions import IsAdminUser

User = get_user_model()


class IsAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class AdminLessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAdminPermission]
    
    def perform_create(self, serializer):
        serializer.save()
    
    @action(detail=True, methods=['post'])
    def add_step(self, request, pk=None):
        lesson = self.get_object()
        serializer = LessonStepSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(lesson=lesson)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminStatsViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminPermission]
    
    def list(self, request):
        total_users = User.objects.count()
        total_lessons = Lesson.objects.count()
        total_progress = UserProgress.objects.count()
        completed_lessons = UserProgress.objects.filter(completed=True).count()
        
        return Response({
            'total_users': total_users,
            'total_lessons': total_lessons,
            'total_progress_records': total_progress,
            'completed_lessons': completed_lessons,
            'completion_rate': f"{(completed_lessons/total_progress*100):.1f}%" if total_progress > 0 else "0%",
        })
    
    
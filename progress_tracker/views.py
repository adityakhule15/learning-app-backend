from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import UserProgress
from .serializers import UserProgressSerializer, ProgressUpdateSerializer
from lessons.models import Lesson


class ProgressViewSet(viewsets.ModelViewSet):
    serializer_class = UserProgressSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserProgress.objects.filter(user=self.request.user).select_related('lesson')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def update_progress(self, request):
        serializer = ProgressUpdateSerializer(data=request.data)
        if serializer.is_valid():
            lesson_id = serializer.validated_data['lesson_id']
            last_step_completed = serializer.validated_data['last_step_completed']
            time_spent = serializer.validated_data.get('time_spent', 0)
            
            # Get or create progress
            progress, created = UserProgress.objects.get_or_create(
                user=request.user,
                lesson_id=lesson_id,
                defaults={
                    'last_step_completed': last_step_completed,
                    'total_time_spent': time_spent
                }
            )
            
            if not created:
                # Update existing progress
                progress.last_step_completed = max(progress.last_step_completed, last_step_completed)
                progress.total_time_spent += time_spent
                progress.save()
            
            return Response(
                UserProgressSerializer(progress).data,
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def by_lesson(self, request):
        lesson_id = request.query_params.get('lesson_id')
        if not lesson_id:
            return Response(
                {'error': 'lesson_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        progress = get_object_or_404(
            UserProgress,
            user=request.user,
            lesson_id=lesson_id
        )
        
        return Response(UserProgressSerializer(progress).data)
    
    @action(detail=False, methods=['get'])
    def overview(self, request):
        progress_list = self.get_queryset()
        total_lessons = Lesson.objects.filter(is_active=True).count()
        completed_lessons = progress_list.filter(completed=True).count()
        in_progress = progress_list.filter(completed=False).count()
        
        return Response({
            'total_lessons': total_lessons,
            'completed_lessons': completed_lessons,
            'in_progress': in_progress,
            'completion_rate': f"{(completed_lessons/total_lessons*100):.1f}%" if total_lessons > 0 else "0%",
            'progress_list': UserProgressSerializer(progress_list, many=True).data
        })
    

    
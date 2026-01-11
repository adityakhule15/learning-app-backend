from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Lesson, LessonStep
from .serializers import LessonSerializer, LessonStepSerializer
from rest_framework.permissions import AllowAny


class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lesson.objects.filter(is_active=True).prefetch_related('steps')
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'language']
    search_fields = ['title', 'description']
    ordering_fields = ['order', 'created_at']
    ordering = ['order']
    
    @action(detail=True, methods=['get'])
    def steps(self, request, pk=None):
        lesson = self.get_object()
        steps = lesson.steps.all().order_by('step_number')
        serializer = LessonStepSerializer(steps, many=True)
        return Response(serializer.data)


class LessonStepViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LessonStep.objects.all()
    serializer_class = LessonStepSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        lesson_id = self.request.query_params.get('lesson_id')
        if lesson_id:
            queryset = queryset.filter(lesson_id=lesson_id)
        return queryset.order_by('step_number')
    
    
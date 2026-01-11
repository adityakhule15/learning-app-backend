from rest_framework import serializers
from .models import Lesson, LessonStep


class LessonStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonStep
        fields = [
            'id', 'step_number', 'title', 'instruction_text',
            'step_type', 'media_url', 'media_caption',
            'estimated_duration', 'is_interactive'
        ]
        read_only_fields = ['id']


class LessonSerializer(serializers.ModelSerializer):
    steps = LessonStepSerializer(many=True, read_only=True)
    total_steps = serializers.SerializerMethodField()
    estimated_duration = serializers.SerializerMethodField()
    
    class Meta:
        model = Lesson
        fields = [
            'id', 'title', 'description', 'category', 'language',
            'order', 'thumbnail_url', 'estimated_duration',
            'total_steps', 'steps', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_total_steps(self, obj):
        return obj.steps.count()
    
    def get_estimated_duration(self, obj):
        total_seconds = sum(step.estimated_duration for step in obj.steps.all())
        minutes = total_seconds // 60
        return f"{minutes} min"
    
    
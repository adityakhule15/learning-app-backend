from rest_framework import serializers
from .models import UserProgress
from lessons.serializers import LessonSerializer


class UserProgressSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(read_only=True)
    lesson_id = serializers.IntegerField(write_only=True)
    total_steps = serializers.SerializerMethodField()
    completion_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProgress
        fields = [
            'id', 'lesson', 'lesson_id', 'last_step_completed',
            'completed', 'total_time_spent', 'completion_percentage',
            'total_steps', 'started_at', 'last_updated', 'completed_at'
        ]
        read_only_fields = [
            'id', 'lesson', 'completed', 'started_at',
            'last_updated', 'completed_at'
        ]
    
    def get_total_steps(self, obj):
        return obj.lesson.steps.count()
    
    def get_completion_percentage(self, obj):
        total_steps = obj.lesson.steps.count()
        if total_steps == 0:
            return 0
        return int((obj.last_step_completed / total_steps) * 100)
    
    def create(self, validated_data):
        user = self.context['request'].user
        lesson_id = validated_data.pop('lesson_id')
        
        # Get or create progress
        progress, created = UserProgress.objects.get_or_create(
            user=user,
            lesson_id=lesson_id,
            defaults=validated_data
        )
        
        if not created:
            # Update existing progress
            for attr, value in validated_data.items():
                setattr(progress, attr, value)
            progress.save()
        
        return progress


class ProgressUpdateSerializer(serializers.Serializer):
    lesson_id = serializers.IntegerField(required=True)
    last_step_completed = serializers.IntegerField(required=True, min_value=0)
    time_spent = serializers.IntegerField(required=False, default=0, min_value=0)

    